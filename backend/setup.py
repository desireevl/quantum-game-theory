from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
  
setup(
    name='quantum-game-theory',
    version='0.0.0',
    install_requirements=requirements,
    long_description=open('README.md').read(),
    packages=find_namespace_packages(),
)
