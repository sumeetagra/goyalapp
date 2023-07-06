from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in goyalapp/__init__.py
from goyalapp import __version__ as version

setup(
	name="goyalapp",
	version=version,
	description="Business App for Goyal Group",
	author="Go4all Technologies Pvt Ltd",
	author_email="admin@goyalironsteel.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
