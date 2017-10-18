This is Uao (UA Objects), for C++ clients and for Quasar-based OPC-UA servers

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
and there is an evaluation version which might help you to see if it satisfies your needs.


--- How does it work ---
1. You start with a quasar-based OPC-UA server

https://github.com/quasar-team/quasar