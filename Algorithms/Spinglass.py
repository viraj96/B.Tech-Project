from igraph import *

g = Graph()
g.add_vertices(5000)

edgeList = []
for line in open("./../Binary_Networks/network.dat", 'r'):
	a = line.split()
	edgeList.append((int(a[0])-1, int(a[1])-1))

g.add_edges(edgeList)
g.simplify()

spinGlass = g.community_spinglass()

file = open("./../Results/Community/Spinglass_Detected.dat", 'w')
fileData = {}

for idx, cluster in enumerate(spinGlass):
	for member in cluster:
		fileData[member+1] = idx+1
		

for key in sorted(fileData):
	file.write(str(key) + "\t" + str(fileData[key]) + "\n")

file.close()
plt = plot(spinGlass)
plt.save("./../Results/Pictures/Spinglass.png")