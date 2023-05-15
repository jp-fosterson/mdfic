from setuptools import find_packages, setup

README = open('README.md').read()

setup(
    name='mdfic'
    , version='1.0.0a0'
    , author='JP Fosterson'
    , author_email='jp.fosterson@gmail.com'
    , description=README.split('\n')[0]
    , long_description=README
    , packages=find_packages(exclude=['test', 'test.*', '*.test', '*.test.*'])
    , install_requires=[
        'click',
        'markdown',
        'python-docx',
        'PyYAML',
        ]
    , entry_points = {
        'console_scripts' : ['mdfic=mdfic.cli:cli']
    }

)
