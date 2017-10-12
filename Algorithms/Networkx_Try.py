import networkx as nx
import community
import matplotlib.pyplot as plt

G = nx.Graph()

nodes = []
for i in range(5000):
	nodes.append(i+1)

G.add_nodes_from(nodes)

edgeList = []
for line in open("./../Binary_Networks/network.dat", 'r'):
	a = line.split()
	edgeList.append((int(a[0]), int(a[1])))

G.add_edges_from(edgeList)

values = list(nx.k_clique_communities(G, 3))

print(values)
print
print(len(values))
