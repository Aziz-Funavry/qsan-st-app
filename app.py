import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from igraph import Graph

def load_file(uploaded_file):
    """Load the uploaded file as a DataFrame."""
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    return df

def display_dataframe_preview(df):
    """Display a preview of the DataFrame."""
    st.write("Preview of the DataFrame:")
    st.write(df)

def display_selected_columns(df, selected_columns):
    """Display the selected columns from the DataFrame."""
    st.write("You selected the following columns:")
    st.write(selected_columns)

    # Display the preview of selected columns
    st.write("Preview of selected columns:")
    st.write(df[selected_columns])

def generate_network_plot(cor_matrix):
    # Create a directed graph from the correlation matrix
    G = nx.DiGraph()
    nodes = list(cor_matrix.columns)
    G.add_nodes_from(nodes)
    
    threshold = 0.2  # Adjust the threshold as needed
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if abs(cor_matrix.iloc[i, j]) > threshold:
                G.add_edge(nodes[i], nodes[j])

    # Position nodes using a spring layout
    pos = nx.spring_layout(G)

    # Create a Plotly figure for network visualization
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G.nodes()),
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Color node points by the number of connections.
    node_colors = [len(adjacencies[1]) for node, adjacencies in enumerate(G.adjacency())]
    node_trace.marker.color = node_colors

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Network Plot',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Network visualization",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)]))
    
    st.plotly_chart(fig, use_container_width=True)

# New function to visualize network using igraph (translated from R to Python)
def visualize_network_with_igraph(cor_matrix):
    nodes = list(cor_matrix.columns)
    edges = [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range(i + 1, len(nodes)) if abs(cor_matrix.iloc[i, j]) > 0.2]

    g = Graph.TupleList(edges, directed=True, weights=True)

    # Set the layout
    layout = g.layout_auto()

    # Plot using igraph
    ig_plot = go.Figure(go.Scatter(x=[layout[i][0] for i in range(len(layout))],
                                   y=[layout[i][1] for i in range(len(layout))],
                                   mode='markers+text',
                                   text=nodes,
                                   hoverinfo='text',
                                   marker=dict(size=10, color='blue')
                                   ))
    for edge in edges:
        src, tgt = edge
        src_index = nodes.index(src)
        tgt_index = nodes.index(tgt)
        ig_plot.add_trace(
            go.Scatter(x=[layout[src_index][0], layout[tgt_index][0]],
                       y=[layout[src_index][1], layout[tgt_index][1]],
                       mode='lines',
                       line=dict(width=1, color='gray')
                       ))
    ig_plot.update_layout(title='Network Plot (igraph)',
                          titlefont_size=16,
                          showlegend=False,
                          hovermode='closest',
                          margin=dict(b=20, l=5, r=5, t=40),
                          annotations=[dict(
                              text="Network visualization using igraph",
                              showarrow=False,
                              xref="paper", yref="paper",
                              x=0.005, y=-0.002)])
    st.plotly_chart(ig_plot, use_container_width=True)

def main():
    st.title("Network Visualizer")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.info("File successfully uploaded!")

        # Load the uploaded file as a DataFrame
        df = load_file(uploaded_file)
        display_dataframe_preview(df)

        # Allow users to select columns
        selected_columns = st.multiselect("Select columns", df.columns)

        if selected_columns:
            display_selected_columns(df, selected_columns)

        st.header('Network Visualization using NetworkX:')
        cor_matrix = df[selected_columns].corr()
        generate_network_plot(cor_matrix)

        st.header('Network Visualization using igraph:')
        visualize_network_with_igraph(cor_matrix)


if __name__ == "__main__":
    main()
