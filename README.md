# ImmVis (Server)

This is the server side project from ImmVis, a platform that aims to connect different data visualization platforms to a data analysis service written in Python.

## Solution archictecture

The platform consists into a GRPC server that exposes some data analysis functions from Python, specifically from [Pandas](https://github.com/pandas-dev/pandas) and [scikit-learn](https://scikit-learn.org). The intent of this is to use Python data analysis capabilities on development environments that aren't to good for that.

Here is a really small architecture diagram about how it works:

![Image of Yaktocat](imgs/highlevel-architecture.png)

## Setup

To develop for the server side, you should have installed [Python](https://www.python.org/) (3.6+) and [PIP](https://pypi.org/project/pip/) (latest version available). 

If you already have them installed, please install the Python dependencies listed at `requirements.txt` file. If you are not sure how to do that, please run or take a look at the scripts `install_python_dependencies.bat` (Windows) and `install_python_dependencies.sh` (Linux/MacOS) available on the `utilities` folder.

## Running the server

Currently there are two ways of running the server: 

* From the root directory of the project run the following command: `python -m immvis.grpc`
* Open the root folder with [Visual Studio Code](https://code.visualstudio.com/) and run the debug task `Python: Immvis Grpc`

## Loading data sets

The method `LoadDataset` is currently able to load data sets using a local path or remote URL as `datasetPath` parameter. In order to ease the process of selecting the available data sets locally, the framework includes a function called `ListAvailableDatasets` that is able to scan any path set on the the environment variable `IMMVIS_DATASETS`. If this environment variable is not configured, the function will search for the files inside a folder named `datasets` on the root folder of this project.

The supported formats are: CSV (with comma separator), XLS and JSON.

## Available Client Libraries:

* [Unity3D](https://github.com/imdavi/immvis-client-grpc-unity)

## Tutorials

* [Adding a new feature to ImmVis](docs/tutorial_add_new_feature.md)

## Contributing

Our model of contribution is similar to the one described on https://github.com/firstcontributions/first-contributions, with the difference that members of IMDAVI don't need to create a fork from this repository, only create a branch here to submit their pull-requests.