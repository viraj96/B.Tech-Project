import pp
import time
import numpy
import scipy.stats
import igraph
import random
import louvain
import networkx
import operator
import itertools
import matplotlib.pyplot

def common_neighbors_modified(graph, node_labels):
	non_edges = networkx.non_edges(graph)
	result = dict()
	for edge in non_edges:
		u = edge[0]
		v = edge[1]
		common_neighbors = set(networkx.common_neighbors(graph, u, v))
		result[edge] = len(common_neighbors)
		for vertex in common_neighbors:
			if( node_labels[vertex] == node_labels[u] == node_labels[v] ):
				result[edge] += 1
	return result

def resource_allocation(graph, node_labels):
	non_edges = networkx.non_edges(graph)
	result = dict()
	for edge in non_edges:
		u = edge[0]
		v = edge[1]
		common_neighbors = set(networkx.common_neighbors(graph, u, v))
		result[edge] = 0
		for vertex in common_neighbors:
			degree_val = graph.degree(vertex)
			if( node_labels[vertex] == node_labels[u] == node_labels[v] ):
				result[edge] += 2 / degree_val
			else:
				result[edge] += 1 / degree_val
	return result

def within_inter_cluster(graph, node_labels):
	non_edges = networkx.non_edges(graph)
	result = dict()
	for edge in non_edges:
		u = edge[0]
		v = edge[1]
		community_u = node_labels[u]
		community_v = node_labels[v]
		if( community_u == community_v and community_u != -1 ):
			common_neighbors = set(networkx.common_neighbors(graph, u, v))
			within = set(w for w in common_neighbors if( node_labels[w] == community_u ))
			inter = common_neighbors - within
			if( len(inter) == 0 ):
				result[edge] = len(within)*1.0
			else:
				result[edge] = len(within)*1.0 / len(inter)
		else:
			result[edge] = 0
	return result

ig_graph = igraph.Graph.Read_GML("footballTSEweb/footballTSEinput.gml")
# ig_graph = igraph.Graph.Read_Ncol("coauthorship_network", directed = False)
ig_nodes = ig_graph.vcount()
ig_graph_partition = louvain.find_partition(ig_graph, method = "Modularity")
# original_community
edge_list = ig_graph.get_edgelist()

