Introduction
============

If you do not use [Slackware Linux](http://www.slackware.com), you won't find
much use for this program.

This program is designed to support the tool [sbopkg](https://www.sbopkg.org/)
by generating sbopkg queue file much faster than the bash script currently
shipped with sbopkg.

Installation
------------

This code uses [setuptools](https://pypi.python.org/pypi/setuptools), which is 
pretty standard for the python community. The command

	python setup.py bdist_dumb --bdist-dir /tmp/package

when run in the same directory as this file will give similar output as this

	0 ✓ flacy@flacy ~/Documents/sqg $ python setup.py bdist_dumb --bdist-dir /tmp/package
	running bdist_dumb
	running build
	running build_py
	installing to /tmp/package
	running install
	running install_lib
	creating /tmp/package
	creating /tmp/package/usr
	creating /tmp/package/usr/lib64
	creating /tmp/package/usr/lib64/python2.7
	creating /tmp/package/usr/lib64/python2.7/site-packages
	creating /tmp/package/usr/lib64/python2.7/site-packages/sqg
	copying build/lib/sqg/__init__.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg
	creating /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities
	copying build/lib/sqg/utilities/__init__.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities
	copying build/lib/sqg/utilities/TopologicalSortTest.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities
	copying build/lib/sqg/utilities/TopologicalSort.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities
	copying build/lib/sqg/utilities/PropertyReader.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities
	creating /tmp/package/usr/lib64/python2.7/site-packages/sqg/scanning
	copying build/lib/sqg/scanning/__init__.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/scanning
	copying build/lib/sqg/scanning/FileLister.py -> /tmp/package/usr/lib64/python2.7/site-packages/sqg/scanning
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/__init__.py to __init__.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities/__init__.py to __init__.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSortTest.py to TopologicalSortTest.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSort.py to TopologicalSort.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/utilities/PropertyReader.py to PropertyReader.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/scanning/__init__.py to __init__.pyc
	byte-compiling /tmp/package/usr/lib64/python2.7/site-packages/sqg/scanning/FileLister.py to FileLister.pyc
	running install_egg_info
	running egg_info
	writing sqg.egg-info/PKG-INFO
	writing top-level names to sqg.egg-info/top_level.txt
	writing dependency_links to sqg.egg-info/dependency_links.txt
	writing entry points to sqg.egg-info/entry_points.txt
	writing sqg.egg-info/PKG-INFO
	writing top-level names to sqg.egg-info/top_level.txt
	writing dependency_links to sqg.egg-info/dependency_links.txt
	writing entry points to sqg.egg-info/entry_points.txt
	reading manifest file 'sqg.egg-info/SOURCES.txt'
	writing manifest file 'sqg.egg-info/SOURCES.txt'
	Copying sqg.egg-info to /tmp/package/usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info
	running install_scripts
	Installing sqg script to /tmp/package/usr/bin
	Creating tar archive
	removing '/tmp/package' (and everything under it)
	0 ✓ flacy@flacy ~/Documents/sqg $ 

The contents of the resulting tar archive look like

	0 ✓ flacy@flacy ~/Documents/sqg $ tar tf dist/sqg-1.0.linux-x86_64.tar.gz 
	./
	./usr/
	./usr/bin/
	./usr/bin/sqg
	./usr/lib64/
	./usr/lib64/python2.7/
	./usr/lib64/python2.7/site-packages/
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/dependency_links.txt
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/SOURCES.txt
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/top_level.txt
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/PKG-INFO
	./usr/lib64/python2.7/site-packages/sqg-1.0-py2.7.egg-info/entry_points.txt
	./usr/lib64/python2.7/site-packages/sqg/
	./usr/lib64/python2.7/site-packages/sqg/__init__.pyc
	./usr/lib64/python2.7/site-packages/sqg/scanning/
	./usr/lib64/python2.7/site-packages/sqg/scanning/FileLister.pyc
	./usr/lib64/python2.7/site-packages/sqg/scanning/__init__.pyc
	./usr/lib64/python2.7/site-packages/sqg/scanning/FileLister.py
	./usr/lib64/python2.7/site-packages/sqg/scanning/__init__.py
	./usr/lib64/python2.7/site-packages/sqg/utilities/
	./usr/lib64/python2.7/site-packages/sqg/utilities/PropertyReader.pyc
	./usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSort.pyc
	./usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSortTest.pyc
	./usr/lib64/python2.7/site-packages/sqg/utilities/__init__.pyc
	./usr/lib64/python2.7/site-packages/sqg/utilities/PropertyReader.py
	./usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSort.py
	./usr/lib64/python2.7/site-packages/sqg/utilities/TopologicalSortTest.py
	./usr/lib64/python2.7/site-packages/sqg/utilities/__init__.py
	./usr/lib64/python2.7/site-packages/sqg/__init__.py
	0 ✓ flacy@flacy ~/Documents/sqg $ 
