This is Uao (UA Objects), for C++ clients and for Quasar-based OPC-UA servers

Author: Piotr Nikiel <piotr.nikiel@gmail.com>

--- UA Objects ---

UA Objects is an approach to create OPC-UA client(s) using a'priori information of 
the OPC-UA information schema which they will serve.
Therefore the obtained client(s) are somehow specific to the particular application.

Pros:
- you don't have to know how to make OPC-UA clients, the tool will generate them for you
- you get type safety, error handling and other nice stuff 'for free'

Cons:
- the client(s) are specific to the application (which might not be a problem, actually)
- there might be situations in which the tool can't cover all of your requirements. 
For example, OPC-UA permits to send multiple requests to the Read Service, but
the current version of UaoForQuasar handles only single requests.

Requirements:
- the generated client depends on the UASDK API for OPC-UA clients
It's best to use the UASDK, of course:
https://www.unified-automation.com/products/server-sdk/c-ua-server-sdk.html

If you don't have the paid UASDK license, we tested this project with the evaluation license,
which can help you see if the overall solution is satisfactory for you.


--- How does it work ---

1. You always start with a quasar-based OPC-UA server project.
Create a quasar project, or use an existing one.
Quasar reference: https://github.com/quasar-team/quasar

2. Add this project as a git submodule to your OPC-UA server:

git submodule add https://github.com/quasar-team/UaoForQuasar.git

git submodule update

3. Generate a client class per Quasar class, e.g. for Quasar class "MyClass" (defined in quasar's Design.xml):

python UaoForQuasar/generateClass.py MyClass

The client class header and body will be places into UaForQuasar/output

4. At this stage you can use your client class. 
Please look into demo/ directory where a simple, CMake-based project which integrated generated classes
in some simple demo client. To compile it, go to build and then:

cmake ../

make

Note that you might need to adjust demo.cpp according to the quasar class you want to talk to.
Note that you might need to adjust CMakeLists.txt for the UASDK paths etc.


