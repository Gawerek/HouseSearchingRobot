*** Settings ***
Library     SeleniumLibrary
Library     ../Resources/searching.resource
Library     ../python_scripts/scraping_offers.py
Library     Collections

*** Keywords ***
Scrape Offers From Current Page
    [Arguments]     &{ALL_OFFERS}
    # Get the page source and scrape offers
    ${html_content}=    Get Source
    ${offers}=          Scrape Offers With URL    ${html_content}

    # Log scraped offers for debugging purposes
    Log Many            &{offers}

    # Append new offers to the global offer list
    FOR    ${key}    IN    @{offers}
        Set To Dictionary    &{ALL_OFFERS}    ${key}=${offers[${key}]}
    END


Scrape All Pages
    [Arguments]    &{ALL_OFFERS}
    FOR    ${i}    IN RANGE    1    2
        Scrape Offers From Current Page     &{ALL_OFFERS}
        #Check if the next page button exists
        ${next_page}=   Check If Next Page Exists
        #If no next page, break the loop
        Run Keyword Unless    ${next_page}    Exit For Loop

        #If there is a next page, click the next page button
        Click Next Page Button

    END

Find Best Offer By Price Per Square Meter
    [Arguments]     &{ALL_OFFERS}
    #Correct assignment of multiple return values
    ${BEST_OFFER}=      Set Variable    ${EMPTY}
    ${BEST_OFFER_URL}=    Set Variable    ${EMPTY}

    # Assign the results from the keyword to two separate variables
    ${BEST_OFFER}    ${BEST_OFFER_URL}=   Find Best Offer By Price    &{ALL_OFFERS}
    # Log the results to the console
    Log To Console    The best price per square meter is: ${BEST_OFFER}
    Log To Console    The URL of the best offer is: ${BEST_OFFER_URL}