def my_function(temp_graph, deleted_vertex, edge_list, ig_nodes, ig_graph_partition, ig_graph):
	neighbors = []
	for vertex in deleted_vertex:
		temp_list = temp_graph.neighbors(vertex)
		for temp_vertex in temp_list:
			if( temp_vertex not in neighbors ):
				neighbors.append(temp_vertex)

	temp_graph.delete_vertices(deleted_vertex)
	temp_graph_nodes = temp_graph.vcount()	
	temp_edge_list = temp_graph.get_edgelist()
	temp_graph_partition = louvain.find_partition(temp_graph, method = "Modularity")
	
	temp_edge_list = sorted(temp_edge_list)

	new_temp_edge_list = []
	for val in temp_edge_list:
		edge = tuple((int(temp_graph.vs[val[0]]['id']), int(temp_graph.vs[val[1]]['id'])))
		new_temp_edge_list.append(edge)

	new_temp_edge_list = sorted(new_temp_edge_list)
	
	inner_precision = []
	inner_recall = []
	precision = []
	recall = []

	for j in range(5):

		random.shuffle(new_temp_edge_list)

		test_edge_list_len = int(0.2 * len(new_temp_edge_list))
		test_edge_list = []
		khali = []
		counter = 0
		for idx, edge in enumerate(new_temp_edge_list):
			if( edge[0] in neighbors or edge[1] in neighbors ):
				test_edge_list.append(edge)
				counter += 1
				khali.append(idx)
			if( counter == test_edge_list_len ):
				break

		if( counter != test_edge_list_len ):
			for idx, edge in enumerate(new_temp_edge_list):
				if( idx not in khali ):
					test_edge_list.append(edge)
					counter += 1
				if( counter == test_edge_list_len ):
					break

		train_edge_list = list(set(new_temp_edge_list) - set(test_edge_list))
		# train_edge_list = new_temp_edge_list[:int(0.8*len(new_temp_edge_list))]  # 80:20 split
		# test_edge_list = new_temp_edge_list[int(0.8*len(new_temp_edge_list)):]

		temp_nx_graph = networkx.Graph(train_edge_list)
		temp_nx_nodes = temp_nx_graph.nodes()

		nx_graph = networkx.Graph(train_edge_list)
		nx_graph.add_nodes_from(deleted_vertex)
		nx_nodes = nx_graph.nodes()

		node_labels = numpy.zeros(ig_nodes)
		node_labels[deleted_vertex] = -1
		for idx, cluster in enumerate(ig_graph_partition):
			for node in cluster:
				node_labels[node] = idx

		temp_node_labels = numpy.zeros(ig_nodes)
		temp_node_labels[deleted_vertex] = -1
		for idx, cluster in enumerate(temp_graph_partition):
			for node in cluster:
				temp_node_labels[int(temp_graph.vs[node]['id'])] = idx

		# preds = within_inter_cluster(nx_graph, node_labels)
		preds = common_neighbors_modified(nx_graph, node_labels)
		# preds = resource_allocation(nx_graph, node_labels)
		preds_sorted = sorted(preds.items(), key = operator.itemgetter(1))
		preds_sorted = preds_sorted[::-1]

		present = 0.0
		counter = 0

		for key, p in preds_sorted:
			u = key[0]
			v = key[1]
			if( (u, v) in test_edge_list ):
				present += 1.0
			counter += 1
			if( counter == 100 ):
				break

		precision.append((present * 1.0) / 100)
		recall.append(((len(test_edge_list) - present) * 1.0) / 100)

		# temp_preds = within_inter_cluster(temp_nx_graph, temp_node_labels)
		temp_preds = common_neighbors_modified(temp_nx_graph, temp_node_labels)
		# temp_preds = resource_allocation(temp_nx_graph, temp_node_labels)
		temp_preds_sorted = sorted(temp_preds.items(), key = operator.itemgetter(1))
		temp_preds_sorted = temp_preds_sorted[::-1]
		
		temp_present = 0.0
		counter = 0

		for key, p in temp_preds_sorted:
			u = key[0]
			v = key[1]
			if( (u, v) in test_edge_list ):
				temp_present += 1.0
			counter += 1
			if( counter >= 100 ):
				break

		inner_precision.append((temp_present * 1.0) / 100)
		inner_recall.append(((len(test_edge_list) - temp_present) * 1.0) / 100)

	return numpy.mean(numpy.array(precision)), numpy.mean(numpy.array(recall)), numpy.mean(numpy.array(inner_precision)), numpy.mean(numpy.array(inner_recall))

	
	################################### keep two different graphs ###################################

	# temp_graph.delete_vertices(deleted_vertex)
	# temp_graph_nodes = temp_graph.vcount()	
	# temp_edge_list = temp_graph.get_edgelist()
	# temp_graph_partition = louvain.find_partition(temp_graph, method = "Modularity")
	
	# temp_edge_list = sorted(temp_edge_list)

	# # new_temp_edge_list = []
	# # for val in temp_edge_list:
	# # 	edge = tuple((int(temp_graph.vs[val[0]]['id']), int(temp_graph.vs[val[1]]['id'])))
	# # 	new_temp_edge_list.append(edge)

	# # new_temp_edge_list = sorted(new_temp_edge_list)
	
	# edge_list_copy = ig_graph.get_edgelist()

	# new_edge_list = []
	# for edge in edge_list_copy:
	# 	if( edge[0] not in deleted_vertex and edge[1] not in deleted_vertex ):
	# 		new_edge_list.append(edge)

	# new_edge_list = sorted(new_edge_list)

	# inner_precision = []
	# inner_recall = []
	# precision = []
	# recall = []

	# for j in range(5):

	# 	random.shuffle(temp_edge_list)

	# 	temp_train_edge_list = temp_edge_list[:int(0.8*len(temp_edge_list))]  # 80:20 split
	# 	temp_test_edge_list = temp_edge_list[int(0.8*len(temp_edge_list)):]

	# 	random.shuffle(new_edge_list)

	# 	train_edge_list = new_edge_list[:int(0.8*len(new_edge_list))]  # 80:20 split
	# 	test_edge_list = new_edge_list[int(0.8*len(new_edge_list)):]

	# 	temp_nx_graph = networkx.Graph(temp_train_edge_list)
	# 	temp_nx_nodes = temp_nx_graph.nodes()

	# 	nx_graph = networkx.Graph(train_edge_list)
	# 	nx_nodes = nx_graph.nodes()

	# 	node_labels = numpy.zeros(ig_nodes)
	# 	node_labels[deleted_vertex] = -1
	# 	for idx, cluster in enumerate(ig_graph_partition):
	# 		for node in cluster:
	# 			node_labels[node] = idx

	# 	temp_node_labels = numpy.zeros(ig_nodes)
	# 	temp_node_labels[deleted_vertex] = -1
	# 	for idx, cluster in enumerate(temp_graph_partition):
	# 		for node in cluster:
	# 			# temp_node_labels[int(temp_graph.vs[node]['id'])] = idx
	# 			temp_node_labels[node] = idx

	# 	preds = within_inter_cluster(nx_graph, node_labels)
	# 	preds_sorted = sorted(preds.items(), key = operator.itemgetter(1))
	# 	preds_sorted = preds_sorted[::-1]

	# 	present = 0.0
	# 	counter = 0

	# 	for key, p in preds_sorted:
	# 		u = key[0]
	# 		v = key[1]
	# 		if( (u, v) in test_edge_list ):
	# 			present += 1.0
	# 		counter += 1
	# 		if( counter == 100 ):
	# 			break

	# 	precision.append((present * 1.0) / 100)
	# 	recall.append(((len(test_edge_list) - present) * 1.0) / 100)

	# 	temp_preds = within_inter_cluster(temp_nx_graph, temp_node_labels)
	# 	temp_preds_sorted = sorted(temp_preds.items(), key = operator.itemgetter(1))
	# 	temp_preds_sorted = temp_preds_sorted[::-1]
		
	# 	temp_present = 0.0
	# 	counter = 0

	# 	for key, p in temp_preds_sorted:
	# 		u = key[0]
	# 		v = key[1]
	# 		if( (u, v) in temp_test_edge_list ):
	# 			temp_present += 1.0
	# 		counter += 1
	# 		if( counter >= 100 ):
	# 			break

	# 	inner_precision.append((temp_present * 1.0) / 100)
	# 	inner_recall.append(((len(temp_test_edge_list) - temp_present) * 1.0) / 100)

	# return numpy.mean(numpy.array(precision)), numpy.mean(numpy.array(recall)), numpy.mean(numpy.array(inner_precision)), numpy.mean(numpy.array(inner_recall))

