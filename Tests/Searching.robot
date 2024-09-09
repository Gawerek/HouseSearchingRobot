*** Settings ***
Library             SeleniumLibrary
Library             DebugLibrary

Resource            ../Resources/searching.resource
Resource            ../Resources/scrapping.resource
Test Setup         Open Browser With Custom Profile

*** Test Cases ***
Searching in otodom mieszkania
    ${ALL_OFFERS}=    Create List
    Click Type Dropdown
    Select Type Dropdown Option    Mieszkania
#    Select Distance From list    css-100wgto   + 10 km
    Enter City in Input    Wpisz lokalizację    Warszawa
    Select City On List   Warszawa
    Enter Min Price     400000
    Enter Max Price     800000
    Enter Min Area      55
    Click Wyszukaj
    Handle Sorting Options
    Select Type Dropdown Option    Cena: od najniższej
    Scrape All Pages    ${ALL_OFFERS}
    Log Many    ${ALL_OFFERS}
    ${best_offers}=     Find Best Offers By Price Per Square Meter   ${ALL_OFFERS}    10
    Save Offers To Excel    ${best_offers}    mieszkania.xlsx
    [Teardown]    Close Browser

Searching in otodom
    ${ALL_OFFERS}=    Create List
    Click Type Dropdown
    Select Type Dropdown Option    Domy
    Select Distance From list    css-100wgto   + 10 km
    Enter City in Input    Wpisz lokalizację    Warszawa
    Select City On List   Warszawa
    Enter Min Price     400000
    Enter Max Price     800000
    Click Wyszukaj
    Handle Sorting Options
    Select Type Dropdown Option    Cena: od najniższej
    Scrape All Pages    ${ALL_OFFERS}
    Log Many    ${ALL_OFFERS}
    ${best_offers}=     Find Best Offers By Price Per Square Meter   ${ALL_OFFERS}    10
    Save Offers To Excel    ${best_offers}    domy.xlsx
    [Teardown]    Close Browser




*** Keywords ***
Handle Sorting Options
    Run Keyword And Ignore Error    Click Element By Partial Text    Data dodania: najnowsze
    Run Keyword And Ignore Error    Click Element By Partial Text    Najlepiej dopasowane
