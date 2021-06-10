from as_graph import ASGraph
from bgp_table_mrt import BGPTable
#from graph_plotter import GraphPlotter
from sankey_plotter import SankeyPlotter
from prefix_weights import PrefixWeights
import sys
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('ASN', type=int,
                        help='ASN of the network manageed by the user')
    #parser.add_argument('-c', '--route_collector', type=str, default='rrc06',
            #help="BGP route collector that peers with given ASN"),
    parser.add_argument('-b', '--bgp_data', type=str, 
            help="MRT file containing a RIB for monitored prefixes"),
    parser.add_argument('-p', '--prefixes', type=str, 
            help="CSV file with a list of selected prefixes and optional weights"),
    parser.add_argument('-w', '--weight_name', type=str, default='avg_bps',
            help="Name of the column in the csv file used for prefix weights"),
    parser.add_argument('-g', '--graph_filename', type=str, default='interactive_graph_AS{ASN}_{weight_name}.html',
            help="File name for the ploted AS graph"),
    args = parser.parse_args()

    
    # load prefix file and weights
    weights = PrefixWeights(args.prefixes, args.weight_name)

    bgp_table = BGPTable(args.bgp_data, args.ASN)
    sys.stderr.write('Reading BGP data\n')
    bgp_table.load_bgp()
    sys.stderr.write('Adding selected prefixes\n')

    # Add selected prefixes if not globally rechable
    if args.prefixes is not None:
        bgp_table.add_prefixes(weights.prefixes())


    sys.stderr.write('Building AS graph\n')
    graph = ASGraph(args.ASN, bgp_table)
    graph.build_graph(weights.prefixes())

    sys.stderr.write('Computing weights\n')
    # compute edges/nodes weights
    graph.propagate_prefix_weight(weights.dataset, hop_power=0)

    graph.top_nodes(10, weights, bgp_table)

    plot_fname = args.graph_filename.format(
        ASN=args.ASN, prefixes=args.prefixes, weight_name=args.weight_name)
    sys.stderr.write('Ploting AS Graph\n')
    #gp = GraphPlotter(args.ASN)
    #gp.plot(graph, plot_fname)
    sp = SankeyPlotter(args.ASN)
    sp.plot(graph, bgp_table, plot_fname)
    
