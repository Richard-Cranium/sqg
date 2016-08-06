#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="sqg",
      version=1.0,
      description="Python based sbopkg queue file generator.",
      author="Mark A. Flacy",
      url = "none",
      author_email="mflacy@verizon.net",
      packages = find_packages(),
      entry_points = {
		'console_scripts': [
			'sqg = sqg:doit'
		]
	  },
	  test_suite="sqg.utilities.TopologicalSortTest",
      long_description = "sbopkg queue file generator."
    )

