from os import path
from codecs import open
from setuptools import setup, find_packages

# we're using a README.md, if you do not have this in your folder, simply
# replace this with a string.
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Here you specify the meta-data of your package. The `name` argument is
# needed in some other steps.
setup(
    name='v6-hads-scoring',
    version="1.0.0",
    description='Vantage6 algorithm that performs hospital anxiety and depression scale (HADS) scoring.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/STRONGAYA/v6-hads-scoring',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'vantage6-algorithm-tools',
        'pandas',
        "vantage6-strongaya-rdf @ git+ssh://github.com/STRONGAYA/v6-tools-rdf.git@v0.1.0",
        "vantage6-strongaya-instruments-licenced @ git+ssh://github.com/STRONGAYA/v6-tools-instruments-licenced.git@v0.1.0"
    ]
)
