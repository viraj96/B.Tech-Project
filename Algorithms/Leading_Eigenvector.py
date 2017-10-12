from igraph import *

g = Graph()
g.add_vertices(5000)

edgeList = []
for line in open("./../Binary_Networks/network.dat", 'r'):
	a = line.split()
	edgeList.append((int(a[0])-1, int(a[1])-1))

g.add_edges(edgeList)
g.simplify()

leadingEigenvector = g.community_leading_eigenvector()

file = open("./../Results/Community/Leading_Eigenvector_Detected.dat", 'w')
fileData = {}

for idx, cluster in enumerate(leadingEigenvector):
	for member in cluster:
		fileData[member+1] = idx+1
		

for key in sorted(fileData):
	file.write(str(key) + "\t" + str(fileData[key]) + "\n")

file.close()
plt = plot(leadingEigenvector)
plt.save("./../Results/Pictures/Leading_Eigenvector.png")