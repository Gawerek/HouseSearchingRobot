*** Settings ***
Library             SeleniumLibrary
Library             DebugLibrary

Resource            ../Resources/searching.resource
Resource            ../Resources/scrapping.resource
Suite Setup         Open Browser With Custom Profile



*** Test Cases ***
Searching in otodom
    ${ALL_OFFERS}=    Create Dictionary
    Click Type Dropdown
    Select Type Dropdown Option    Domy
    Select Distance From list    css-100wgto   + 10 km
    Enter City in Input    Wpisz lokalizację    Warszawa
    Select City On List   Warszawa
    Enter Min Price     400000
    Enter Max Price     800000
    Click Wyszukaj
    Click Element By Partial Text       Data dodania: najnowsze
    Select Type Dropdown Option    Cena: od najniższej
    Scrape All Pages    ALL_OFFERS=${ALL_OFFERS}
    Log Many    &{ALL_OFFERS}
    Find Best Offer By Price Per Square Meter   &{ALL_OFFERS}
    [Teardown]    Close Browser



