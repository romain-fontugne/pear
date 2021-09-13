import appdirs
import arrow
from collections import defaultdict
import os
import json
import requests
import statistics
import sys
from progress.bar import Bar

CACHE_DIR = appdirs.user_cache_dir('pear', 'IHR')+"/atlas/"
URL_PROBE_INFO = "https://atlas.ripe.net/api/v2/probes/"
URL_MSM = "https://atlas.ripe.net/api/v2/measurements/?target_asn={asn}&status=2&type={type}"
CACHE_EXPIRATION = 60*60*24*7
WINDOW_SIZE_DAYS = 1

class AtlasTraceroute(object):
    def __init__(self, asn, bgp_table, cache_directory=CACHE_DIR, cache_expiration=CACHE_EXPIRATION,
            window_size_days=WINDOW_SIZE_DAYS):
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

        self.all_probes = self.probe_infos()
        self.asn_probes = self.find_probes(asn=self.asn)
        print(f'Found {len(self.asn_probes)} probes in AS{self.asn}')
        self.traceroute_msms = []
        self.find_measurements()
        print(f'Found {len(self.traceroute_msms)} mesurements towards AS{self.asn}')
        self.traceroutes = self.fetch_measurement_results()
        self.country_stats = self.compute_country_stats()

    def probe_infos(self, cached_data=True):

        # Try to get data from cache
        if os.path.exists(self.cache_directory+"/probe_info.json") and cached_data:
            # Get probe information from cache
            cache = json.load(open(self.cache_directory+"/probe_info.json","r"))
            if (arrow.utcnow() - arrow.get(cache["timestamp"])).seconds > CACHE_EXPIRATION:
                sys.stderr.write("Atlas probe cache expired!\n")
            else:
                return cache["probes"]


        # Fetch probe information from RIPE API
        url =  URL_PROBE_INFO
        bar = None
        probes = {}
        with requests.Session() as session:

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

        # Save probe information to cache
        fi = open(self.cache_directory+"/probe_info.json", "w")
        json.dump({
            "probes":probes, 
            "timestamp":str(arrow.utcnow())
            }, fi, indent=4)
        fi.close()

        return probes

    def find_probes(self, asn=None):
        """Return probes corresponding to the given attributes"""

        selected_probes = []

        for probe in self.all_probes.values():
            if ( ('asn_v4' in probe and str(probe['asn_v4']) == asn) 
                    or ('asn_v6' in probe and str(probe['asn_v6']) == asn) ):

                selected_probes.append(probe)

        return selected_probes


    def find_measurements(self):
        """Find IDs for ongoing Atlas measurement targeting selected ASN"""

        url = URL_MSM.format(asn=self.asn, type="traceroute")
        with requests.Session() as session:
            # Fetch all pages
            while url:
                page = session.get(url).json()
                self.traceroute_msms.extend(page["results"])
                url = page['next']


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

        with requests.Session() as session:
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
                            'as_path': defaultdict(list) 
                        } 

                    first_ip = None
                    aspath = []
                    try:
                        rnode = self.bgp_table.rtree.search_best(trace["from"])
                        if rnode: aspath.append(rnode.data['originasn'])
                    except Exception as e:
                        print(trace["from"])
                        print(e)

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
                                if ip2asn == self.asn:
                                    if first_ip is None or first_ip == res["from"]:
                                        first_ip = res["from"]
                                        traceroutes[pid]["as_path"][ipversion+": "+" ".join(aspath)].append(res["rtt"])

                                    else:
                                        # No need to read the end of the traceroute
                                        break

        return traceroutes

    def compute_country_stats(self):
        """Compute RTT stats per country"""

        countries = defaultdict(lambda: defaultdict(dict))

        peer_rtts = defaultdict(lambda: defaultdict(list))
        for pid, traces in self.traceroutes.items():

            country = traces['country']
            probe_stats = {}
            for aspath, rtts in traces['as_path'].items():
                asns_aspath = aspath.split(' ')
                ipversion = asns_aspath[0]
                probe_asn = asns_aspath[1]
                peer_asn = asns_aspath[-2]

                probe_stats[aspath] = {
                        'asn': probe_asn,
                        'min': min(rtts),
                        'med': statistics.median(rtts),
                        'max': max(rtts),
                        'nb_samples': len(rtts)
                        }

                peer_rtts[traces['country']][ipversion+peer_asn].append(rtts)

                if ipversion+peer_asn in countries[country]['peers']:
                    countries[country]['peers'][ipversion+peer_asn]['rtts'].extend(rtts)
                else:
                    countries[country]['peers'][ipversion+peer_asn] = {'rtts':list(rtts)}


            countries[country]['probes'][pid] = probe_stats 

        # Compute stats per country and peer
        for country, types in countries.items():
            for stats in types['peers'].values():
                stats['median'] = statistics.median(stats['rtts'])
                stats['nb_samples'] = len(stats['rtts'])

        return countries



if __name__ == '__main__':
    import sys
    import IPython
    from .bgp_table import BGPTable

    table = BGPTable(2497)
    table.load_bgp("data/mrt/bview.20210615.0000.gz")
    atlas = AtlasTraceroute(2497, table)

    IPython.embed()
