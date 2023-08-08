import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="queue-event-handler",
    install_requires=["chalice"],
    version="1.5.0",
    author="Joaquín Grez",
    author_email="joaco@tether.education",
    description=("Thin wrapper for AWS Queues"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TetherEducation/queue-event-handler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
)
