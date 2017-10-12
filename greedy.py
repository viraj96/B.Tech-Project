import argparse
import datetime
import operator
import community
import numpy as np
import networkx as nx
import matplotlib.pyplot as plot
from itertools import permutations, combinations

parser = argparse.ArgumentParser(description = 'Generate greedy answer based to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation)')
parser.add_argument('--metric', type = str, nargs = '+', help = 'Metric to be used for greedy approach. Choices are degree, clustering coefficient and local modularity', choices = ['degree', 'clusteringCoeff', 'localMod', 'squareCluster', 'degreeCenter', 'betweenCenter', 'eigenCenter', 'closeVital'])

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

def storeFileAndPlots(fileName, plot, plotName, budget, startLine):
	plot.savefig(plotName + str(budget) + ".png")
	file = open(fileName, 'w')
	file.write(startLine)
	for result in scoresSorted:
		file.write("%s\n" % str(result))
	file.write(str(graphModularity - finalModularity) + "\n")
	file.close()
	return plot

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
modularityScores = []

print("\nCalculating modularity scores...\n")

bottleneckStart = datetime.datetime.now()
tempGraph = graph.copy()
for i in range(budget):
	bestNode = -1
	if( args.metric[0] == 'degree' ):
		bestNode = sorted(tempGraph.degree_iter(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'clusteringCoeff' ): # <- next best result
		bestNode = sorted(nx.clustering(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'localMod' ):
		print("Local Modularity")
	elif( args.metric[0] == 'squareCluster' ):
		bestNode = sorted(nx.square_clustering(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'degreeCenter' ):
		bestNode = sorted(nx.degree_centrality(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'betweenCenter' ):
		bestNode = sorted(nx.betweenness_centrality(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'eigenCenter' ):
		bestNode = sorted(nx.eigenvector_centrality(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	elif( args.metric[0] == 'closeVital' ): # Closeness vitality of a node is the change in the sum of distances between all node pairs when excluding that node. <- best result
		bestNode = sorted(nx.closeness_vitality(tempGraph).items(), key = operator.itemgetter(1), reverse = True)[0][0]
	tryAll.append(bestNode)
	tempGraph.remove_node(bestNode)
	partition = community.community_louvain.best_partition(tempGraph)
	modularityScores.append(graphModularity - community.modularity(partition, tempGraph))
bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format((bottleneckEnd - bottleneckStart))

print("\nCompiling results...\n")

tryAll = np.array(tryAll)
modularityScores = np.array(modularityScores)
scores = dict(zip(tryAll, modularityScores))
scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
bestNodes = np.array([x[0] for x in scoresSorted])
bestGraph = graph.copy()
bestGraph.remove_nodes_from(bestNodes)
bestGraphPartition = community.best_partition(bestGraph)
finalModularity = community.modularity(bestGraphPartition, bestGraph)
bestPosition = community_layout(bestGraph, bestGraphPartition)
nx.draw(bestGraph, bestPosition, node_color = bestGraphPartition.values(), with_labels = True)
if( args.metric[0] == 'degree' ):
	storeFileAndPlots("Results/Data/greedyDegreeResults.dat", plot, "Results/Plots/karate_club_graph_degree_", budget, "<------------------Final Greedy Degree Based Scores------------------>\n")
elif( args.metric[0] == 'clusteringCoeff' ):
	storeFileAndPlots("Results/Data/clusteringCoefficientResults.dat", plot, "Results/Plots/karate_club_graph_clusteringCoeff_", budget, "<------------------Final Greedy Clustering Coefficient Based Scores------------------>\n")
elif( args.metric[0] == 'squareCluster' ):
	storeFileAndPlots("Results/Data/squareClusteringResults.dat", plot, "Results/Plots/karate_club_graph_squareCluster_", budget, "<------------------Final Greedy Square Clustering Based Scores------------------>\n")
elif( args.metric[0] == 'degreeCenter' ):
	storeFileAndPlots("Results/Data/degreeCentralityResults.dat", plot, "Results/Plots/karate_club_graph_degreeCenter_", budget, "<------------------Final Greedy Degree Centrality Based Scores------------------>\n")
elif( args.metric[0] == 'betweenCenter' ):
	storeFileAndPlots("Results/Data/betweennessCentralityResults.dat", plot, "Results/Plots/karate_club_graph_betweenCenter_", budget, "<------------------Final Greedy Betweenness Centrality Based Scores------------------>\n")
elif( args.metric[0] == 'eigenCenter' ):
	storeFileAndPlots("Results/Data/eigenvectorCentralityResults.dat", plot, "Results/Plots/karate_club_graph_eigenCenter_", budget, "<------------------Final Greedy Eigenvector Centrality Based Scores------------------>\n")
elif( args.metric[0] == 'closeVital' ):
	storeFileAndPlots("Results/Data/closenessVitalityResults.dat", plot, "Results/Plots/karate_club_graph_closeVital_", budget, "<------------------Final Greedy Closeness Vitality Based Scores------------------>\n")
plot.show()
totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format((totalTimeEnd - totalTimeStart))