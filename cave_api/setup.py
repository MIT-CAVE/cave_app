from distutils.core import setup

setup(
    name="cave_api",
    packages=["cave_api"],
    package_data={"": ["*.json", "*.csv"]},
    version="0.0.1",
    license="MIT",
    description="Python wrapper for api use in the cave_app",
    author="Connor Makowski",
    author_email="conmak@mit.edu",
    url="https://github.com/mit-cave/cave_app/cave_api",
    keywords=["data", "api", "cave", "app"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
