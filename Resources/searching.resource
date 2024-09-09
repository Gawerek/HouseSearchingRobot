*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${HOME_URL}         https://www.otodom.pl
${BROWSER}          Firefox


*** Keywords ***
Open Browser With Custom Profile
    Open Browser    ${HOME_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    id=onetrust-accept-btn-handler
    Click Button    id=onetrust-accept-btn-handler

Click Type Dropdown
    # Click the dropdown control element
    Click Element    css:.react-select__control

Select Type Dropdown Option
    # Select the option by its text
    [Arguments]     ${estate_type}
    Click Element    xpath=//div[@role='option' and text()='${estate_type}']


Select Distance From list
    [Arguments]    ${class_name}    ${label_text}
    # Click the element by its class name
    Click Element    css:.${class_name}
    Click Element    xpath=//div[@aria-label='${label_text}']

Enter Max Price
    [Arguments]     ${price}
    Click Element    id=priceMax
    Input Text    id=priceMax      ${price}

Enter Min Price
    [Arguments]     ${price}
    Click Element    id=priceMin
    Input Text    id=priceMin   ${price}

Enter Min Area
    [Arguments]     ${area}
    Click Element    id=areaMin
    Input Text    id=areaMin   ${area}

Select Rooms
    [Arguments]     ${rooms_number}
    Wait Until Element Is Visible    css=#roomsNumber
    Click Element    xpath=//*[@id="roomsNumber"]//*[text()='${rooms_number}']

Enter City in Input
    [Arguments]    ${placeholder_text}    ${input_text}
    # Locate the input element by placeholder, click it, then input the text
    Click Element    xpath=//input[@placeholder='${placeholder_text}']
    Input Text       xpath=//input[@data-cy='search.form.location.input']    ${input_text}

Select City On List
    [Arguments]    ${text}
    # Click the element using the text
    Wait Until Element Is Visible    xpath=//p[.//mark[contains(text(), '${text}')]]    timeout=10s
    Click Element                   xpath=//p[.//mark[contains(text(), '${text}')]]/..

Click Wyszukaj
    Wait Until Element Is Enabled    id=search-form-submit
    Click Button    id=search-form-submit

Click Element By Partial Text
    [Arguments]    ${text}
    # Locate the element by partial text match and click it
    Wait Until Element Is Visible    xpath=//*[contains(text(), '${text}')]    timeout=20s
    Click Element                   xpath=//*[contains(text(), '${text}')]

Click Next Page Button
    # Set the XPath as a variable
    ${xpath_var}=   Set Variable    //li[@aria-label='Go to next Page']
    # Locate the element by XPath and store it in a variable
    ${element}=   Get WebElement    xpath=//li[@aria-label='Go to next Page']

    # Use JavaScript to scroll the element into view
    Run Keyword And Ignore Error    Scroll Element Into View    xpath=${xpath_var} 

    # Wait until the element is visible
    Wait Until Element Is Enabled    xpath=${xpath_var}   timeout=10s

    # Click the element
    Click Element    xpath=${xpath_var}
    Sleep    5

Check If Next Page Exists
    # Check if the next page button exists and is clickable
    ${next_button_exist}=   Run Keyword And Return Status    Element Should Be Visible    xpath=//li[@aria-label='Go to next Page']
    Return From Keyword If    ${next_button_exist}    ${next_button_exist}
    Log    No more pages to navigate.


Get Url
    ${current_url}=     Get Location
    Log    The current URL is: ${current_url}
    RETURN  ${current_url}