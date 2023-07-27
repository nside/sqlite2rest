from setuptools import setup, find_packages

# Read the contents of the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sqlite2rest',
    version='1.2.0',
    description='A Python library for creating a RESTful API from an SQLite database using Flask.',
    author='Denis Laprise',
    author_email='git@2ni.net',
    url='https://github.com/nside/sqlite2rest',
    packages=find_packages(),
    install_requires=[
        'flask==2.3.2',
        'openapi-spec-validator==0.6.0',
        'pyyaml==6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'sqlite2rest=sqlite2rest.__main__:main',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
