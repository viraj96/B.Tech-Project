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

parser = argparse.ArgumentParser(description = 'Generate greedy answer based to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation)')
parser.add_argument('--metric', type = str, nargs = '+', help = 'Metric to be used for greedy approach. Choices are degree, clustering coefficient and local modularity', choices = ['clusteringCoeff', 'localMod', 'degreeCenter', 'betweenCenter', 'eigenCenter', 'closeCenter', 'coreness', 'diversity', 'eccentricity', 'constraint', 'closeVital'])
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])

args = parser.parse_args()

def storeFileAndPlots(fileName, graph, tempGraph, graphPartition, partition, plotName, budget, selection = None):
	vertex_label = []
	for i in range(graph.vcount()):
		if( i not in bestNodes ):
			vertex_label.append(i)
	ig.plot(partition, plotName + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)
	file = open(fileName, 'w')
	score = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
	file.write(str(score) + "\n")
	file.close()	

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

def returnScore(graph, tempGraph, graphPartition, partition, value, selection = None):
	if( value == 'modularity' ):
		graphModularity = graph.modularity(graphPartition)
		return graphModularity - tempGraph.modularity(partition)
	elif( value == 'nmi' ):
		new_graph = graph.copy()
		new_graph.vs["membership"] = graphPartition.membership
		new_graph.delete_vertices(selection)
		new_graphPartition = ig.VertexClustering(new_graph, new_graph.vs["membership"])
		return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)

def closenessVitality(graph):
	initial = 0
	for i in range(graph.vcount()):
		paths = graph.get_shortest_paths(i, mode = 3)
		initial += sum(len(path) for path in paths)	
	closeness_vitality = []
	for i in range(graph.vcount()):		
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		vertex_cont = 0
		for j in range(tempGraph.vcount()):
			paths = tempGraph.get_shortest_paths(j, mode = 3)
			vertex_cont += sum(len(path) for path in paths)		
		closeness_vitality.append(initial - vertex_cont)
	return closeness_vitality

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
	elif( algo == 'walktrap' ):
		dendrogram = graph.community_walktrap()
		graphPartition = dendrogram.as_clustering()
		return graphPartition

graphPartition = returnPartition(graph, args.algo[0])

if( args.budget ):
	budget = args.budget
else:
	budget = 5

tryAll = []

print("\nCalculating value scores...\n")

bottleneckStart = datetime.datetime.now()

tempGraph = graph.copy()

if( args.metric[0] == 'clusteringCoeff' ):
	bestNodes = np.array(tempGraph.transitivity_local_undirected(mode = 'zero')).argsort()[-budget:][::-1]
elif( args.metric[0] == 'localMod' ):
	print("Local Modularity")
elif( args.metric[0] == 'degreeCenter' ):
	bestNodes = np.array(tempGraph.degree()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'betweenCenter' ):
	bestNodes = np.array(tempGraph.betweenness(directed = False)).argsort()[-budget:][::-1]
elif( args.metric[0] == 'eigenCenter' ):
	bestNodes = np.array(tempGraph.eigenvector_centrality(directed = False)).argsort()[-budget:][::-1]
elif( args.metric[0] == 'closeCenter' ):
	bestNodes = np.array(tempGraph.closeness()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'coreness' ):
	bestNodes = np.array(tempGraph.coreness()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'diversity' ):
	bestNodes = np.array(tempGraph.diversity()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'eccentricity' ):
	bestNodes = np.array(tempGraph.eccentricity()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'constraint' ):
	bestNodes = np.array(tempGraph.constraint()).argsort()[-budget:][::-1]
elif( args.metric[0] == 'closeVital' ):
	bestNodes = np.array(closenessVitality(tempGraph)).argsort()[-budget:][::-1]

tryAll = bestNodes
tempGraph.delete_vertices(bestNodes)
valueScore = 0
selection = bestNodes

if( args.algo[0] == 'louvain' ):
	partition = louvain.find_partition(tempGraph, method = 'Modularity')
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'edge_betweenness' ):
	dendrogram = tempGraph.community_edge_betweenness(directed = False)
	fix_dendrogram(tempGraph, dendrogram)
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'fast_greedy' ):
	dendrogram = tempGraph.community_fastgreedy()
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'infomap' ):
	partition = tempGraph.community_infomap()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'label_propagation' ):
	partition = tempGraph.community_label_propagation()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'leading_eigenvector' ):
	partition = tempGraph.community_leading_eigenvector()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'multilevel' ):
	partition = tempGraph.community_multilevel()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'walktrap' ):
	dendrogram = tempGraph.community_walktrap()
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)

bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format((bottleneckEnd - bottleneckStart))

print("\nCompiling results...\n")

storeFileAndPlots("Results/Data/" + args.value[0] + "/" + args.algo[0] + "/" + args.metric[0] + ".dat", graph, tempGraph, graphPartition, partition, "Results/Plots/" + args.value[0] + "/" + args.algo[0] +  "/karate_club_graph_", args.metric[0] + "_" + str(budget), bestNodes)

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format((totalTimeEnd - totalTimeStart))