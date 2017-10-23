#!/bin/bash

echo "Starting modularity value.."

echo "Starting louvain.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo louvain
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo louvain
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo louvain
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo louvain
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo louvain
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo louvain
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo louvain
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo louvain
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo louvain
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo louvain
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo louvain

echo "Starting edge_betweenness.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo edge_betweenness
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo edge_betweenness
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo edge_betweenness
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo edge_betweenness
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo edge_betweenness
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo edge_betweenness
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo edge_betweenness
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo edge_betweenness
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo edge_betweenness
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo edge_betweenness
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo edge_betweenness

echo "Starting fast_greedy.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo fast_greedy
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo fast_greedy
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo fast_greedy
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo fast_greedy
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo fast_greedy
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo fast_greedy
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo fast_greedy
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo fast_greedy
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo fast_greedy
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo fast_greedy
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo fast_greedy

echo "Starting infomap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo infomap
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo infomap
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo infomap
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo infomap
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo infomap
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo infomap
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo infomap
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo infomap
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo infomap
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo infomap
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo infomap

echo "Starting label_propagation.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo label_propagation
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo label_propagation
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo label_propagation
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo label_propagation
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo label_propagation
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo label_propagation
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo label_propagation
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo label_propagation
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo label_propagation
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo label_propagation
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo label_propagation

echo "Starting leading_eigenvector.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo leading_eigenvector
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo leading_eigenvector
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo leading_eigenvector
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo leading_eigenvector
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo leading_eigenvector
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo leading_eigenvector
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo leading_eigenvector
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo leading_eigenvector
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo leading_eigenvector
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo leading_eigenvector
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo leading_eigenvector

echo "Starting multilevel.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo multilevel
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo multilevel
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo multilevel
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo multilevel
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo multilevel
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo multilevel
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo multilevel
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo multilevel
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo multilevel
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo multilevel
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo multilevel

# echo "Starting spinglass.."
# python greedy.py --budget 4 --value modularity --algo spinglass

echo "Starting walktrap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo walktrap
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo walktrap
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo walktrap
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo walktrap
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo walktrap
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo walktrap
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo walktrap
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo walktrap
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo walktrap
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo walktrap
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo walktrap


echo "Starting nmi value.."

echo "Starting louvain.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo louvain
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo louvain
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo louvain
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo louvain
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo louvain
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo louvain
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo louvain
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo louvain
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo louvain
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo louvain
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo louvain

echo "Starting edge_betweenness.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo edge_betweenness
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo edge_betweenness
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo edge_betweenness
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo edge_betweenness
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo edge_betweenness
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo edge_betweenness
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo edge_betweenness
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo edge_betweenness
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo edge_betweenness
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo edge_betweenness
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo edge_betweenness

echo "Starting fast_greedy.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo fast_greedy
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo fast_greedy
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo fast_greedy
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo fast_greedy
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo fast_greedy
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo fast_greedy
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo fast_greedy
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo fast_greedy
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo fast_greedy
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo fast_greedy
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo fast_greedy

echo "Starting infomap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo infomap
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo infomap
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo infomap
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo infomap
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo infomap
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo infomap
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo infomap
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo infomap
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo infomap
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo infomap
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo infomap

echo "Starting label_propagation.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo label_propagation
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo label_propagation
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo label_propagation
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo label_propagation
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo label_propagation
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo label_propagation
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo label_propagation
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo label_propagation
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo label_propagation
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo label_propagation
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo label_propagation

echo "Starting leading_eigenvector.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo leading_eigenvector
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo leading_eigenvector
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo leading_eigenvector
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo leading_eigenvector
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo leading_eigenvector
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo leading_eigenvector
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo leading_eigenvector
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo leading_eigenvector
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo leading_eigenvector
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo leading_eigenvector
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo leading_eigenvector

echo "Starting multilevel.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo multilevel
# echo "Starting local modularity"
python greedy.py --budget 4 --metric localMod --value nmi --algo multilevel
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo multilevel
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo multilevel
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo multilevel
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo multilevel
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo multilevel
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo multilevel
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo multilevel
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo multilevel
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo multilevel

# echo "Starting spinglass.."
# python greedy.py --budget 4 --value nmi --algo spinglass

echo "Starting walktrap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo walktrap
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo walktrap
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo walktrap
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo walktrap
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo walktrap
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo walktrap
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo walktrap
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo walktrap
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo walktrap
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo walktrap
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo walktrap