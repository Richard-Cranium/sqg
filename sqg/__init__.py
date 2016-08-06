def doit():
	import argparse
	import os
	import os.path
	from utilities.PropertyReader import PropertyReader
	from scanning import FileLister
	from utilities.TopologicalSort import GraphNode, Graph, StronglyConnectedComponentFinder
	
	# Read the sbopkg config file
	y = PropertyReader()
	sbo_config = y.readBash("/etc/sbopkg/sbopkg.conf")
	qDir = sbo_config["QUEUEDIR"].strip()
	epilog = """
	Package names are case-sensitive.  Use
	'sbopkg -g pkg' to search if needed.

	This script will overwrite existing queuefiles in {0} so back up any
	existing queuefiles or local modifications prior to running this.
	"""
	parser = argparse.ArgumentParser(description="Generate sbopkg queue files",
										epilog=epilog.format(qDir))
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-a", "--all", help="Generate package queues for all packages.",
						action="store_true")
	group.add_argument("-p","--package", nargs='+', help="Generate queues for the given package(s) only.")
	parser.add_argument("-s","--skip-empty", help="Do not skip packages with empty REQUIRES= lines,", action="store_false")
	args = parser.parse_args()

	# Create formatters for adding lines to the output lists.
	readme_fmt = "# %README%: see the {0} README file." + os.linesep
	package_fmt = "{0}" + os.linesep


	scan_dir = os.path.join(sbo_config["REPO_ROOT"].strip(), sbo_config["REPO_NAME"].strip(), sbo_config["REPO_BRANCH"].strip())

	# Get the list of all the .info files.
	x = FileLister.FileLister(".*\\.info")
	files = x.getList(scan_dir)
	
	# Create and fill the directed graph that contains all the packages and what
	# is found in their REQUIRES lines.
	g = Graph()
	for f in files:
		gn = GraphNode(name=os.path.splitext(os.path.basename(f))[0],child_list=y.read(f)['requires'].split())
		g.addNode(gn)
	
	# Create a StronglyConnectedComponentFinder that will find any Strongly
	# Connected Components (packages that require each other) as well as
	# create a topological sort.
	#
	# The graphing stuff came from another project that I had worked on a long
	# time ago. I've modified it a little to support what we need to do.
	sccf = StronglyConnectedComponentFinder(g)

	sccf.findSCC()
	for x in sccf.SCCList:
		if len(x.nodes) > 1:
			print "You have builders that require each other!"
			print x

	# Build each package's dependency list
	fdata = {}
	for gn in g.nodes.keys():
		fdata[gn] = DependencyContainer(package_fmt.format(gn),g.getNode(gn).has_readme)
		if g.getNode(gn).has_readme:
			fdata[gn].addPackage(readme_fmt.format(gn))
	for x in sccf.SCCList:
		node = x.nodeList[0]
		nname = node.name
		n_readme = node.has_readme
		for z in node.descendants:
			fdata[z].addPackage(package_fmt.format(nname))
			if n_readme:
				fdata[z].addPackage(readme_fmt.format(nname))

	# Choose the packages that you are going to print out.
	packages = args.package
	if args.all:
		packages = fdata.iterkeys()

	# Write them out.
	for x in packages:
		pkg = fdata[x]
		if not (args.skip_empty and pkg.canSkip()):
			with (open(os.path.join(qDir, os.extsep.join([x,"sqf"])), "w+")) as pf:
				pf.writelines(fdata[x].buildList)
	print "Done!"
	
def shouldWrite(skip_flag, depCont):
	return skip_flag==False or depCont.canSkip()


class DependencyContainer(object):
	
	def __init__(self, rootName, has_readme):
		self.has_readme = has_readme
		self.__buildList = [rootName]
		
	def addPackage(self, pName):
		self.__buildList.append(pName)
		
	def canSkip(self):
		return self.has_readme == False and len(self.__buildList) == 1
	
	@property
	def buildList(self):
		return reversed(self.__buildList)