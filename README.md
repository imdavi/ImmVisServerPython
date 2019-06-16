# ImmVis (Server)

This is the server side project from ImmVis, a platform that aims to connect different data visualization platforms to a data analysis service written in Python.

## Solution archictecture

The platform consists into a GRPC server that exposes some data analysis functions from Python, specifically from [Pandas](https://github.com/pandas-dev/pandas) and [scikit-learn](https://scikit-learn.org). The intent of this is to use Python data analysis capabilities on development environments that aren't to good for that.

Here is a really small architecture diagram about how it works:

"Python" (pandas, scikit-learn, etc) <-> GRPC <-> Clients

(This will be improved in the future)

## Development setup

To develop for the server side, you should have installed [Python](https://www.python.org/) (2.7.+ or 3.+) and [PIP](https://pypi.org/project/pip/) (latest version available). 

If you already have them installed, please install the Python dependencies listed at `requirements.txt` file. If you are not sure how to do that, please run or take a look at the scripts `install_python_dependencies.bat` (Windows) and `install_python_dependencies.sh` (Linux) available on the `utilities` folder.

After installing the dependencies is necessary to run the python libs generation scripts (`generate_python_libs.bat` or `generate_python_libs.sh`) to transform the definitions from the `proto/immvis.proto` definitions into Python bindings. These files aren't versioned to ensure that developers will always generate the libs before running the platform.

After installing the dependencies and generating the server scripts you can run the server running the `run_server.bat` or `run_server.sh`, also available on the `utilities` folder.

## Adding new features

If you are planning to add new features on the platform, please follow the following steps:

1. Create the required data structures or functions on the `proto/immvis.proto` file. If you want more information about how to do that, please check the [GRPC documentation](https://grpc.io/).
1. Run the python libs generation scripts (`generate_python_libs.bat` or `generate_python_libs.sh`) to transform the definitions from the `proto/immvis.proto` definitions into Python bindings. 
1. Extend the class `ImmVisServer` at `immvis/__main__.py` adding the functions created on the proto file. To have more details about how to use GRPC on Python please check this [link](https://grpc.github.io/grpc/python/). Please try to follow the implementation of current features for now, as there are plans to simplify the way of adding new features.
1. Generate the libs for the clients that you are willing to use. Currently we have scripts only to generate libs for C#/Unity3D (`generate_csharp_libs.bat` or `generate_csharp_libs.sh`)

# License

```
MIT License

Copyright (c) 2018 Felipe Pedroso

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```