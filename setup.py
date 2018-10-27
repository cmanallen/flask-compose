import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='flask_router',
    version='0.1.0',
    author='Colton Allen',
    author_email='colton.allen@caxiam.com',
    description='A flask routing library.',
    long_description=long_description,
    url='https://github.com/cmanallen/flask_router',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
