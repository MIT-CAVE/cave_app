from distutils.core import setup
from setuptools import find_packages

setup(
    name="cave_api",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    version="0.0.1",
    license="MIT",
    description="Python wrapper for api use in the cave_app",
    author="Connor Makowski",
    author_email="conmak@mit.edu",
    url="https://github.com/mit-cave/cave_server/cave_api",
    download_url="https://github.com/mit-cave/cave_server/cave_api/dist/cave_api-0.0.1.tar.gz",
    keywords=["data", "api", "cave", "app"],
    install_requires=["scoptimize==0.0.3", "type_enforced>=0.0.4"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
