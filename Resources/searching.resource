*** Settings ***
Library    SeleniumLibrary
Library    ../python_scripts/browser_setup.py

*** Variables ***
${HOME_URL}         https://www.otodom.pl
${BROWSER}          edge


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
    Click Button    id=search-form-submit

Click Element By Partial Text
    [Arguments]    ${text}
    # Locate the element by partial text match and click it
    Wait Until Element Is Visible    xpath=//*[contains(text(), '${text}')]    timeout=20s
    Click Element                   xpath=//*[contains(text(), '${text}')]



