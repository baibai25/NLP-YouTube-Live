import matplotlib.pyplot as plt
import networkx as nx
import graphviz

# ref. https://www.dskomei.com/entry/2019/04/07/021028
def plot_network(data, edge_threshold, random_state):

    plt.figure(figsize=(15, 15), facecolor='white')
    G = nx.Graph()
    
    # node
    nodes = list(set(data['word1'].tolist() + data['word2'].tolist()))
    G.add_nodes_from(nodes)
    
    # edge
    for i in range(len(data)):
        row_data = data.iloc[i]
        if row_data['jaccard_coefficient'] > edge_threshold:
            G.add_edge(row_data['word1'], row_data['word2'], weight=row_data['jaccard_coefficient'])

    # remove independent nodes
    isolated = [n for n in G.nodes if len([i for i in nx.all_neighbors(G, n)]) == 0]
    for n in isolated:
        G.remove_node(n)
        
    # adjust layout
    #pos = nx.spring_layout(G, k=0.3, seed=42)
    pos = nx.nx_agraph.graphviz_layout(
        G,
        prog='neato',
        args='-Goverlap="scalexy" -Gsep="+6" -Gnodesep=0.8 -Gsplines="polyline" -GpackMode="graph" -Gstart={}'.format(random_state)
    )
    
    pr = nx.pagerank(G)
    nx.draw_networkx_nodes(G, pos, node_color=list(pr.values()), cmap=plt.cm.Reds, alpha=0.7, node_size=[60000*v for v in pr.values()])
    edge_width = [d['weight'] * 100 for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='darkgrey', width=edge_width)
    nx.draw_networkx_labels(G, pos, fontsize=14, font_family='Noto Sans CJK JP', font_weight='bold')
    
    plt.axis('off')
    plt.savefig('./collocation_network.png', dpi=100)
    plt.show()
