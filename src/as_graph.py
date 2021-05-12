import sys
import networkx as nx
import arrow
import pybgpstream

FILTER = "peer {}"

class ASGraph(object):
    def __init__(self, timestamp, peer_as, collector):
        """Initialize AS Graph attributes"""

        self.timestamp = arrow.get(timestamp)
        self.peer_as = int(peer_as)
        self.collector = collector
        self.graph = nx.DiGraph()


    def build_graph(self):
        """Fetch BGP data and build the AS graph"""

    
        start = self.timestamp.shift(hours=-1)
        end = self.timestamp.shift(hours=1)
        stream = pybgpstream.BGPStream(
            from_time=int(start.timestamp()), until_time=int(end.timestamp()),
            record_type="ribs", collector=self.collector,
            filter=FILTER.format(self.peer_as)
        )

        sys.stderr.write(f'\nReading BGP data:\n')
        for elem in stream:
            # Extract the prefix and origin ASN
            msg = elem.fields
            prefix = msg['prefix']

            # Add path to the graph
            prev_asn = None
            for asn in msg['as-path'].split(' '):
                if prev_asn is not None:
                    self.graph.add_edge(prev_asn, asn)

                    # Keep track of prefix on each edge
                    edge = self.graph[prev_asn, asn]
                    if 'prefixes' not in edge:
                        edge['prefixes'] = set()
                    edge['prefixes'].add(prefix)

                prev_asn = asn


    def propagate_prefix_weight(self, prefix_weight):
        """Compute edge and node weights using given prefix weights 

        prefix_weights: a dict of prefix:weights"""

        # Compute edge weights
        for _, _, data in self.graph.edges(data=True):
            data['weight'] = 0
            for prefix in data['prefixes']:
                data['weight'] += prefix_weight.get(prefix, 0)

        # Compute node weights
        for node, node_data in self.graph.nodes(data=True):
            node_data['weight'] = 0
            for _, edge_data in self.graph.in_edge(node, data=True):
                node_data['weight'] += edge_data['weight']
                


