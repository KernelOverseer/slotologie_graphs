import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import sys
from flask import Flask, request

app = Flask(__name__)

def load_page(name):
    with open(name) as filehandler:
        content = filehandler.read()
        filehandler.close()
        return (content)
    return '404'

print ('in flask server')

@app.route("/")
def home():
    return load_page('index.html')
@app.route("/login")
def get_user():
    try:
        name = request.args.get('login')
    except:
        return "ach kadir ahia"
    print ('=' * 100, "someone is looking for name : " + name , '=' * 100)
    try:
        file_handler = open(name + '.svg', 'rb')
        return file_handler.read()
    except:
        try:
            get_graph(name)
            file_handler = open(name + '.svg', 'rb')
            return file_handler.read()
        except:
            return "makaynch"
def get_graph(username):
    data = pd.read_csv('result_800.csv')
    G = nx.Graph()
    k = 0
    for j in data[username]:
        if j != 0:
            G.add_edge(username, data['logins'][k], weight=j)
        k += 1
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=10)
    e1 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 1]
    e2 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 2]
    e3 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 3]
    e4 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 4]
    e5 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 5]
    e6 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 6]
    e7 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 7]
    e8 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 8]
    e9 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 9]
    e10 = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] >= 10]
    nx.draw_networkx_edges(G, pos, edgelist=e1,
                                   width=0.2, alpha=0.1, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e2,
                                   width=0.4, alpha=0.2, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e3,
                                   width=0.6, alpha=0.3, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e4,
                                   width=0.8, alpha=0.4, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e5,
                                   width=1, alpha=0.5, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e6,
                                   width=1.2, alpha=0.6, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e7,
                                   width=1.4, alpha=0.7, edge_color='b')
    nx.draw_networkx_edges(G, pos, edgelist=e8,
                                   width=1.6, alpha=0.8, edge_color='r')
    nx.draw_networkx_edges(G, pos, edgelist=e9,
                                   width=1.8, alpha=0.9, edge_color='r')
    nx.draw_networkx_edges(G, pos, edgelist=e10,
                                   width=2, alpha=1, edge_color='r')
    nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')
    plt.axis('off')
    plt.savefig(username + '.svg')
    plt.close()
    return (1)

if __name__ == "__main__":
    app.run(debug=True, host="e1r3p7.1337.ma", port=3000)
