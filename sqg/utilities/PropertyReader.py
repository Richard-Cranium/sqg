import StringIO
import ConfigParser
import subprocess
    

class PropertyReader(object):
	""" Read standard bash property files."""
	def __init__(self):
		pass

	def read(self, filename):
		"""There is a fast way that works most of the time and a slower way that
		works all of the time.
		Try the faster way first; if it fails, try the slower way.
		"""
		try:
			with open(file_path) as f:
				config = StringIO.StringIO()
				config.write('[dummy_section]\n')
				config.write(f.read().replace('%', '%%'))
				config.seek(0, os.SEEK_SET)

				cp = ConfigParser.SafeConfigParser()
				cp.readfp(config)

				return dict(cp.items('dummy_section'))
		except:
			retval = {}
			command = ['/bin/ash', '-c', 'set -a && . ' + filename + ' && env']
			proc = subprocess.Popen(command, stdout = subprocess.PIPE)
			for line in proc.stdout:
				(key, _, val) = line.partition('=')
				retval[key.lower()] = val
			return retval


	def readBash(self, filename):
		"""Just use the bash shell to expand and read the provided file."""
		retval = {}
		command = ['/bin/bash', '-c', 'set -a && . ' + filename + ' && env']
		proc = subprocess.Popen(command, stdout = subprocess.PIPE)
		for line in proc.stdout:
			(key, _, val) = line.partition('=')
			retval[key] = val
		return retval