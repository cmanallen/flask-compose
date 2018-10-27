import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='flask_compose',
    version='0.2.0',
    author='Colton Allen',
    author_email='colton.allen@caxiam.com',
    description='A routing library for flask applications obeying the "Decorator Design Pattern".',
    long_description=long_description,
    url='https://github.com/cmanallen/flask_router',
    packages=setuptools.find_packages(),
    install_requires=['flask'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
