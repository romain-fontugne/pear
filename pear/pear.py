import sys
from .as_graph import ASGraph
from .bgp_table import BGPTable
from .sankey_plotter import SankeyPlotter
from .prefix_weights import PrefixWeights

from rov import ROV
from pear.geolite_city import GeoliteCity

def sizeof_fmt(num, suffix=''):

    if isinstance(num, str):
        return num

    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class Pear():
    def __init__(self, ASN, weight_name):
        self.ASN = ASN
        self.weight_name = weight_name

        self.first_router = None
        self.ribs = {}
        self.flows = {}
        self.all_peers = set()

        self.rov = ROV()
        self.rov.load_databases()
        self.gc = GeoliteCity()
        self.gc.load_database()

    def load(self, prefix_fnames, bgp_fnames):
        for prefix_fname in prefix_fnames:
            router_name = prefix_fname.rpartition('/')[2].rpartition('.')[0] 
            if self.first_router is None:
                self.first_router = router_name

            # load prefix file and weights
            weights = PrefixWeights(prefix_fname, self.weight_name)
            self.flows[router_name] = weights

            # Look for the corresponding RIB file
            bgp_fname = bgp_fnames[0]
            if len(bgp_fnames) > 1:
                bgp_fname = [fname for fname in bgp_fnames if router_name in fname][0]

            # load routing data
            rib = BGPTable( self.ASN, self.rov, self.gc )
            self.ribs[router_name] = rib
            sys.stderr.write(f'Reading BGP data for {router_name}\n')
            rib.load_bgp(bgp_fname)
            sys.stderr.write('Adding selected prefixes\n')
            # Add selected prefixes if not globally rechable
            rib.add_prefixes(weights.prefixes())
            sys.stderr.write('Cleaning table\n')
            rib.clean_table(weights.prefixes())
            sys.stderr.write('Adding prefixes info\n')
            rib.add_prefix_info(weights.prefixes())

            self.all_peers.update(rib.list_peers())


    def make_graphs(self):
        sp = SankeyPlotter(self.ASN)
        for router_name, rib in self.ribs.items():
            weights = self.flows[router_name]
            # Create AS graph
            sys.stderr.write('Building AS graph\n')
            graph = ASGraph(self.ASN, rib)
            graph.build_graph(weights.prefixes())

            sys.stderr.write('Computing weights\n')
            # compute edges/nodes weights
            graph.propagate_prefix_weight(weights.dataset, hop_power=0)
            #graph.top_nodes(10, weights, rib)

            sp.add_graph(graph, rib, aliases={self.ASN: router_name})

        # Prepare AS graph plot
    # plot_fname = self.graph_filename.format(
    #     ASN=args.ASN, prefixes=args.prefixes, weight_name=args.weight_name)
    # sp.plot(plot_fname)

        return sp

    def get_rib(self, router_name):

        if router_name is None or router_name not in self.ribs:
            router_name = self.first_router

        rib = self.ribs[router_name].list_aspaths()

        return router_name, rib

    def get_traffic(self, router_name):

        traffic = {}

        if router_name is None or router_name not in self.ribs:
            router_name = self.first_router

        if router_name in self.ribs:
            rib = self.ribs[router_name]

            for prefix, vol in self.flows[router_name].raw_weights().items():
                info = rib.prefix_info(prefix)
                traffic[prefix] = {
                        'vol': sizeof_fmt(vol), 
                        'info': info
                        }

        return router_name, traffic

    def get_all_peers(self):

        peers = {}

        for asn in self.all_peers:
            peers[asn] = {
                    'name': 'UNK',
                    'vol': 0
                    }

        return peers

    def get_router_names(self):

        return list(self.ribs.keys())


