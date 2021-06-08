import networkx as nx
import plotly.graph_objects as go

OWN_AS, DIRECT_PEER, OTHER_COLOR = "gray", "green", "blue"

def sizeof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class SankeyPlotter(object):
    def __init__(self, asn: int) -> None:
        self.main_as = str(asn)

    def plot(self, graph, bgp_table, fname):
        """Fetch BGP data and build the AS graph"""
        # Plot graph
        # Prepare Data
        #graph.normalize_weights()
        #graph.trim(0)
        G = graph.graph.copy()

        colors = {}
        colors[str(self.main_as)] = OWN_AS
        for peer in bgp_table.list_peers():
            colors[peer] = DIRECT_PEER

        # Prepare data for sankey plot
        direct_peers = bgp_table.list_peers()
        nodes_list = ['AS'+node for node in G.nodes()]
        nodes_color = [ colors[node] if node in colors else OTHER_COLOR
                for node in G.nodes() ]
        sources = []
        targets = []
        values = []
        link_data = []
        for n0, n1, data in G.edges(data=True):
            sources.append(nodes_list.index('AS'+n0))
            targets.append(nodes_list.index('AS'+n1))
            values.append(data['weight'])
            link_data.append(
                    f'Total: {sizeof_fmt(data["weight"])} <br />' +
                    '<br />'.join([f'{prefix}: {info}' 
                        for prefix, info in data['prefix_info'].items()]
                        ))

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad = 15,
                label = nodes_list,
                color = nodes_color
            ),
            link= dict(
                source = sources,
                target = targets,
                value = values,
                customdata = link_data,
                hovertemplate= 'Total: %{value} <br />%{customdata}<extra></extra>',
            ))])
        
        fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        fig.write_html(fname)

