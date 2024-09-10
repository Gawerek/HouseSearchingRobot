*** Settings ***
Library     SeleniumLibrary
Library     ../Resources/searching.resource
Library     ../python_scripts/scraping_offers.py
Library     Collections

*** Keywords ***
Scrape Offers From Current Page
    [Arguments]     ${ALL_OFFERS}
    # Get the page source and scrape offers
    ${html_content}=    Get Source
    ${offers}=          Scrape Offers With URL    ${html_content}

    # Log scraped offers for debugging purposes
    Log Many            ${offers}

    # Append new offers to the global offer list (as a list of dictionaries)
    FOR    ${offer}    IN    @{offers}
        Append To List    ${ALL_OFFERS}    ${offer}
    END

Scrape All Pages
    [Arguments]    ${ALL_OFFERS}
    FOR    ${i}    IN RANGE    1    2
        Scrape Offers From Current Page     ${ALL_OFFERS}
        # Check if the next page button exists
        ${next_page}=   Check If Next Page Exists
        # If no next page, break the loop
        Run Keyword If    not ${next_page}    Exit For Loop

        # If there is a next page, click the next page button
        Click Next Page Button
    END
    Log Many    ${ALL_OFFERS}

Find Best Offers By Price Per Square Meter
    [Arguments]     ${ALL_OFFERS}    ${n}=10

    # Ensure there are offers to work with
    Run Keyword If    ${ALL_OFFERS} == []    Log To Console    No offers found.

    # Log all offers to inspect them
    Log Many    ${ALL_OFFERS}

    # Get the top n offers by calling the Python function
    ${best_offers}=    Find Best Offer By Price    ${ALL_OFFERS}    ${n}

    RETURN  ${best_offers}
    # Log the best offers
    Log To Console    The best ${n} offers:
    Log Many    ${best_offers}