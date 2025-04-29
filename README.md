# UaoForQuasar - UA Objects for quasar-based OPC UA Servers

UaoForQuasar (UA Objects) is a code generation tool that creates type-safe OPC UA client classes in C++ based on quasar server designs. It simplifies OPC UA client development by generating client code that matches your quasar server's information model.

## Overview

UA Objects uses a priori information from your OPC UA server's information schema to generate client classes that are specifically tailored to your application. This approach provides several benefits:

### Advantages
- **No OPC UA expertise required** - Create type-safe OPC UA clients without deep protocol knowledge
- **Type safety** - Generated code ensures type correctness at compile time
- **Error handling** - Built-in error handling for OPC UA operations
- **Clean abstraction** - Use your OPC UA server's objects directly in client code

### Limitations
- Client classes are specific to your quasar application design
- Currently handles only single requests to OPC UA Read Service (not batch operations)
- Requires Unified Automation SDK (UASDK)

## Requirements

- **quasar Framework** - UaoForQuasar must be deployed in a quasar project
  - Reference: https://github.com/quasar-team/quasar
- **Unified Automation SDK** - The generated client code depends on UASDK
  - Commercial: https://www.unified-automation.com/products/server-sdk/c-ua-server-sdk.html
  - Evaluation license available for testing
- **Python Dependencies**
  - Jinja2 (templating engine)
  - colorama (terminal coloring)
  - pyuaf (OPC UA Access Framework)

## Quick Start

### 1. Add UaoForQuasar to your quasar project

```bash
# In your quasar project directory
git submodule add https://github.com/quasar-team/UaoForQuasar.git
git submodule update
```

### 2. Generate client classes

Generate a client class for each quasar class you want to access:

```bash
python UaoForQuasar/generateClass.py MyClass
```

You can specify a C++ namespace for your generated code:

```bash
python UaoForQuasar/generateClass.py --namespace MyProject MyClass
```

Generated files will be placed in `UaoForQuasar/generated/`.

### 3. Use the generated client

The following example shows how to use a generated client class:

```cpp
#include <ClientSessionFactory.h>

// Include your generated client class
#include <MyClass.h>

#include <uaplatformlayer.h>
#include <iostream>

int main()
{
    UaPlatformLayer::init();

    UaClientSdk::UaSession* session = ClientSessionFactory::connect("opc.tcp://127.0.0.1:4841");
    if (!session)
        return -1;

    MyClass myObject(session, UaNodeId("instance1", 2));
    
    std::cout << "Value = " << myObject.readMyVariable() << std::endl;
    
    return 0;
}
```

## Demo Application

A demo application is included to show how to use the generated client code:

1. Navigate to the demo directory
2. Adjust `demo.cpp` to use your generated class
3. Modify `CMakeLists.txt` to set the correct paths for UASDK
4. Build the demo:

```bash
cd UaoForQuasar/demo/build
cmake ../
make
```

## Contact

For questions or issues, contact: paris.moschovakos@cern.ch