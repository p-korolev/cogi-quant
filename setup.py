from setuptools import setup, find_packages 

setup(
    name='cogi-quant',
    version='1.0.0',
    packages=find_packages(),
    instal_requires=['pandas', 'numpy', 'scipy', 'matplotlib'],
    author='Phillip Korolev',
    description='Toolkit for quantitative market analysis',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)

