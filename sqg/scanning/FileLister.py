import os
import os.path
import re


class FileLister(object):
    """Retrieve lists of file names from a directory."""

    def __init__(self, thePattern=None):
        self.pattern = thePattern

    def getList(self, dirname):
		"""Traverse dirname and find all files matching my pattern.
		Return the list of full path names of matching files."""
		if self.pattern == None:
			walker = _ListInfo()
		else:
			walker = _ListInfoPattern(self.pattern)
		for path, dirs, files in os.walk(dirname):
			for f in files:
				if walker.test(path, f):
					yield os.path.join(path, f)

## These are internal to FileLister

class _ListInfoPattern(object):
    """Hold the state required for retrieving file lists via os.path.walk()
    calls.
    """

    def __init__(self, thePattern):
        super(_ListInfoPattern, self).__init__()
        self.pattern = re.compile(thePattern)

    def test(self, currDir, aFileName):
		"""See if 'aFileName' matches the filename pattern."""
		return (os.path.isfile(os.path.join(currDir, aFileName))
            and self.pattern.match(aFileName))


class _ListInfo(object):
    """Just get a file list."""
    
    def test(self, currDir, aFileName):
		"""Test if 'aFileName' is a file."""
		return os.path.isfile(os.path.join(currDir, aFileName))

