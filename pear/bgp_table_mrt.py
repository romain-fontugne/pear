from mrtparse import *
import radix
import sys

from rov import ROV
from pear.geolite_city import GeoliteCity

class BGPTable(object):
    def __init__(self, mrt_fname, peer_as):
        """Initialize BGP Table attributes"""

        self.mrt_fname = mrt_fname
        self.main_as = str(peer_as)
        self.main_as_idx = set()
        self.rtree = radix.Radix()
        self.peers = set()

        self.rov = ROV()
        self.rov.load_databases()

        self.gc = GeoliteCity()
        self.gc.load_database()


    def load_bgp(self):
        """Fetch BGP data and add AS paths to the radix tree"""
    
        for entry in Reader(self.mrt_fname):

            # parse RIB entries
            if ( entry.data['subtype'][1] == 'RIB_IPV4_UNICAST' 
                or entry.data['subtype'][1] == 'RIB_IPV6_UNICAST' ):

                prefix = f"{entry.data['prefix']}/{entry.data['prefix_length']}"
                as_path = []
                recs = [rec 
                            for rec in entry.data['rib_entries']
                                if rec['peer_index'] in self.main_as_idx]
                if len(recs)>1:
                    print('more than one rec per prefix!\n',recs)
                elif len(recs) > 0:
                    rec = recs[0]
                    # Get AS path
                    path = [attribute 
                            for attribute in rec['path_attributes']
                            if attribute['type'][1] == 'AS_PATH'] 
                    if path[0]['length']>0:
                        # fetch the AS path
                        as_path = path[0]['value'][0]['value']

                    # Add path to the radix tree
                    rnode = self.rtree.add(prefix)
                    as_path = self.clean_aspath(as_path)
                    rnode.data['as-path'] = as_path 
                    if len(as_path) > 1:
                        self.peers.add(as_path[1])


            # parse peers list and get main peer indexes
            elif entry.data['subtype'][1] == 'PEER_INDEX_TABLE':
                for idx, peer in enumerate(entry.data['peer_entries']):
                    if peer['peer_as'] == self.main_as:
                        self.main_as_idx.add(idx)

    def add_prefix_info(self):
        """Add geoloc and IRR data to all prefixes in the table"""

        self.add_irr()
        self.add_geoloc()


    def add_irr(self):
        """Add IRR data to all prefixes in the table"""

        for rnode in self.rtree:

            if not 'info' in rnode.data:
                rnode.data['info'] = {}

            # find country code
            irr = self.rov.lookup(rnode.prefix)['irr'].get(rnode.prefix, {})

            rnode.data['info']['irr'] = irr

    def add_geoloc(self):
        """Geolocate all prefixes in the table"""

        for rnode in self.rtree:

            if not 'info' in rnode.data:
                rnode.data['info'] = {}

            # find country code
            ip = rnode.prefix.partition('/')[0]
            cc = self.gc.country(ip)

            rnode.data['info']['country'] = cc

    def prefix_info(self, prefix):
        """Return the computed info (geoloc/irr) for the given prefix"""

        rnode = self.rtree.search_best(prefix)
        if rnode is None:
            return {}
        else:
            return rnode.data.get('info', {})

    def list_peers(self):
        """Return the list of 1-hop peer ASes"""

        return self.peers

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
            if prefix not in self.rtree:
                cov_prefix = self.rtree.search_best(prefix)

                if cov_prefix is None:
                    sys.stderr.write(f'Error: could not find {prefix} covering prefix')
                    continue

                rnode = self.rtree.add(prefix)
                rnode.data['as-path'] = cov_prefix.data['as-path']

    def list_aspaths(self):
        """Returns all prefixes and corresponding AS paths found in this routing
        table."""

        for node in self.rtree.nodes():
            yield node.prefix, node.data['as-path']

    def path(self, prefix):

        rnode = self.rtree.search_best(prefix)
        return rnode.prefix, rnode.data['as-path']
