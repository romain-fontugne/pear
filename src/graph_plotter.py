import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool, LabelSet, ColumnDataSource,
                          MultiLine, Plot, Range1d, ResetTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

DIRECT_PEER, OTHER_COLOR = "black", "red"

class GraphPlotter(object):
    def __init__(self, asn: int) -> None:
        self.main_as = str(asn)

    def plot(self, graph, fname):
        """Fetch BGP data and build the AS graph"""
        # Plot graph
        # Prepare Data
        graph.normalize_weights()
        graph.trim(0)
        G = graph.graph.copy()


        for start_node, end_node, data in G.edges(data=True):
            data['edge_color'] = DIRECT_PEER if start_node == self.main_as else OTHER_COLOR

        # Show with Bokeh
        plot = Plot(plot_width=1024, plot_height=1024,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = f"AS Graph for AS{self.main_as}"
        
        node_hover_tool = HoverTool(tooltips=[("AS", "@index"), ("weight", "@weight")])
        plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

        graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

        graph_renderer.node_renderer.glyph = Circle(size="weight", fill_color=Spectral4[0], )
        graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, 
                line_width="weight")
        plot.renderers.append(graph_renderer)

        # Add node labels
        x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
        node_labels = [f'AS{node}' for node in G.nodes()]
        source = ColumnDataSource({'x': x, 'y': y,
                                'ASN': [node_labels[i] for i in range(len(x))]})
        labels = LabelSet(x='x', y='y', text='ASN', source=source,)
        plot.renderers.append(labels)

        output_file(fname)
        show(plot)

