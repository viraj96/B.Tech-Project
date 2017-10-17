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
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'spinglass', 'walktrap'])

args = parser.parse_args()

def storeFileAndPlots(fileName, plot, plotName, budget, startLine):
	plot.savefig(plotName + str(budget) + ".png")
	file = open(fileName, 'w')
	file.write(startLine)
	for result in scoresSorted:
		file.write("%s\n" % str(result))
	file.write(str(graphModularity - finalModularity) + "\n")
	file.close()
	return plot

def load_karate_club_graph():
	graph = ig.read('karate/karate.gml')
	graph.simplify()
	return graph

def fix_dendrogram(graph, cl):
    already_merged = set()
    for merge in cl.merges:
        already_merged.update(merge)

    num_dendrogram_nodes = graph.vcount() + len(cl.merges)
    not_merged_yet = sorted(set(xrange(num_dendrogram_nodes)) - already_merged)
    if len(not_merged_yet) < 2:
        return

    v1, v2 = not_merged_yet[:2]
    cl._merges.append((v1, v2))
    del not_merged_yet[:2]

    missing_nodes = xrange(num_dendrogram_nodes,
            num_dendrogram_nodes + len(not_merged_yet))
    cl._merges.extend(izip(not_merged_yet, missing_nodes))
    cl._nmerges = graph.vcount()-1

totalTimeStart = datetime.datetime.now()
print("\nStarting code...\n")

graph = load_karate_club_graph()

def returnPartition(graph, algo):
	if( algo == 'louvain' ):
		graphPartition = louvain.find_partition(graph, method = 'Modularity')
		return graphPartition
	elif( algo == 'edge_betweenness' ):
		dendrogram = graph.community_edge_betweenness(directed = False)
		graphPartition = dendrogram.as_clustering()
		return graphPartition
	elif( algo == 'fast_greedy' ):
		dendrogram = graph.community_fastgreedy()
		graphPartition = dendrogram.as_clustering()
		return graphPartition
	elif( algo == 'infomap' ):
		graphPartition = graph.community_infomap()
		return graphPartition
	elif( algo == 'label_propagation' ):
		graphPartition = graph.community_label_propagation()
		return graphPartition
	elif( algo == 'leading_eigenvector' ):
		graphPartition = graph.community_leading_eigenvector()
		return graphPartition
	elif( algo == 'multilevel' ):
		graphPartition = graph.community_multilevel()
		return graphPartition
	elif( algo == 'spinglass' ):
		graphPartition = graph.community_spinglass()
		return graphPartition
	elif( algo == 'walktrap' ):
		dendrogram = graph.community_walktrap()
		graphPartition = dendrogram.as_clustering()
		return graphPartition

graphPartition = returnPartition(graph, args.algo[0])
plt = ig.plot(graphPartition, "Results/Plots/karate_club_graph_" + args.algo[0] + ".png", mark_groups = True)

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