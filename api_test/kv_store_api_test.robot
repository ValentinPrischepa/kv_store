*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000/key-value

*** Test Cases ***
Put Entry
    [Documentation]    Test the creation of a new key-value pair.
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${data}=    Create Dictionary    key=testKey    value=testValue
    ${response}=    POST    ${BASE_URL}/key-value    headers=${headers}    json=${data}
    Should Be Equal As Strings    ${response.status_code}    201

Get Entry
    [Documentation]    Test retrieval of a key-value pair.
    ${response}=    GET    ${BASE_URL}/testKey
    Should Be Equal As Strings    ${response.status_code}    200
    Dictionary Should Contain Value    ${response.json()}    testValue

Delete Entry
    [Documentation]    Test deletion of a key-value pair.
    ${response}=    DELETE    ${BASE_URL}/testKey
    Should Be Equal As Strings    ${response.status_code}    200

Verify Deletion
    [Documentation]    Verify that the key-value pair was deleted.
    ${response}=    GET    ${BASE_URL}/testKey
    Should Be Equal As Strings    ${response.status_code}    404
