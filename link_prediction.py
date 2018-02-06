import random
import louvain
import operator
import numpy as np
import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import networkx.algorithms.link_prediction as lp
from itertools import permutations, combinations, izip

def within_inter_cluster(graph, node_labels):
	non_edges = nx.non_edges(graph)
	result = dict()
	for edge in non_edges:
		u = edge[0]
		v = edge[1]
		community_u = node_labels[u]
		community_v = node_labels[v]
		if( community_u == community_v ):
			common_neighbors = set(nx.common_neighbors(graph, u, v))
			within = set(w for w in common_neighbors if( node_labels[w] == community_u ))
			inter = common_neighbors - within
			if( len(inter) == 0 ):
				result[edge] = len(within)*1.0
			else:
				result[edge] = len(within)*1.0 / len(inter)
		else:
			result[edge] = 0
	return result

# ig_graph = ig.Graph.Read_Ncol("coauthorship_network", directed = False)
ig_graph = ig.Graph.Read_GML("footballTSEweb/footballTSEinput.gml")
ig_nodes = ig_graph.vcount()
ig_graph.vs["name"] = np.arange(ig_nodes)

ig_graph_partition = louvain.find_partition(ig_graph, method = "Modularity")

edge_list = ig_graph.get_edgelist()

precision = []

for i in range(5):

	random.shuffle(edge_list)

	train_edge_list = edge_list[:int(0.8*len(edge_list))]  # 80:20 split
	test_edge_list = edge_list[int(0.8*len(edge_list)):]

	nx_graph = nx.Graph(train_edge_list)
	nx_nodes = nx_graph.nodes()

	for node in range(ig_nodes):
		if( node not in nx_nodes ):
			nx_graph.add_node(node)

	node_labels = np.zeros(ig_nodes)

	for idx, cluster in enumerate(ig_graph_partition):
		for node in cluster:
			node_labels[node] = idx

	preds = within_inter_cluster(nx_graph, node_labels)
	preds_sorted = sorted(preds.items(), key = operator.itemgetter(1))
	preds_sorted = preds_sorted[::-1]

	present = 0.0
	l = 100
	counter = 0

	for key, p in preds_sorted:
		u = key[0]
		v = key[1]
		if( (u, v) in test_edge_list ):
			present += 1.0
		counter += 1
		if( counter >= 100 ):
			break
	precision.append(present/l)

print("Original Precision = {0}".format(np.mean(np.array(precision))))

budget = 50

def my_function(temp_graph, deleted_vertex):
	temp_graph.delete_vertices(deleted_vertex)
	temp_graph_nodes = temp_graph.vcount()
	
	temp_graph_partition = louvain.find_partition(temp_graph, method = "Modularity")

	temp_edge_list = temp_graph.get_edgelist()
	
	inner_precision = []

	for j in range(5):

		random.shuffle(temp_edge_list)

		temp_train_edge_list = temp_edge_list[:int(0.8*len(temp_edge_list))]
		temp_test_edge_list = temp_edge_list[int(0.8*len(temp_edge_list)):]

		temp_nx_graph = nx.Graph(temp_train_edge_list)
		temp_nx_nodes = temp_nx_graph.nodes()

		for node in range(temp_graph_nodes):
			if( node not in temp_nx_nodes ):
				temp_nx_graph.add_node(node)

		temp_node_labels = np.zeros(temp_graph_nodes)

		for idx, cluster in enumerate(temp_graph_partition):
			for node in cluster:
				temp_node_labels[node] = idx

		temp_preds = within_inter_cluster(temp_nx_graph, temp_node_labels)
		temp_preds_sorted = sorted(temp_preds.items(), key = operator.itemgetter(1))
		temp_preds_sorted = temp_preds_sorted[::-1]
		temp_present = 0.0
		inner_counter = 0

		for key, p in temp_preds_sorted:
			u = key[0]
			v = key[1]
			if( (u, v) in temp_test_edge_list ):
				temp_present += 1.0
			inner_counter += 1
			if( inner_counter >= 100 ):
				break

		inner_precision.append(temp_present/l)

	return inner_precision, temp_graph

