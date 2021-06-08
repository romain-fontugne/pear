import sys
import networkx as nx
import arrow
import pybgpstream
from ihr.rov import ROV
from geolite_city import GeoliteCity

def sizeof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class ASGraph(object):
    def __init__(self, peer_as) :
        """Initialize AS Graph attributes"""

        self.peer_as = int(peer_as)
        self.graph = nx.DiGraph()
        self.max_weight = 1

        self.rov = ROV()
        self.rov.load_databases()

        self.gc = GeoliteCity()
        self.gc.load_database()


    def build_graph(self, bgp_table, prefixes=None):
        """Fetch BGP data and build the AS graph. 
        If a list of prefix is given, the graph represents only these prefixes"""

        if prefixes is None:
            paths = bgp_table.list_aspahts()
        else:
            paths = map(bgp_table.path, prefixes)

        for prefix, aspath in paths:
            # Add path to the graph
            asns = aspath.split(' ')
            prev_asn = asns[0]
            for distance, asn in enumerate(asns[1:]):
                self.graph.add_edge(prev_asn, asn)

                # Keep track of prefix on each edge
                edge = self.graph.edges[prev_asn, asn]
                if 'prefixes' not in edge:
                    edge['prefixes'] = {}
                edge['prefixes'][prefix] = distance

                prev_asn = asn

    def propagate_prefix_weight(self, prefix_weight, hop_power=1):
        """Compute edge and node weights using given prefix weights.
        This method assumes that given prefixes are already in the graph.

        prefix_weights: a dataframe with at least a 'prefix' and '__weights__'
        column or None for equal weights for all prefixes."""

        # Compute edge weights
        for _, _, data in self.graph.edges(data=True):
                # edges not seen for selected prefixes will be removed by trim
                data['weight'] = None 
                for p0, distance in data['prefixes'].items():
                    if prefix_weight is None:
                        p0_weights = [1]
                    else:
                        p0_weights = prefix_weight[prefix_weight['prefix'] == p0]['__weights__'].values
                    for p0_weight in p0_weights:
                        if data['weight'] is None:
                            data['weight'] = 0
                            data['prefix_info'] = {}
                        data['weight'] += p0_weight*(distance**hop_power)

                        # get more info
                        irr = self.rov.lookup(p0)['irr'].get(p0, {})
                        ip = p0.partition('/')[0]
                        cc = self.gc.lookup(ip).country.iso_code
                        data['prefix_info'][p0] = f'{sizeof_fmt(p0_weight)}, {cc}, {irr.get("descr","-")}'#({info["delegated"].get("country")})'

        # Compute node weights
        for node, node_data in self.graph.nodes(data=True):
            # node not seen for selected prefixes have a negative weight
            node_data['weight'] = None 
            for _, _, edge_data in self.graph.in_edges(node, data=True):
                if edge_data['weight'] is not None:
                    if node_data['weight'] is None:
                        node_data['weight'] = 0
                    node_data['weight'] += edge_data['weight']

                    if node_data['weight'] > self.max_weight:
                        self.max_weight = node_data['weight']


    def normalize_weights(self, upper_limit_node=10, upper_limit_edge=10, base_node=10, base_edge=10):
        """Normalize edges and nodes weight to values between 0 and upper_limit"""

        # Normalize nodes' weight
        for node, data in self.graph.nodes(data=True):
            if data['weight'] is not None:
                data['weight'] = base_node+(data['weight']*upper_limit_node)/self.max_weight

        for _, _, data in self.graph.edges(data=True):
            if data['weight'] is not None:
                data['weight'] = base_edge+(data['weight']*upper_limit_edge)/self.max_weight

    def trim(self, min_weight):
        """Remove node and edges with a weight less than 'min_weight'"""

        edge_to_remove = []
        for n0, n1, data in self.graph.edges(data=True):
            if data['weight'] is None or data['weight'] < min_weight:
                edge_to_remove.append( (n0,n1) )

        self.graph.remove_edges_from( edge_to_remove )

        node_to_remove = []
        for node, data in self.graph.nodes(data=True):
            if node == str(self.peer_as):
                continue

            if data['weight'] is None or data['weight'] < min_weight: 
                node_to_remove.append(node)

        self.graph.remove_nodes_from(node_to_remove)

    def top_nodes(self, n, prefix_weights=None, bgp_table=None, hop_power=1):
        """Return the list of top nodes with the highest weights"""

        df_weight = prefix_weights.dataset
        weights = {prefix:data['weight'] 
                for prefix, data in self.graph.nodes(data=True)
                if data['weight'] is not None}

        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)

        for top_asn, weight in sorted_weights[:n]:
            print(f'AS{top_asn}:')
            if prefix_weights is not None and bgp_table is not None:

                computed_weights = []
                for peer_asn, _, data in self.graph.in_edges(top_asn, data=True):
                    # edges not seen for selected prefixes will be removed by trim
                    for p0, distance in data['prefixes'].items():
                        p0_df = df_weight[df_weight['prefix'] == p0]
                        computed_weights.append( {
                            'peer_asn': peer_asn, 
                            'as_path': bgp_table.path(p0),
                            'prefix': p0,
                            'weight': sum([w*(distance**hop_power) for w in p0_df['__weights__'].values]),
                            'init_val': p0_df[prefix_weights.weight_column].values.tolist()
                            })

                sorted_prefix_weights = sorted(computed_weights, key=lambda x: x['weight'], reverse=True)

                # print top 3 prefixes
                for top_prefix in sorted_prefix_weights[:3]:
                    if top_prefix['weight']>0:
                        print(f"\t{top_prefix['as_path']}: {top_prefix['init_val']}")

