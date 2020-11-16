import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "mp_boilerplate",
    version = "0.2.1",
    author = '@markanewman',
    author_email = 'mp_boilerplate@trinetteandmark.com',
    description = 'A collection of patterns to use over top of the built in multiprocessing package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/markanewman/mp_boilerplate",
    project_urls = {
        'Bug Reports': 'https://github.com/markanewman/mp_boilerplate/issues',
        'Source': 'https://github.com/markanewman/mp_boilerplate',
    },
    packages = setuptools.find_packages(),
    classifiers = [        
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    python_requires = '>=3.6, <4',
    install_requires = [
        "typeguard>=2.7.1,<3.0.0"]
)