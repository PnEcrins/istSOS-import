import setuptools

setuptools.setup(
    name="istsos-import",
    description="Import module for IstSOS software",
    maintainer="Parcs national des Écrins",
    python_requires=">=3.6",
    packages=setuptools.find_packages(where="src", include=["istsos*"]),
    install_requires=list(open("requirements.txt", "r")),
    package_dir={
        "": "src",
    },
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
