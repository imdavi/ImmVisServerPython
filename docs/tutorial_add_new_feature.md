# Tutorial:  Adding a new feature to ImmVis

This tutorial shows how to implements a new feature to the ImmVis framework on the server and Unity client library.

The feature to be implemented is the `correlation matrix`, using the function [pandas.DataFrame.corr](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html) to find the correlation between the dimensions of a given dataset.

## Requirements

- Operating system: Windows, Linux, or macOS
- Download the [ImmVisServerPython](https://github.com/imdavi/ImmVisServerPython) source code and follow its setup instructions
- Download the [ImmVisClientLibraryUnity](https://github.com/imdavi/ImmVisClientLibraryUnity) source code and follow its setup instructions

## GRPC References

Adding a new feature on ImmVis consists of adding a new GRPC service on the server-side (Python) and then updating the client library (Unity) with the newly implemented function.

For more references about how to use GRPC, please refer to the GRPC documentation for [Python](https://grpc.io/docs/languages/python/basics/) and [C#](https://grpc.io/docs/languages/csharp/basics/).

If you want to implement a client in any other language, please refer to the [GRPC Supported Languages documentation](https://grpc.io/docs/languages/).

## Creating the feature on ImmVisServerPython

1. On the `ImmVisServerPython` folder, add the code below to the DataManager class (`immvis/data/data_manager.py`). Please follow the exact indentation of the other functions.

```python
    def get_correlation_matrix(self):
        return self.data_frame.corr()
```

2. Create the following funtion on the `ImmVisPandas` service (`proto\immvis.proto`)
```proto
syntax = "proto3";

service ImmVisPandas {
    …
    rpc GetCorrelationMatrix(Empty) returns (CorrelationMatrix) {}
}
```

We will call our function `GetCorrelationMatrix`,  making it receive an `Empty` parameter and return a `CorrelationMatrix`. If you need to add other parameters than `Empty`, please refer to the other existing functions to create custom parameters for your case. We also recommend visiting the gRPC documentation mentioned earlier.

3. Create the `CorrelationMatrix` and `CorrelationMatrixRow` messages at the end of the proto file (`proto\immvis.proto`):
```proto
message CorrelationMatrix {
    repeated CorrelationMatrixRow rows = 1;
}

message CorrelationMatrixRow {
    string column1 = 1;
    string column2 = 2;
    float correlationCoeficient = 3;
}
```

4. Run the command `.\utilities\generate_python_libs.bat` (Windows) or `./utilities/generate_python_libs.sh` (Linux/Mac) in order to generate the GRPC python libraries on `immvis\grpc\proto`

5. Open the file `immvis\grpc\proto\immvis_pb2_grpc.py` and change the line `import immvis_pb2 as immvis__pb2` to `from . import immvis_pb2 as immvis__pb2`. Ignore the other errors and save the file. We are currently working to make this step automatic in the future.

6. Create the file `immvis\grpc\mappers\correlation_matrix.py` with the following content:
```Python
from ..proto.immvis_pb2 import CorrelationMatrix, CorrelationMatrixRow
from pandas import DataFrame, Series

def map_correlation_matrix(data_frame: DataFrame) -> CorrelationMatrix:
    rows = []

    for index in data_frame.index.values:
        row = data_frame.loc[index]
        for column_index in row.index.values:
            coeficient = row.loc[column_index]
            rows.append(CorrelationMatrixRow(column1=str(index), column2=str(column_index), correlationCoeficient=coeficient))

    return CorrelationMatrix(rows = rows)
    
```
7. Add the following line to `immvis\grpc\mappers\__init__.py`:
```python
from .correlation_matrix import map_correlation_matrix
```

8. Open `immvis\grpc\immvis_grpc_servicer.py` and update the mappers import line with `map_correlation_matrix` created on the previous step:
```python
from .mappers import get_dataset_metadata, map_correlation_matrix
```

9. Still on `immvis\grpc\immvis_grpc_servicer.py`, add the following method to the `ImmvisGrpcServicer` class:
```python
class ImmvisGrpcServicer(immvis_pb2_grpc.ImmVisPandasServicer):

    …

    def GetCorrelationMatrix(self, request, context):
        correlation_matrix = self._data_manager.get_correlation_matrix()

        return map_correlation_matrix(correlation_matrix)
```

## Updating ImmVis Unity3D Client Library

1. Still inside the server project, run the command `.\utilities\generate_csharp_libs.bat` (Windows) or `./utilities/generate_python_libs.sh` (Linux/Mac) in order to generate the ImmVis GRPC C#  files (`csharp\Immvis.cs` and `csharp\ImmvisGrpc.cs`)

2. Open the project using Unity3D and navigate to the `Assets\ImmVisClientGrpcUnity\Scripts\ImmVis\Grpc\Generated` folder

3. Replace the files `Assets\ImmVisClientGrpcUnity\Scripts\ImmVis\Grpc\Generated\Immvis.cs` and `Assets\ImmVisClientGrpcUnity\Scripts\ImmVis\Grpc\Generated\ImmvisGrpc.cs` by the ones that were generated on the step 1.

4. To test if everything worked, open the `Assets\ImmVisClientGrpcUnity\Examples\BasicUsage\ExampleSceneBehaviour.cs` file, add the line `var correlationMatrix = await grpcClient.GetCorrelationMatrix(new Empty());` after the dataset is loaded.
```csharp
// Add the code below this line:
Debug.Log($"Loaded a dataset:\n{datasetInfoStringBuilder.ToString()}");

// Code to be added:
var correlationMatrix = await grpcClient.GetCorrelationMatrix(new Empty());

// Using the correlation matrix
Debug.Log($"Using:\n{correlationMatrix}");

```
5. [Run the server](https://github.com/imdavi/immvis-server-grpc#running-the-server) and then run the Unity3D project to check the project will build correctly.

6. If everything worked correctly, the project will run, with logs available on the Unity console.
