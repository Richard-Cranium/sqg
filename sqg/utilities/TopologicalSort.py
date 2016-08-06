#! /usr/bin/env python
#                             -*- Mode: Python -*-
#
# Figure out strongly connected components from a graph.
#
# See http://en.wikipedia.org/wiki/Strongly_connected_component
#
#
import os


class GraphNode(object):

    def __init__(self, **kwargs):
        # expect "name", "child_list"
        # will set transpose_finish if found
		# will set has_readme if found, otherwise calculate it.
		# will set descendants if found, otherwise initialize it from child_list
        super(GraphNode, self).__init__()
        self.name = kwargs["name"]
        # child_list is a list of GraphNode names.
        self.child_list = kwargs["child_list"]
        self.transpose_finish = kwargs.get("transpose_finish", -1)
        if kwargs.has_key("has_readme"):
            self.has_readme = kwargs["has_readme"]
        else:
            self.has_readme = "%README%" in self.child_list
            if self.has_readme:
                self.child_list.remove("%README%")
        if kwargs.has_key("descendants"):
            self.descendants = kwargs["descendants"]
        else:
            self.descendants = set(self.child_list)
        self.discover = -1
        self.finish = -1

    def __str__(self):
        return ("GraphNode %s; readMe? %s; child_list %s; descendants %s; discover %d. finish %d. finishT: %d."  %
                (self.name, self.has_readme, repr(self.child_list), repr(self.descendants), self.discover, self.finish, self.transpose_finish ))

    def isWhite(self):
        return self.discover == -1 and self.finish == -1

    def isBlack(self):
        return self.finish != -1

    def isGrey(self):
        return self.discover != -1 and self.finish == -1
    

class Graph(object):

    def __init__(self, **kwargs):
        """nodes is a list of GraphNode objects.
        This constructor will create a dictionary (hashmap) of those
        nodes with the node name as a key."""
        super(Graph, self).__init__()
        if kwargs.has_key("nodes"):
            self.nodes = dict([ (x.name, x) for x in kwargs["nodes"] ])
        else:
            self.nodes = {}
        self.time = 0

    def addNode(self, node):
        self.nodes[node.name] = node

    def getNode(self, name):
        return self.nodes[name]
    
    def transpose(self):
        """Return a Graph object which describes the transpose of this one."""
        retval = Graph(nodes=[GraphNode(name=x.name,
                                        child_list=[],
                                        transpose_finish=x.finish,
                                        has_readme=x.has_readme)
                              for x in self.nodes.itervalues()])
        
        for x in self.nodes:
            for y in self.nodes[x].child_list:
                retval.nodes[y].child_list.append(x)
            for y in self.nodes[x].descendants:
                retval.nodes[y].descendants.add(x)
            
        return retval

    def dfs(self, recording=False):
        """Perform a DFS on the graph, setting the discover and finish values.
		recording set to True means that you will update the descendants set
		of each node with the descendants of your immediate children when
		traversing the graph.  That is used only in the sqg context the first
		time we walk the graph.  That allows us to later traverse the 
		topological sort, look at each entry in the list and update the sqf 
		files that entry should be in.
		"""
        # Normally, white, grey, and black are used to mark the nodes.
        # discover == finish == -1 means the node is white.
        # discover != -1 and finish == -1 means the node is grey
        # discover != -1 and finish != -1 means the node is black.
        # (Actually, finish != -1 is sufficient to declare a node to be black.)
        #
        # More wierdness.  If none of the transposeFinish values are
        # different from the default, you essentially get all the nodes in
        # no particular order.
        #
        for aval in self.nodes.values():
            aval.discover = aval.finish = -1
        theList = [ x for x in self.nodes.values() ]
        theList.sort(None, lambda x: x.transpose_finish, True)
        self.time = 0
        if recording:
            return [ self.__visitRecording(x, []) for x in theList if x.isWhite()]
        else:
            return [ self.__visit(x, []) for x in theList if x.isWhite() ]

    def __visit(self, node, retlist):
        self.time += 1
        node.discover = self.time
        for x in node.child_list:
            if self.nodes[x].isWhite():
                self.__visit(self.nodes[x], retlist)
        self.time += 1
        node.finish = self.time
        retlist.append(node)
        return retlist

    def __visitRecording(self, node, retlist):
        self.time += 1
        node.discover = self.time
        for x in node.child_list:
            if self.nodes[x].isWhite():
                self.__visitRecording(self.nodes[x], retlist)
            node.descendants.update(self.nodes[x].descendants) 
        self.time += 1
        node.finish = self.time
        retlist.append(node)
        return retlist
            
class SCC(object):
	"""This is a Strongly Connected Component object."""

	IDENT = 1

	def __init__(self, nodeList, verbose):
		self.import_list = set() # this is a set of GraphNode ids
		self.nodes = set()        # this is a set of GraphNode objects
		self.ident = SCC.IDENT
		SCC.IDENT += 1

		for aNode in nodeList:
			self.addNode(aNode, verbose)


	def addNode(self, theNode, verbose):
		if verbose:
			print "Adding %s to SCC %d" % (theNode, self.ident)
		self.nodes.add(theNode)
		self.import_list.update(theNode.child_list)

	@property
	def nodeList(self):
		"""Return a list of nodes versus a set of them."""
		return [ y for y in self.nodes]

	def __str__(self):
		temp = "SCC ident: %d" % self.ident
		for aNode in self.nodes:
			temp += (os.linesep + str(aNode))
		return temp + os.linesep

class StronglyConnectedComponentFinder(object):

    def __init__(self, theGraph, verbose=False):
        # verbose here is for debugging
        self.graph = theGraph
        self.graphT = None
        self.verbose = verbose
        self.SCCList = []
        self.SCCMap = {}

    def findSCC(self):
        if self.graphT:
            return
        self.graph.dfs(True)
        self.graphT = self.graph.transpose()
        theList = self.graphT.dfs(False)
        # theList is a list of lists of GraphNodes.  Python can be rather Lispy at times.
        for x in theList:
            newSCC = SCC(x, self.verbose)
            self.SCCList.append(newSCC)
            self.SCCMap[newSCC.ident] = newSCC

