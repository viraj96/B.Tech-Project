import argparse
import datetime
import operator
import community
import numpy as np
import networkx as nx
import matplotlib.pyplot as plot
from itertools import permutations, combinations

parser = argparse.ArgumentParser(description = 'Generate exhaustive answer to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation)')

args = parser.parse_args()

def community_layout(graph, partition):
	position_communities = _position_communities(graph, partition, scale = 3.)
	position_nodes = _position_nodes(graph, partition, scale = 1.)
	position = dict()
	for node in graph.nodes():
		position[node] = position_communities[node] + position_nodes[node]
	return position

def _position_communities(graph, partition, **kwargs):
	between_community_edges = _find_between_community_edges(graph, partition)
	communities = set(partition.values())
	hypergraph = nx.DiGraph()
	hypergraph.add_nodes_from(communities)
	for (ci, cj), edges in between_community_edges.items():
		hypergraph.add_edge(ci, cj, weight = len(edges))
	position_communities = nx.spring_layout(hypergraph, **kwargs)
	position = dict()
	for node, community in partition.items():
		position[node] = position_communities[community]
	return position

def _find_between_community_edges(graph, partition):
	edges = dict()
	for (ni, nj) in graph.edges():
		ci = partition[ni]
		cj = partition[nj]
		if( ci != cj ):
			try:
				edges[(ci, cj)] += [(ni, nj)]
			except KeyError:
				edges[(ci, cj)] = [(ni, nj)]
	return edges

def _position_nodes(graph, partition, **kwargs):
	communities = dict()
	for node, community in partition.items():
		try:
			communities[community] += [node]
		except KeyError:
			communities[community] = [node]
	position = dict()
	for ci, nodes in communities.items():
		subgraph = graph.subgraph(nodes)
		position_subgraph = nx.spring_layout(subgraph, **kwargs)
		position.update(position_subgraph)
	return position

totalTimeStart = datetime.datetime.now()
print("\nStarting code...\n")

graph = nx.karate_club_graph()
graphPartition = community.community_louvain.best_partition(graph)
position = community_layout(graph, graphPartition)
nx.draw(graph, position, node_color = graphPartition.values(), with_labels = True)
plot.savefig("Results/Plots/karate_club_graph.png")
plot.show()

graphModularity = community.modularity(graphPartition, graph)

if( args.budget ):
	budget = args.budget
else:
	budget = 5

totalNodes = len(graph.nodes())
nodesList = np.arange(totalNodes)
tryAll = []

print("\nStarting combinations code...\n")

combinationsStart = datetime.datetime.now()
for val in combinations(nodesList, budget):
	allPerms = list(permutations(val))
	for perm in allPerms:
		tryAll.append(perm)
tryAll = np.array(tryAll)
print("Length of combinations = {0}\n").format(len(tryAll))
combinationsEnd = datetime.datetime.now()

print("\nCombinations Time = {0} seconds\n").format(combinationsEnd - combinationsStart)

modularityScores = []

print("\nCalculating modularity scores...\n")

bottleneckStart = datetime.datetime.now()
for idx, selection in enumerate(tryAll):
	if( idx % 10000 == 0 and idx != 0 ):
		print("{0} combinations done!!").format(idx + 1)
	tempGraph = graph.copy()
	tempGraph.remove_nodes_from(selection)
	partition = community.community_louvain.best_partition(tempGraph)
	modularityScores.append(graphModularity - community.modularity(partition, tempGraph))
bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format(bottleneckEnd - bottleneckStart)

print("\nCompiling results...\n")

tupledTryAll = []
for element in tryAll:
	tupledTryAll.append(tuple(element))

modularityScores = np.array(modularityScores)
scores = dict(zip(tupledTryAll, modularityScores))
scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
bestNodes = np.array(scoresSorted[0][0])
bestGraph = graph.copy()
bestGraph.remove_nodes_from(bestNodes)
bestGraphPartition = community.best_partition(bestGraph)
bestPosition = community_layout(bestGraph, bestGraphPartition)
nx.draw(bestGraph, bestPosition, node_color = bestGraphPartition.values(), with_labels = True)
plot.savefig("Results/Plots/karate_club_graph_exhaustive_" + str(budget) + ".png")
plot.show()

exhaustiveFile = open("Results/Data/exhaustiveResults" + str(budget) + ".dat", 'w')
exhaustiveFile.write("<------------------Final Exhaustive Scores------------------>\n")
for result in scoresSorted:
	exhaustiveFile.write("%s\n" % str(result))
exhaustiveFile.close()

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format(totalTimeEnd - totalTimeStart)