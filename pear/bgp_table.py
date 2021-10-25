import appdirs
from bgpdumpy import BGPDump, TableDumpV2
import radix
import sqlite3
import sys

from rov import ROV
from pear.geolite_city import GeoliteCity

CACHE_DIR = appdirs.user_cache_dir('pear', 'IHR')+"/atlas/"

class BGPTable(object):
    def __init__(self, peer_as, rov=None, gc=None, cache_db=None):
        """Initialize BGP Table attributes"""

        self.main_as = str(peer_as)
        self.rtree = radix.Radix()
        self.peers = set()

        self.iscached = False
        if cache_db is None:
            self.cache_db = CACHE_DIR+'pear.sql'
        else:
            self.cache_db = cache_db

        self.rov = rov
        self.gc = gc


    def load_bgp(self, mrt_fname):
        """Fetch BGP data and add AS paths to the radix tree"""
    
        con = sqlite3.connect(self.cache_db)
        cur = con.cursor()

        self.sqltable = 'bgp_'+mrt_fname.rpartition('/')[2].replace('.','_')
        try:
            # Create table
            cur.execute('''CREATE TABLE {table}
                (prefix text, descr text, originasn text, country text, peer text, as_path text, irr_status text, rpki_status text)'''.format(table=self.sqltable))

            if self.rov is None:
                self.rov = ROV()
                self.rov.load_databases()

            if self.gc is None:
                self.gc = GeoliteCity()
                self.gc.load_database()

            with BGPDump(mrt_fname) as bgp:
                for entry in bgp:

                    # entry.body can be either be TableDumpV1 or TableDumpV2
                    if not isinstance(entry.body, TableDumpV2):
                        continue  # I expect an MRT v2 table dump file

                    # get a string representation of this prefix
                    prefix = f'{entry.body.prefix}/{entry.body.prefixLength}'

                    as_paths = [ route.attr.asPath
                        for route in entry.body.routeEntries
                        if route.attr.asPath.startswith(self.main_as) ]

                    if not len(as_paths):
                        continue

                    # Add path to the tree
                    rnode = self.rtree.add(prefix)
                    as_path = self.clean_aspath(as_paths[0].split())
                    rnode.data['aspath'] = as_path 
                    rnode.data['originasn'] = as_path[-1]
                    if len(as_path) > 1:
                        self.peers.add(as_path[1])

        except sqlite3.OperationalError:
            self.iscached = True

            print(f'Loading cached RIB {self.sqltable}')


            # FIXME: do we really need to reload everything in memory? maybe
            # not needed if everything else have been computed at first load
            con = sqlite3.connect(self.cache_db)
            cur = con.cursor()

            cur.execute("SELECT * FROM {table}".format(table=self.sqltable))

            for prefix, descr, originasn, country, peer, aspath, irr_status, rpki_status in cur:
                rnode = self.rtree.add(prefix)
                rnode.data['descr'] = descr 
                rnode.data['originasn'] = originasn
                rnode.data['country'] = country 
                rnode.data['peer'] = peer 
                rnode.data['aspath'] = aspath.split(' ')
                rnode.data['irr_status'] = irr_status 
                rnode.data['rpki_status'] = rpki_status 


    def cache_rib(self):
        """Save RIB with all computed information to the sqlite database"""

        con = sqlite3.connect(self.cache_db)
        cur = con.cursor()

        for node in self.rtree.nodes():
            d = node.data

            # get prefix description from IRR data
            descr = ''
            if node.prefix in d['irr']:
                try: 
                    descr = next(iter(d['irr'][node.prefix].values()))[0]['descr'] 
                except Exception as e:
                    print('ERROR!', e)
                    pass


            # peer from AS path
            peer = ''
            if len(d['aspath']) > 1:
                peer = d['aspath'][1]

            # push data to database
            cur.execute(
                    "INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?)".format(table=self.sqltable),
                    (node.prefix, descr, d['originasn'], 
                        d['country'], peer, ' '.join(d['aspath']), 
                        d['rov'].get('irr', {'status':''})['status'],
                        d['rov'].get('rpki', {'status':''})['status']
                        )
                    )

        con.commit()
        con.close

    def add_prefix_info(self, prefixes):
        """Add geoloc and IRR data to given prefixes or all prefixes 
        if prefixes=None"""

        nodes = []
        if prefixes is None:
            nodes = self.rtree.nodes()
        else:
            for prefix in prefixes:
                rnode = self.rtree.search_best(prefix)
                if rnode is not None:
                    nodes.append(rnode)
        
        self.add_rov(nodes)
        self.add_geoloc(nodes)


    def clean_table(self, prefixes):
        """Remove all RIB entries that are not in the given list of prefixes"""

        all_prefixes = set([node.prefix for node in self.rtree.nodes()])
        to_remove = all_prefixes.difference(prefixes)
        for node in to_remove:
            self.rtree.delete(node)


    def add_rov(self, nodes):
        """Add RPKI, IRR, delegated data to all given nodes"""

        for rnode in nodes:

            rov_data = self.rov.lookup(rnode.prefix)
            rnode.data['irr'] = rov_data['irr']
            rnode.data['rpki'] = rov_data['rpki']
            rnode.data['delegated'] = rov_data['delegated']

            # Prefix description
            descr = ''
            if (rnode.prefix in rov_data['irr'] 
                    and rnode.data['originasn'] in rov_data['irr'][rnode.prefix] 
                    and len(rov_data['irr'][rnode.prefix][rnode.data['originasn']])):
                descr = rov_data['irr'][rnode.prefix][rnode.data['originasn']][0]['descr']
            rnode.data['descr'] = descr

            
            try:
                rov_data = self.rov.check(rnode.prefix, int(rnode.data['originasn']))
                rnode.data['rov'] = rov_data
            except ValueError:
                rnode.data['rov'] = {}

    def add_geoloc(self, nodes):
        """Geolocate prefixes for all given nodes"""

        for rnode in nodes:

            # find country code
            ip = rnode.prefix.partition('/')[0]
            cc = self.gc.country(ip)

            rnode.data['country'] = cc

    def prefix_info(self, prefix):
        """Return the computed info (geoloc/irr) for the given prefix"""

        rnode = self.rtree.search_best(prefix)
        if rnode is None:
            return {}
        else:
            return rnode.data

    def list_peers(self):
        """Return the list of 1-hop peer ASes"""

        con = sqlite3.connect(self.cache_db)
        cur = con.cursor()
        cur.execute("SELECT distinct(peer) from {table}".format(table=self.sqltable))
        return [peer[0] for peer in cur.fetchall()]

    def clean_aspath(self, aspath):
        """Remove path prepending and duplicate ASes"""
        
        # make sure the path starts with the main AS (and that we have at least
        # one AS e.g. for internal prefixes)
        cleaned = [self.main_as]

        for asn in aspath:
            if asn not in cleaned:
                cleaned.append(asn)
            
        return cleaned

    def add_prefixes(self, prefixes):
        """Ensure that the given list of prefixes is in  the radix tree. 
        Copy the AS path from covering prefixes for prefixes not in the tree."""

        for prefix in prefixes:
            prefix = prefix.strip()
            if self.rtree.search_exact(prefix) is None:
                cov_prefix = self.rtree.search_best(prefix)

                if cov_prefix is None:
                    rnode = self.rtree.add(prefix)
                    rnode.data['aspath'] = [self.main_as, '0'] 
                    rnode.data['originasn'] = '0'
                    sys.stderr.write(
                        f'Error: could not find {prefix} covering prefix! '+
                        'Set origin ASN to 0.\n'
                        )

                else:
                    rnode = self.rtree.add(prefix)
                    rnode.data['aspath'] = cov_prefix.data['aspath']
                    rnode.data['originasn'] = cov_prefix.data['aspath'][-1]

    def list_aspaths(self):
        """Returns all prefixes and corresponding AS paths found in this routing
        table."""

        for node in self.rtree.nodes():
            yield node.prefix, node.data['aspath']

    def list_prefixes(self):
        """Returns all prefixes and corresponding information."""

        for node in self.rtree.nodes():
            yield node.prefix, node.data

    def path(self, prefix):

        rnode = self.rtree.search_best(prefix)
        if rnode is None:
            return prefix, ['']

        return rnode.prefix, rnode.data['aspath']


if __name__ == '__main__':
    import sys
    import IPython

    table = BGPTable(sys.argv[1], 2497)

    IPython.embed()
