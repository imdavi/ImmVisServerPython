# ImmVis (Server)

This project is the server-side part from ImmVis, an open-source framework that aims to provide data services to Immersive Analytics. The framework is built on top of [gRPC](https://grpc.io/), enabling different platforms and programming languages to use the data analysis libraries from the Python ecosystem.

## Tutorials

* [ImmVis Server Setup](docs/tutorial_setup.md)
* [Adding a new feature to ImmVis](docs/tutorial_add_new_feature.md)

## Running the server

After doing the [ImmVis Server Setup](docs/tutorial_setup.md), you could run the server using one of the following options: 

* From the project's root directory, run the following command: `python -m immvis.grpc`
* Open the root folder with [Visual Studio Code](https://code.visualstudio.com/) and run the debug task `Python: Immvis Grpc`

## Client Libraries

To use the ImmVis server with your application, you have two options:

* Generate the gRPC code using the [Protobuf services definition file](./proto/immvis.proto) and use it inside your application. Please refer to [gRPC documentation](https://grpc.io/docs/languages/) for more details about how to do it for your programming language.
* Integrate one of the available client libraries to your project:
  * [Unity3D](https://github.com/imdavi/immvis-client-grpc-unity)

## Supported dataset formats

Currently, ImmVis uses [pandas](https://pandas.pydata.org/) to load datasets with the following formats:

* CSV (with semicolon separator)
* XLS
* JSON

If you need to change or configure something with pandas to load your dataset (e.g., change the separator), please refer to the [load_dataset.py](./immvis/data/utils/load_dataset.py) file.

## Contributing

Our contribution model is similar to the one described on https://github.com/firstcontributions/first-contributions, with the difference that members of IMDAVI don't need to create a fork from this repository, only create a branch here to submit their pull-requests.