from setuptools import setup, find_packages

setup(
	name='Performance',
	version='1.0',
	author='Peppy Sisay',
	license='MIT',
	packages=find_packages(),
	py_modules=['performance'],
	include_package_data=True,
	install_requires=[
		'Click'
	],
	entry_points='''
		[console_scripts]
		performance=performance:cli
	'''
)
