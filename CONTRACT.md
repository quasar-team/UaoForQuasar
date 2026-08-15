# CONTRACT.md

UaoForQuasar is written exactly once against the client surface below, which was
verified stable across every supported Unified Automation C++ SDK tree. The
templates and the supplementary C++ use nothing outside this surface, contain no
SDK version or backend conditionals, and include every SDK header prefix-free
(for example `#include <uaclientsdk.h>`, `#include <uasession.h>`,
`#include <uavariant.h>`), matching the SDK's own internal convention. The build
supplies the include directories through the Client component of quasar's
`cmake/FindOpcUaToolkit.cmake`, which also computes the link closure. No toolkit
path, library name or include directory appears anywhere in this repository.

## Half 1: SDK symbols used by templates and supplementary C++

Session services (namespace `UaClientSdk`):

| Symbol | Used as |
|---|---|
| `UaSession` | `connect(url, SessionConnectInfo, SessionSecurityInfo, UaSessionCallback*)`, `read(ServiceSettings, maxAge, timestamps, UaReadValueIds, UaDataValues, UaDiagnosticInfos)`, `write(ServiceSettings, UaWriteValues, UaStatusCodeArray, UaDiagnosticInfos)`, `call(ServiceSettings, CallIn, CallOut)` |
| `SessionConnectInfo` | fields `sApplicationName`, `sApplicationUri`, `sProductUri` |
| `SessionSecurityInfo` | default-constructed only |
| `UaSessionCallback` | base of `MyCallBack`; only the pure virtual `connectionStatusChanged(OpcUa_UInt32, UaClient::ServerStatus)` is implemented |
| `UaClient::ServerStatus` | callback argument type |
| `ServiceSettings` | default-constructed |
| `CallIn` | fields `objectId`, `methodId`, `inputArguments` |
| `CallOut` | field `outputArguments` |

Value, status and array types:

| Symbol | Used as |
|---|---|
| `UaNodeId` | `(UaString, ns)` constructor, `identifierString()`, `namespaceIndex()`, `copyTo()` |
| `UaString` | construction from `const char*`, `operator+`, `toUtf8()` |
| `UaStatus` | construction from `OpcUa_StatusCode`, `isBad()`, `isGood()`, `statusCode()`, `toString()` |
| `UaDateTime` | assignment from `UaDataValue` timestamps |
| `UaVariant` | value construction, `copyTo()`, `toString()`, `setByteString(UaByteString&, OpcUa_Boolean)`, plus the scalar and array setters and converters enumerated in Half 2 |
| `UaByteString` | pass-through value type |
| `UaDataValue` | fields `Value`, `StatusCode`, `SourceTimestamp`, `ServerTimestamp` |
| `UaReadValueIds`, `UaWriteValues`, `UaDataValues`, `UaDiagnosticInfos`, `UaStatusCodeArray` | `create(n)`, `operator[]` |
| `UaByteArray`, `UaStringArray` | array carriers in `ArrayTools` |
| `UaPlatformLayer` | `init()` in the demo |

Constants (the three): `OpcUa_Attributes_Value`, `OpcUa_TimestampsToReturn_Both`,
`OpcUa_Good`.

Primitive typedefs: `OpcUa_StatusCode`, `OpcUa_Boolean`, `OpcUa_Byte`,
`OpcUa_SByte`, `OpcUa_Int16`, `OpcUa_UInt16`, `OpcUa_Int32`, `OpcUa_UInt32`,
`OpcUa_Int64`, `OpcUa_UInt64`, `OpcUa_Float`, `OpcUa_Double`.

## Half 2: generator tables that emit the surface

`Oracle.DataTypeToVariantSetter` (scalar write and method input path):

| quasar type | `UaVariant` setter |
|---|---|
| `OpcUa_Double` | `setDouble` |
| `OpcUa_Float` | `setFloat` |
| `OpcUa_Byte` | `setByte` |
| `OpcUa_SByte` | `setSByte` |
| `OpcUa_Int16` | `setInt16` |
| `OpcUa_UInt16` | `setUInt16` |
| `OpcUa_Int32` | `setInt32` |
| `OpcUa_UInt32` | `setUInt32` |
| `OpcUa_Int64` | `setInt64` |
| `OpcUa_UInt64` | `setUInt64` |
| `OpcUa_Boolean` | `setBool` |
| `UaString` | `setString` |
| `UaByteString` | special-cased to `setByteString(data, false)` |

`Oracle.DataTypeToVariantConverter` (read and method output path, emitted via
`Delphi.readPronouncementToType`):

| quasar type | `UaVariant` converter |
|---|---|
| `OpcUa_Double` | `toDouble` |
| `OpcUa_Float` | `toFloat` |
| `OpcUa_Byte` | `toByte` |
| `OpcUa_SByte` | `toSByte` |
| `OpcUa_Int16` | `toInt16` |
| `OpcUa_UInt16` | `toUInt16` |
| `OpcUa_Int32` | `toInt32` |
| `OpcUa_UInt32` | `toUInt32` |
| `OpcUa_Int64` | `toInt64` |
| `OpcUa_UInt64` | `toUInt64` |
| `OpcUa_Boolean` | `toBool` |
| `UaString` | special-cased to `toString()` |
| `UaByteString` | `toByteString` |

Array arguments and return values route through
`Oracle.vector_to_uavariant_function` and `Oracle.uavariant_to_vector_function`
into `ArrayTools` (`convertVectorToUaVariant`, `convertUaVariantToVector`, and
the `Boolean` and `Byte` specialisations), which in turn use the `UaVariant`
array members `setBoolArray`, `setByteArray`, `setSByteArray`, `setInt16Array`,
`setUInt16Array`, `setInt32Array`, `setUInt32Array`, `setInt64Array`,
`setUInt64Array`, `setFloatArray`, `setDoubleArray`, `setStringArray` and their
`to*Array` counterparts.

## Known limitation

Generated method calls build the methodId as
`UaNodeId(<objectId>.<methodName>, 2)` with the namespace index fixed at 2,
while reads and writes take the namespace index from the object's NodeId. An
object living in any other namespace gets its methods addressed in namespace 2.
This predates the redesign and is frozen as-is; changing it alters generated
bodies and needs its own regeneration round.

## Contract growth

Any new SDK symbol used by the templates or the supplementary C++ must first be
shown present in every supported UASDK tree and in open62541-compat. Until both
hold, it does not ship.

## Callback discipline

`MyCallBack` implements only `connectionStatusChanged`, the pure virtual of
`UaSessionCallback`. Overriding any optional `UaSessionCallback` virtual is out
of contract: their names and signatures reshuffled across SDK versions, so such
an override silently stops being called when the toolkit changes.

## open62541-compat backend (experimental)

The Client component of `FindOpcUaToolkit.cmake` also resolves an
open62541-compat install, linking `libopen62541-compat`, `open62541`, `LogIt`
and `pthread`. The same sources compile against it, with these semantic
caveats:

- `SessionSecurityInfo` is a stub: no secure endpoints, connections are
  unencrypted regardless of what the struct is set to.
- `connectionStatusChanged` never fires: compat has no session watchdog and
  never invokes the callback. Disconnects surface as bad statuses on the next
  service call.
- `ClientSessionFactory::tryConnect` polling works: it relies on the `connect`
  return status only.
- As of open62541-compat v1.5.12 `UaSessionCallback` is an empty stub that does
  not declare `connectionStatusChanged`, so `MyCallBack`'s `override` does not
  compile there. The compat row goes green once compat declares the pure
  virtual; that one-line growth is the only compat change this contract needs.
- No subscriptions and no security growth are planned for the compat row.
