from collections import defaultdict
import networkx as nx
import json
import plotly
from plotly.utils import PlotlyJSONEncoder
from plotly.graph_objects import Figure, Sankey

from .as_name import ASName

OWN_AS, DIRECT_PEER, OTHER_COLOR = "gray", "green", "blue"

def sizeof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class SankeyPlotter(object):
    def __init__(self, asn: int, as_name: ASName, pad=50) -> None:
        self.main_as = str(asn)
        self.as_name = as_name
        self.pad = pad
        self.traces = {'all': self.new_trace(visible=True)}

        self.colors = defaultdict(lambda: OTHER_COLOR)

        self.minimum_traffic = 0

    def new_trace(self, visible=False):
        "Returns a new empty sankey trace"

        return {
                'visible': visible,
                'node': {
                    'pad': self.pad,
                    'label': [],
                    'color': [],
                    'customdata': [],
                    'hovertemplate': '%{label}<br />%{customdata} <br />%{value}<extra></extra>',
                    },
                'link': {
                    'source': [],
                    'target': [],
                    'value':[],
                    'customdata': [],
                    'hovertemplate': 'Total: %{value} <br />%{customdata}<extra></extra>',
                    },
                'node_idx': {},
                'stats':{
                    'node':{
                        'in':defaultdict(float),
                        'out':defaultdict(float)
                        }
                    }
                }

    def graph2trace(self, G, trace):

        ## Add nodes to the sankey
        for node in G.nodes():
            if node not in trace['node_idx']:
                trace['node_idx'][node] = len(trace['node']['label'])
                trace['node']['label'].append(node)
                trace['node']['customdata'].append(self.as_name.name(node))
                trace['node']['color'].append(self.colors[node])

        ## Add links to the sankey
        for n0, n1, data in G.edges(data=True):
            trace['link']['source'].append(trace['node_idx'][n0])
            trace['link']['target'].append(trace['node_idx'][n1])
            trace['link']['value'].append(data['weight'])
            trace['link']['customdata'].append(
                    f'Total: {sizeof_fmt(data["weight"])} <br />' +
                    '<br />'.join([f'{prefix}: {info}' 
                        for prefix, info in data['prefix_info'].items()]
                        ))

            trace['stats']['node']['out'][n0] += data['weight']
            trace['stats']['node']['in'][n1] += data['weight']


    def add_graph(self, graph, bgp_table, aliases={}):
        """Fetch BGP data and build the AS graph"""
        # Prepare Data
        G = graph.graph.copy()
        node_aliases = {str(label): str(new_label) for label, new_label in aliases.items()}

        # Remove 'small' nodes
        #to_remove = []
        #for node, data in G.nodes(data=True):
        #    if ( ( data['weight'] is None or data['weight'] < minimum_traffic ) 
        #    and node != self.main_as):
        #        to_remove.append(node)

        #G.remove_nodes_from(to_remove)

        # Set node colors
        self.colors['AS'+self.main_as] = OWN_AS
        if self.main_as in node_aliases:
            self.colors[node_aliases[self.main_as]] = OWN_AS

        for peer in bgp_table.list_peers():
            self.colors['AS'+peer] = DIRECT_PEER

        # Prepare data for sankey plot:
        ## rename nodes
        nodes_name = {
                node:'AS'+node if not node in node_aliases else node_aliases[node] 
                for node in G.nodes()
                }
        G = nx.relabel_nodes(G, nodes_name)

        # Create a new trace for this graph
        if self.main_as in node_aliases:
            unique_trace = self.new_trace()
            self.graph2trace(G, unique_trace)
            self.traces[ node_aliases[self.main_as] ] = unique_trace

        self.graph2trace(G, self.traces['all'])


    def plot(self, minimum_traffic):

        self.minimum_traffic = minimum_traffic
        data = []
        buttons = []
        # Add each trace to the figure and dropdown menu
        for i, (trace_name, trace) in enumerate( self.traces.items() ):
            # find prominent nodes (in terms of given min traffic)
            selected_nodes = set()
            for node_idx, node in enumerate( trace['node']['label'] ):
                if( trace['stats']['node']['in'][node] > minimum_traffic 
                    or trace['stats']['node']['out'][node] > minimum_traffic):
                    selected_nodes.add(node_idx)

            # select links for prominent nodes
            selected_link = self.new_trace()['link']
            for j, (source, target) in enumerate( zip(trace['link']['source'], trace['link']['target'])):
                if source in selected_nodes and target in selected_nodes:
                    selected_link['target'].append(target)
                    selected_link['source'].append(source)
                    selected_link['value'].append(trace['link']['value'][j])
                    selected_link['customdata'].append(trace['link']['customdata'][j])


            data.append( Sankey(
                node=trace['node'], 
                link=selected_link, 
                visible=trace['visible']
                )
            )
            visibility_mask = [False]*len(self.traces)
            visibility_mask[i] = True
            buttons.append(
                {
                'label': trace_name,
                'method': 'update',
                'args': [{'visible': visibility_mask}]
                })


        self.fig = Figure(data=data)
        # add dropdown menu
        self.fig.update_layout( updatemenus=[ 
            dict(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
                ) ] )
        

    def to_json(self):
        return json.dumps(self.fig, cls=PlotlyJSONEncoder)

