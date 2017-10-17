import louvain
import argparse
import datetime
import operator
import community
import numpy as np
import igraph as ig
import networkx as nx
import matplotlib.pyplot as plot
from itertools import permutations, combinations, izip

parser = argparse.ArgumentParser(description = 'Generate exhaustive answer to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation).')
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'spinglass', 'walktrap'])

args = parser.parse_args()

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
plt = ig.plot(graphPartition, "Results/Plots/karate_club_graph_" + args.algo[0] + ".png", mark_groups = True, vertex_label = [i for i in range(graph.vcount())])

if( args.value[0] == 'modularity' ):
	graphModularity = graph.modularity(graphPartition)

if( args.budget ):
	budget = args.budget
else:
	budget = 5

totalNodes = graph.vcount()
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

valueScores = []

print("\nCalculating modularity scores...\n")

def returnScore(graph, tempGraph, graphPartition, partition, value):
	if( value == 'modularity' ):
		graphModularity = graph.modularity(graphPartition)
		return graphModularity - tempGraph.modularity(partition)
	elif( value == 'nmi' ):
		maxValue = -10000
		for i in range(len(graphPartition)):
			for j in range(len(partition)):
				print
				print(len(graphPartition[i]))
				print(len(partition[j]))
				print(graphPartition[i])
				print(partition[j])
				exit()
				# consider = ig.compare_communities(graphPartition[i], partition[j], method = 'nmi', remove_none = False)
				# if( consider >= maxValue ):
				# 	maxValue = consider
		exit()
		return maxValue # <- can be done with mean calculation as well?

bottleneckStart = datetime.datetime.now()
for idx, selection in enumerate(tryAll):
	if( idx % 10000 == 0 and idx != 0 ):
		print("{0} combinations done!!").format(idx + 1)
	tempGraph = graph.copy()
	tempGraph.delete_vertices(selection)
	if( args.algo[0] == 'louvain' ):
		partition = louvain.find_partition(tempGraph, method = 'Modularity')
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'edge_betweenness' ):
		dendrogram = tempGraph.community_edge_betweenness(directed = False)
		fix_dendrogram(tempGraph, dendrogram)
		partition = dendrogram.as_clustering()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'fast_greedy' ):
		dendrogram = tempGraph.community_fastgreedy()
		partition = dendrogram.as_clustering()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'infomap' ):
		partition = tempGraph.community_infomap()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'label_propagation' ):
		partition = tempGraph.community_label_propagation()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'leading_eigenvector' ):
		partition = tempGraph.community_leading_eigenvector()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'multilevel' ):
		partition = tempGraph.community_multilevel()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'spinglass' ): # <- Problem - does not work on disconnected graphs
		partition = tempGraph.community_spinglass()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))
	elif( args.algo[0] == 'walktrap' ):
		dendrogram = tempGraph.community_walktrap()
		partition = dendrogram.as_clustering()
		valueScores.append(returnScore(graph, tempGraph, graphPartition, partition, args.value[0]))

bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format(bottleneckEnd - bottleneckStart)

print("\nCompiling results...\n")

tupledTryAll = []
for element in tryAll:
	tupledTryAll.append(tuple(element))

valueScores = np.array(valueScores)
scores = dict(zip(tupledTryAll, valueScores))
scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
bestNodes = np.array(scoresSorted[0][0])
bestGraph = graph.copy()
bestGraph.delete_vertices(bestNodes)

if( args.algo[0] == 'louvain' ):
	bestGraphPartition = louvain.find_partition(bestGraph, method = 'Modularity')
elif( args.algo[0] == 'edge_betweenness' ):
	dendrogram = bestGraph.community_edge_betweenness(directed = False)
	fix_dendrogram(tempGraph, dendrogram)
	bestGraphPartition = dendrogram.as_clustering()
elif( args.algo[0] == 'fast_greedy' ):
	dendrogram = bestGraph.community_fastgreedy()
	bestGraphPartition = dendrogram.as_clustering()
elif( args.algo[0] == 'infomap' ):
	bestGraphPartition = bestGraph.community_infomap()
elif( args.algo[0] == 'label_propagation' ):
	bestGraphPartition = bestGraph.community_label_propagation()
elif( args.algo[0] == 'leading_eigenvector' ):
	bestGraphPartition = bestGraph.community_leading_eigenvector()
elif( args.algo[0] == 'multilevel' ):
	bestGraphPartition = bestGraph.community_multilevel()
elif( args.algo[0] == 'spinglass' ):
	bestGraphPartition = bestGraph.community_spinglass()
elif( args.algo[0] == 'walktrap' ):
	dendrogram = bestGraph.community_walktrap()
	bestGraphPartition = dendrogram.as_clustering()

vertex_label = []
for i in range(graph.vcount()):
	if( i not in bestNodes ):
		vertex_label.append(i)

plt = ig.plot(bestGraphPartition, "Results/Plots/" + args.value[0] + "/karate_club_graph_exhaustive_" + str(budget) + "_" + args.algo[0] + ".png", mark_groups = True, vertex_label = vertex_label)

exhaustiveFile = open("Results/Data/" + args.value[0] + "/exhaustiveResults" + str(budget) + "_" + args.algo[0] + ".dat", 'w')
exhaustiveFile.write("<------------------Final Exhaustive Scores------------------>\n")
for result in scoresSorted:
	exhaustiveFile.write("%s\n" % str(result))
exhaustiveFile.close()

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format(totalTimeEnd - totalTimeStart)