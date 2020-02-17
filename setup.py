import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="i3alerts",
    version="0.0.1",
    author="Robert Stein",
    author_email="robert.stein@desy.de",
    description="Package for analysis of IceCube Realtime alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="astroparticle physics science IceCube neutrino multimessenger",
    url="https://github.com/robertdstein/i3alerts",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.16.0",
        "matplotlib",
        "astropy",
        "flarestack>=2.0.2",
        "pandas",
        "sphinx",
        "jupyter",
        "coveralls"
    ],
    package_data={'i3alerts': [
        'effective_area/alerts_v2/*/*.csv']},
    include_package_data=True
)