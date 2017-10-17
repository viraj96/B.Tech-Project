#!/bin/bash

echo "Starting modularity metric.."
echo "Starting louvain.."
python exhaustive.py --budget 4 --value modularity --algo louvain
echo "Starting edge_betweenness.."
python exhaustive.py --budget 4 --value modularity --algo edge_betweenness
echo "Starting fast_greedy.."
python exhaustive.py --budget 4 --value modularity --algo fast_greedy
echo "Starting infomap.."
python exhaustive.py --budget 4 --value modularity --algo infomap
echo "Starting label_propagation.."
python exhaustive.py --budget 4 --value modularity --algo label_propagation
echo "Starting leading_eigenvector.."
python exhaustive.py --budget 4 --value modularity --algo leading_eigenvector
echo "Starting multilevel.."
python exhaustive.py --budget 4 --value modularity --algo multilevel
# echo "Starting spinglass.."
# python exhaustive.py --budget 4 --value modularity --algo spinglass
echo "Starting walktrap.."
python exhaustive.py --budget 4 --value modularity --algo walktrap


echo "Starting nmi metric.."
echo "Starting louvain.."
python exhaustive.py --budget 4 --value nmi --algo louvain
echo "Starting edge_betweenness.."
python exhaustive.py --budget 4 --value nmi --algo edge_betweenness
echo "Starting fast_greedy.."
python exhaustive.py --budget 4 --value nmi --algo fast_greedy
echo "Starting infomap.."
python exhaustive.py --budget 4 --value nmi --algo infomap
echo "Starting label_propagation.."
python exhaustive.py --budget 4 --value nmi --algo label_propagation
echo "Starting leading_eigenvector.."
python exhaustive.py --budget 4 --value nmi --algo leading_eigenvector
echo "Starting multilevel.."
python exhaustive.py --budget 4 --value nmi --algo multilevel
# echo "Starting spinglass.."
# python exhaustive.py --budget 4 --value nmi --algo spinglass
echo "Starting walktrap.."
python exhaustive.py --budget 4 --value nmi --algo walktrap