from setuptools import setup, find_packages

setup(
	name='cgtool',
	version='1.0',
	author='Peppy Sisay',
	license='MIT',
	packages=find_packages(),
	py_modules=['cgtool'],
	include_package_data=True,
	install_requires=[
		'Click'
	],
	entry_points='''
		[console_scripts]
		cgtool=cgtool:cli
	'''
)
