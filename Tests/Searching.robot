*** Settings ***
Library             SeleniumLibrary
Library             DebugLibrary

Resource            ../Resources/searching.resource
Suite Setup         Open Browser With Custom Profile



*** Test Cases ***
Searching in otodom
    Click Type Dropdown
    Select Type Dropdown Option    Domy
    Select Distance From list    css-100wgto   + 15 km     
    Enter City in Input    Wpisz lokalizację    Warszawa
    Select City On List   Warszawa
    Enter Max Price     900000
    Click Wyszukaj
    Sleep    3
    [Teardown]    Close Browser



