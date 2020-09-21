import os
from setuptools import find_packages, setup

where = os.path.join("src", "main", "python")
setup(
    name='gridhex',
    version='2.4',
    description='Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html',
    author='Mansour Raad',
    author_email='mraad@esri.com',
    python_requires='>=3.6',
    install_requires=["numba>=0.49.1"],
    packages=find_packages(where=where),
    package_dir={'': where}
)