def closenessVitality(graph):
	temp = numpy.matrix(graph.shortest_paths_dijkstra(mode = 3))
	initial = temp[temp != numpy.inf].sum()
	closeness_vitality = []
	for i in range(graph.vcount()):
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		vertex_cont = numpy.matrix(tempGraph.shortest_paths_dijkstra(mode = 3))
		closeness_vitality.append(initial - vertex_cont[vertex_cont != numpy.inf].sum())
	return closeness_vitality

def intra_degree(graph, partition):
	intra_degree_values = numpy.zeros(len(graph.vs))
	for cluster in partition:
		tuples = itertools.combinations(cluster, 2)
		for first, second in tuples:
			edges = graph.es.select(_within = [first, second])
			for e in edges:
				intra_degree_values[e.tuple[0]] += 1
				intra_degree_values[e.tuple[1]] += 1
	return intra_degree_values

def inter_degree(graph, partition):
	intra_degree_values = numpy.array(intra_degree(graph, partition))
	degrees = numpy.array(graph.degree())
	return degrees - intra_degree_values

def normalize(vector):
	norm = numpy.linalg.norm(vector)
	if( norm == 0 ):
		return vector
	return vector / norm


modes = ["clustering_coefficient", "degree_centrality", "betweeness_centrality", "eigenvector_centrality", "closeness_centrality", "coreness", "diversity", "eccentricity", "constraint", "closeness_vitality", "intra_degree", "inter_degree"]

percent_nodes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

def main(mode, ig_graph, edge_list,ig_nodes, ig_graph_partition, percent_nodes):
	counter = 1
	budget = len(percent_nodes)
	mode_f1_curve = []
	mode_temp_f1_curve = []

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
		nodes = sorted(my_dict.items(), key = operator.itemgetter(1), reverse = True)
		len_nodes = int(ig_nodes * 0.01 * percent_nodes[counter - 1])
		nodes = nodes[:len_nodes]
		
		deleted_nodes = []
		for tuple_val in nodes:
			deleted_nodes.append(tuple_val[0])
		
		precision, recall, inner_precision, inner_recall = my_function(temp_graph, deleted_nodes, edge_list, ig_nodes, ig_graph_partition, ig_graph)
		mode_f1_curve.append((2.0 * precision * recall) / (precision + recall))
		mode_temp_f1_curve.append((2.0 * inner_precision * inner_recall) / (inner_precision + inner_recall))
		mode_f1_curve_ratio = [ (b / a) for a, b in zip(mode_f1_curve, mode_temp_f1_curve)]
		counter += 1

	matplotlib.pyplot.figure()
	matplotlib.pyplot.plot(mode_f1_curve, color = 'b', marker = 'o', label = "original")
	matplotlib.pyplot.plot(mode_temp_f1_curve, color = 'g', marker = 'o', label = mode)
	matplotlib.pyplot.xticks(numpy.arange(len(percent_nodes)), percent_nodes)
	legend = matplotlib.pyplot.legend(bbox_to_anchor=(1.04,1), loc = "upper left")
	matplotlib.pyplot.savefig('task_based_images/football/' + mode + '.png', bbox_extra_artists=(legend,), bbox_inches='tight')

	matplotlib.pyplot.figure()
	matplotlib.pyplot.plot(mode_f1_curve_ratio, color = 'g', marker = 'o', label = mode)
	matplotlib.pyplot.savefig('task_based_images/football/' + mode + '_ratio.png', bbox_extra_artists=(legend,), bbox_inches='tight')

	print("KL Divergence score of Original and {0} = {1}".format(mode, scipy.stats.entropy(mode_f1_curve, mode_temp_f1_curve)))

ppservers = ()
ncpus = 4
job_server = pp.Server(ncpus, ppservers = ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

start_time = time.time()

jobs = [(mode, job_server.submit(main, (mode, ig_graph, edge_list, ig_nodes, ig_graph_partition, percent_nodes), (my_function, within_inter_cluster, inter_degree, intra_degree, closenessVitality, normalize, common_neighbors_modified, resource_allocation), ("random", "louvain", "operator", "numpy", "igraph", "networkx", "matplotlib.pyplot", "itertools", "scipy.stats"))) for mode in modes]

for mode, job in jobs:
	print("Mode = {0}".format(mode))
	job()

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()