def closenessVitality(graph):
	temp = np.matrix(graph.shortest_paths_dijkstra(mode = 3))
	initial = temp[temp != np.inf].sum()
	closeness_vitality = []
	for i in range(graph.vcount()):
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		vertex_cont = np.matrix(tempGraph.shortest_paths_dijkstra(mode = 3))
		closeness_vitality.append(initial - vertex_cont[vertex_cont != np.inf].sum())
	return closeness_vitality

def intra_degree(graph, partition):
	intra_degree_values = np.zeros(len(graph.vs))
	for cluster in partition:
		tuples = combinations(cluster, 2)
		for first, second in tuples:
			edges = graph.es.select(_within = [first, second])
			for e in edges:
				intra_degree_values[e.tuple[0]] += 1
				intra_degree_values[e.tuple[1]] += 1
	return intra_degree_values

def inter_degree(graph, partition):
	intra_degree_values = np.array(intra_degree(graph, partition))
	degrees = np.array(graph.degree())
	return degrees - intra_degree_values


modes = ["clustering_coefficient", "degree_centrality", "betweeness_centrality", "eigenvector_centrality", "closeness_centrality", "coreness", "diversity", "eccentricity", "constraint", "closeness_vitality", "intra_degree", "inter_degree"]

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'lawngreen', 'peru', 'springgreen', 'brown', 'khaki']
modes_plot = []

for idxi, mode in enumerate(modes):

	print("Mode = {0}".format(mode))
	counter = 1
	mode_precision_curve = []

	while( counter <= budget ):

		temp_graph = ig_graph.copy()
		
		if( mode == "clustering_coefficient" ):
			value_list = temp_graph.transitivity_local_undirected(mode = 'zero')
		elif( mode == "degree_centrality" ):
			value_list = temp_graph.degree()
		elif( mode == "betweeness_centrality" ):
			value_list = temp_graph.betweenness(directed = False)
		elif( mode == "eigenvector_centrality" ):
			value_list = temp_graph.eigenvector_centrality(directed = False)
		elif( mode == "closeness_centrality" ):
			value_list = temp_graph.closeness()
		elif( mode == "coreness" ):
			value_list = temp_graph.coreness()
		elif( mode == "diversity" ):
			value_list = temp_graph.diversity()
		elif( mode == "eccentricity" ):
			value_list = temp_graph.eccentricity()
		elif( mode == "constraint" ):
			value_list = temp_graph.constraint()
		elif( mode == "closeness_vitality" ):
			value_list = closenessVitality(temp_graph)
		elif( mode == "intra_degree" ):
			value_list = intra_degree(temp_graph, ig_graph_partition)
		elif( mode == "inter_degree" ):
			value_list = inter_degree(temp_graph, ig_graph_partition)

		my_dict = dict()
		for idx, val in enumerate(value_list):
			my_dict[idx] = val
		nodes = sorted(my_dict.items(), key = operator.itemgetter(1))
		nodes = nodes[:counter]
		deleted_nodes = []
		for tuple_val in nodes:
			deleted_nodes.append(tuple_val[0])
		inner_precision, temp_graph = my_function(temp_graph, deleted_nodes)
		precision_val = np.mean(np.array(inner_precision))
		mode_precision_curve.append(precision_val)
		
		print("New Precision = {0}".format(np.mean(np.array(inner_precision))))

		counter += 1

	plt.plot(mode_precision_curve, color = colors[idxi], marker = 'o', label = mode)

legend = plt.legend(bbox_to_anchor=(1.04,1), loc = "upper left")
plt.savefig('football_task_based_approach.png', bbox_extra_artists=(legend,), bbox_inches='tight')
plt.show()

print("Done!!")