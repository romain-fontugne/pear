import appdirs
import arrow
from collections import defaultdict
import os
import requests_cache
from datetime import timedelta
import socket
import statistics
import sys
from progress.bar import Bar

import sqlite3

CACHE_DIR = appdirs.user_cache_dir('pear', 'IHR')+"/atlas/"
URL_PROBE_INFO = "https://atlas.ripe.net/api/v2/probes/"
URL_MSM_SEARCH = "https://atlas.ripe.net/api/v2/measurements/?target_asn={asn}&status=2&type={type}"
URL_MSM = "https://atlas.ripe.net/api/v2/measurements/"
CACHE_EXPIRATION = 1 # days
WINDOW_SIZE_DAYS = 1

class AtlasTraceroute(object):
    def __init__(self, asn, bgp_table, cache_directory=CACHE_DIR, cache_expiration=CACHE_EXPIRATION,
            window_size_days=WINDOW_SIZE_DAYS, measurement_ids=[], cache_db=None):
        """Initialize object with given parameters:
            - asn: ASN used as a target in traceroutes
            - bgp_table: used to map IPs to ASNs
            - cache_directory: directory to cache atlas data
            - cache_expiration: cache expiration in seconds
            - window_size_days: get data for the past window_size_days days
                """
        
        self.asn = str(asn)
        self.bgp_table = bgp_table
        self.cache_directory = cache_directory
        os.makedirs(self.cache_directory, exist_ok=True)
        self.cache_expiration = cache_expiration
        self.window_size_days = window_size_days

        self.dns = {}
        
        if cache_db is None:
            self.cache_db = cache_directory+'pear.sql'
        else:
            self.cache_db = cache_db

        self.con = sqlite3.connect(self.cache_db)
        self.cur = self.con.cursor()
        try:
            # Create table
            self.cur.execute('''CREATE TABLE traceroutes
               (pid integer, asn text, country text, as_path text, af integer, router text, nb_samples integer, min_rtt real, med_rtt real, max_rtt)''')

            # Fetch traceroutes
            self.all_probes = self.probe_infos()
            self.asn_probes = self.find_probes(asn=self.asn)
            print(f'Found {len(self.asn_probes)} probes in AS{self.asn}')
            self.traceroute_msms = []
            self.find_measurements(measurement_ids)

            self.traceroutes = self.fetch_measurement_results()
            # Compute stats and store in db
            self.compute_traceroute_stats()

        except sqlite3.OperationalError:
            # The table already exists
            print('Using cached traceroutes')

        self.con.commit()
        self.con.close()

        # Keep a cursor open for reads
        self.con = sqlite3.connect(self.cache_db, check_same_thread=False)
        self.cur = self.con.cursor()


    def probe_infos(self):

        # Fetch probe information from RIPE API
        url =  URL_PROBE_INFO
        bar = None
        probes = {}
        with requests_cache.CachedSession(self.cache_directory,
                backend='filesystem',
                expire_after=timedelta(days=CACHE_EXPIRATION)) as session:

            # Fetch all pages
            while url:
                page = session.get(url).json()
                if bar is None:
                    bar = Bar(
                        "Fetching probe information from RIPE API", 
                        max=page["count"], 
                        suffix='%(percent)d%%'
                        )

                for probe in page["results"]:
                    bar.next()
                    if "id" in probe:
                        probes[str(probe["id"])] = probe

                url = page['next']
            bar.finish()

        return probes

    def find_probes(self, asn=None):
        """Return probes corresponding to the given attributes"""

        selected_probes = []

        for probe in self.all_probes.values():
            if ( ('asn_v4' in probe and str(probe['asn_v4']) == asn) 
                    or ('asn_v6' in probe and str(probe['asn_v6']) == asn) ):

                selected_probes.append(probe)

        return selected_probes


    def find_measurements(self, msm_ids):
        """Find IDs for ongoing Atlas measurement targeting selected ASN"""

        with requests_cache.CachedSession(self.cache_directory,
                backend='filesystem',
                expire_after=timedelta(days=CACHE_EXPIRATION)) as session:
            if msm_ids:
                for id in msm_ids:
                    url = f'{URL_MSM}{id}'
                    page = session.get(url).json()
                    self.traceroute_msms.append(page)

            else:
                url = URL_MSM_SEARCH.format(asn=self.asn, type="traceroute")
                # Fetch all pages
                while url:
                    page = session.get(url).json()
                    self.traceroute_msms.extend(page["results"])
                    url = page['next']

                print(f'Found {len(self.traceroute_msms)} mesurements towards AS{self.asn}')


            #self.ping_msms = []
            #url = URL_MSM.format(asn=self.asn, type="ping")
            #with requests.Session() as session:
                ## Fetch all pages
                #while url:
                    #page = session.get(url).json()
                    #self.traceroute_msms.extend(page["results"])
                    #url = page['next']

        
    def fetch_measurement_results(self):
        """Get traceroute results from RIPE Atlas' REST API"""

        time_window = arrow.now().shift(days=-WINDOW_SIZE_DAYS).timestamp()
        traceroutes = {} 

        with requests_cache.CachedSession(self.cache_directory,
                backend='filesystem',
                expire_after=timedelta(days=CACHE_EXPIRATION)) as session:
            for msm in self.traceroute_msms:

                page = session.get(msm['result'], params={"start": int(time_window)}).json()

                for trace in page:
                    # Skip errors
                    if ("prb_id" not in trace or trace is None 
                            or "from" not in trace
                            or "error" in trace["result"][0] 
                            or "err" in trace["result"][0]["result"]):
                        continue

                    pid = str(trace["prb_id"])
                    if pid not in self.all_probes:
                        sys.stderr.write(f'Error: Traceroute from unknown probe {pid}\n')
                        continue

                    # summarize traceroutes per probe
                    if pid not in traceroutes:
                        cc = self.all_probes[pid].get('country_code', 'XX')
                        traceroutes[pid] = {
                            'pid': pid,
                            'country': cc,
                            'dst_as_path': defaultdict(lambda: defaultdict(lambda: {'rtt':[]})) 
                        } 

                    first_border_ip = None
                    aspath = []
                    try:
                        rnode = self.bgp_table.rtree.search_best(trace["from"])
                        if rnode: aspath.append(rnode.data['originasn'])
                    except Exception as e:
                        print(trace["from"])
                        print(e)
                        continue

                    ipversion = 'IPv4' if '.' in trace['from'] else 'IPv6'

                    for hop in trace["result"]:
                        if "result" in hop :

                            for res in hop["result"]:
                                if not "from" in res or not "rtt" in res \
                                        or res["rtt"] <= 0.0:
                                    continue

                                # Find origin ASN for this hop
                                rnode = self.bgp_table.rtree.search_best(res["from"])
                                if not rnode:
                                    continue

                                # build AS path
                                ip2asn = rnode.data['originasn']
                                if ip2asn not in aspath:
                                    aspath.append(ip2asn)

                                # keep rtt if first IP or last IP
                                if ip2asn == self.asn or first_border_ip is not None:
                                    if first_border_ip is None or first_border_ip == res["from"]:
                                        first_border_ip = res["from"]
                                        hostname = self.reversedns(res['from']) 
                                        traceroutes[pid]["dst_as_path"][hostname][ipversion+": "+" ".join(aspath)]['rtt'].append(res["rtt"])

                                    else:
                                        # No need to read the end of the traceroute
                                        break

        print('finished reading traceroutes')
        return traceroutes

    def reversedns(self, ip):
        """Find and cache the hostname corresponding to the given IP"""

        if ip not in self.dns:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = ip
            self.dns[ip] = hostname

        return self.dns[ip]

    def compute_traceroute_stats(self):
        """Compute RTT stats min/med/max
        """


        for pid, traces in self.traceroutes.items():

            country = traces['country']

            for router, aspaths in traces['dst_as_path'].items():
                for aspath, stats in aspaths.items(): 
                    rtts = stats['rtt']
                    asns_aspath = aspath.split(' ')
                    probe_asn = asns_aspath[1]
                    self.cur.execute(
                            "INSERT INTO traceroutes VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (pid, probe_asn, country, " ".join(asns_aspath[1:]), 
                                int(asns_aspath[0][-2]), router, len(rtts), 
                                min(rtts), statistics.median(rtts), max(rtts)))

                    #if ipversion+peer_asn not in countries[country]['peers']:
                        #countries[country]['peers'][ipversion+peer_asn] = defaultdict(lambda: {'rtts':list()})
                    #countries[country]['peers'][ipversion+peer_asn][router]['rtts'].extend(rtts)

        # Compute stats per country and peer
        #for country, types in countries.items():
            #for router_stats in types['peers'].values():
                #for stats in router_stats.values():
                    #stats['med'] = statistics.median(stats['rtts'])
                    #stats['nb_samples'] = len(stats['rtts'])

        self.con.commit()

    def country_stats(self, cc, asn=None):


        asn_where = ''
        # Call may come from a different thread, create a new connection  
        if cc is None:
            if asn is not None:
                asn_where = f" WHERE  as_path LIKE '% {asn}%' OR as_path LIKE '%{asn} %' "

            self.cur.execute("select * from traceroutes "+asn_where,)
        else:
            if asn is not None:
                asn_where = f" AND ( as_path LIKE '% {asn}%' OR as_path LIKE '%{asn} %' ) "
            self.cur.execute("select * from traceroutes where country = ? "+asn_where, (cc,))

        return self.cur.fetchall()
        
    def country_code(self):

        # Call may come from a different thread, create a new connection  
        self.cur.execute("select distinct(country) from traceroutes")
        return [cc[0] for cc in self.cur.fetchall()]


if __name__ == '__main__':
    import sys
    import IPython
    from .bgp_table import BGPTable

    table = BGPTable(2497)
    table.load_bgp("data/mrt/bview.20210615.0000.gz")
    atlas = AtlasTraceroute(2497, table)

    IPython.embed()
