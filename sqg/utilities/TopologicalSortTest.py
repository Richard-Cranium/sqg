import unittest
from TopologicalSort import Graph, GraphNode, StronglyConnectedComponentFinder


class  TopologicalSortTestCase(unittest.TestCase):

	def testTopologicalSort(self):

		sets = {
			1: set(["a", "b", "e"]),
			2: set(["h", "d", "c"]),
			3: set(["f", "g"])
		}
		aGraph = Graph(nodes=[ GraphNode(name="a", child_list=["b"]),
                           GraphNode(name="b", child_list=["e", "f", "c"]),
                           GraphNode(name="c", child_list=["d", "g"]),
                           GraphNode(name="d", child_list=["c", "h"]),
                           GraphNode(name="e", child_list=["a", "f"]),
                           GraphNode(name="f", child_list=["g"]),
                           GraphNode(name="g", child_list=["f"]),
                           GraphNode(name="h", child_list=["g", "d"]) ])
		print "Create StronglyConnectedComponentFinder object."
		finder = StronglyConnectedComponentFinder(aGraph, False)
		print "Calculate dfs of original graph, the transpose, and the DFS of the transpose."
		finder.findSCC()
		for scc in finder.SCCList:
			self.assertSetEqual(set([x.name for x in scc.nodes]), sets[scc.ident])


