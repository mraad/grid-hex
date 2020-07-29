import os
from setuptools import find_packages, setup

where = os.path.join("src", "main", "python")
setup(
    name='gridhex',
    version='2.2',
    description='Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html',
    author='Mansour Raad',
    author_email='mraad@esri.com',
    python_requires='>=2.7',
    packages=find_packages(where=where),
    package_dir={'': where}
)
