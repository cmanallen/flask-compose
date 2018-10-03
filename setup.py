from setuptools import find_packages, setup


setup(
    name='flask_router',
    version='0.0.1',
    url='https://github.com/cmanallen/flask_router',
    license='Apache Version 2.0',
    author='Colton Allen',
    author_email='colton.allen@caxiam.com',
    long_description=__doc__,
    packages=find_packages(exclude=("tests*", "examples*")),
    package_dir={'flask_router': 'flask_router'},
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
