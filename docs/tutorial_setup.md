# Tutorial:  ImmVis Setup

This tutorial covers how to set up and run ImmVis Python Server.

## Requirements

- Operating system: Windows, Linux, or macOS
- Install Python 3.8 or earlier ([download link](https://www.python.org/downloads/))
- Install `pip` ([download link](https://pypi.org/project/pip/))

## Running ImmVis Server

1. Clone [ImmVisServerPython](https://github.com/imdavi/ImmVisServerPython) or download its source code
1. Open a terminal and navigate to the folder where the code was cloned/downloaded
1. Install the [required dependencies](../requirements.txt) by using the `install_python_dependencies`script available on [utilities folder](../utilities) or running the command `pip install -r requirements.txt`
1. Still inside the project folder, run the command `python -m immvis.grpc` (or `python3`).
1. If everything worked fine, you are going to see the following output on the terminal: 
```shell
Creating DataManager
Creating ImmvisGrpcServicer
Creating GRPC server...
Creating Discovery server...
Starting ImmvisGrpcServer...
ImmvisGrpcServer has started!
Starting discovery service.
Broadcasting...
```
1. To finish the server, press `CTRL + C`

Note: if you want to test ImmVis inside an immersive application, please refer to [ImmVisClientLibraryUnity](https://github.com/imdavi/ImmVisClientLibraryUnity) to check samples implemented using the Unity game engine.


## Configuring `IMMVIS_DATASETS` environment variable 

The ImmVis server currently provides the `ListAvailableDatasets` function to list the available datasets from a specific folder. To configure which folder ImmVis Server should scan, you need to have the `IMMVIS_DATASETS` [environment variable](https://en.wikipedia.org/wiki/Environment_variable) set in your operating system. 

If the variable is not available, the framework will look for datasets inside a folder named `datasets` inside the root folder inside this project. If you don't want to set the environment variable, consider just creating the folder and copying the datasets to it.

## Development IDE

This project was developed using [Visual Studio Code](https://code.visualstudio.com/) but feel free to use any Python IDE from your preference.

If you are using Visual Studio Code, please note that we included the launch configuration `Python: Immvis Grpc` to ease the development process.
