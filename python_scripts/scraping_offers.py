from bs4 import BeautifulSoup
import re
from robot.api.deco import keyword
import pandas as pd

@keyword("Scrape Offers With URL")
def scrape_site_content(html_content):
    """
    This function scrapes both the price per square meter and the URL for each offer.
    Returns a list of dictionaries where each dictionary contains 'price' and 'url'.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    offers = []

    # Find all listings (li elements)
    for listing in soup.find_all('li'):
        # Extract price per square meter from dd[3]
        price_per_sqm_element = listing.select_one('dd:nth-of-type(3)')
        # Extract URL from the first <a> tag inside the listing
        url_element = listing.find('a', href=True)

        if price_per_sqm_element and url_element:
            price_text = price_per_sqm_element.get_text()
            # Clean the price, remove non-numeric characters
            clean_price = re.sub(r'\D', '', price_text)
            offer_url = url_element['href']

            if clean_price:
                # Append each offer as a dictionary with 'price' and 'url'
                offers.append({
                    'price': int(clean_price),
                    'url': f'https://www.otodom.pl{offer_url}'
                })

    return offers


@keyword("Find Best Offer By Price")
def find_best_offer(offers, n=10):
    """
    Given a list of offers (each as a dictionary with 'price' and 'url' keys),
    find the `n` best (lowest) price offers and return their URLs and prices.

    Args:
    - offers: List of dictionaries with 'price' and 'url' keys.
    - n: Number of top offers to return (default is 10).

    Returns:
    - A list of the `n` best offers sorted by price.
    """
    if not offers:
        return None

    #Filter the offers to include only those with a price greater than 1000
    filtered_offers = [offer for offer in offers if offer['price'] > 1000]

    # Sort the offers by price (ascending order)
    sorted_offers = sorted(filtered_offers, key=lambda x: x['price'])

    # Return the top `n` offers
    return sorted_offers[:n]


@keyword("Save Offers to Excel")
def save_offers_to_excel(offers, file_name="offers.xlsx"):
    """
    Save the list of offers to an Excel file with columns 'Price' and 'URL'.

    Args:
    - offers: List of dictionaries with 'price' and 'url' keys.
    - file_name: The name of the Excel file (default is 'offers.xlsx').
    """
    if not offers:
        print("No offers to save.")
        return

    # Create a DataFrame from the list of offers
    df = pd.DataFrame(offers)

    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)