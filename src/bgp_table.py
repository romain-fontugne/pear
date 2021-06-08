import arrow
import pybgpstream
import radix
import sys

FILTER = "peer {}"

class BGPTable(object):
    def __init__(self, peer_as):
        """Initialize BGP Table attributes"""

        self.peer_as = peer_as
        self.rtree = radix.Radix()
        self.peers = set()


    def add_bgp(self, timestamp, collector):
        """Fetch BGP data and add AS paths to the radix tree"""
    
        ts = arrow.get(timestamp)
        start = ts.shift(hours=-1)
        end = ts.shift(hours=1)
        stream = pybgpstream.BGPStream(
            from_time=int(start.timestamp()), until_time=int(end.timestamp()),
            record_type="ribs", collector=collector,
            filter=FILTER.format(self.peer_as)
        )

        for elem in stream:
            # Extract the prefix and origin ASN
            msg = elem.fields
            prefix = msg['prefix']

            # Add path to the tree
            rnode = self.rtree.add(prefix)
            aspath = self.clean_aspath(msg['as-path'])
            rnode.data['as-path'] = aspath 
            ases = aspath.split(' ')
            if len(ases) > 1:
                self.peers.add(ases[1])

    def list_peers(self):
        """Return the list of 1-hop peer ASes"""

        return self.peers

    def clean_aspath(self, aspath):
        """Remove path prepending and duplicate ASes"""
        
        cleaned = []

        for asn in aspath.split(" "):
            if asn not in cleaned:
                cleaned.append(asn)
            
        return " ".join(cleaned)

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
