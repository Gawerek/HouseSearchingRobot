from bs4 import BeautifulSoup
import re
from robot.api.deco import keyword


@keyword("Scrape Offers With URL")
def scrape_site_content(html_content):
    """
    This function scrapes both the price per square meter and the URL for each offer.
    Returns a dictionary where the price per square meter is the key and the offer URL is the value.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    offers = {}

    # Find all listings (li elements)
    for listing in soup.find_all('li'):
        # Extract price per square meter from dd[3]
        price_per_sqm_element = listing.select_one('dd:nth-of-type(3)')
        # Extract URL from the first <a> tag inside the listing
        url_element = listing.find('a', href=True)  # Corrected from 'fin' to 'find'

        if price_per_sqm_element and url_element:
            price_text = price_per_sqm_element.get_text()
            # Clean the price, remove "nbsp", "zł/m2" and other non-numeric characters
            clean_price = re.sub(r'\D', '', price_text)
            offer_url = url_element['href']

            if clean_price:
                offers[int(clean_price)] = offer_url  # Convert price to integer instead of float

    print(offers)  # Optional for debugging
    return offers


@keyword("Find Best Offer By Price")
def find_best_offer(offers):
    """
    Given a dictionary of offers (price per square meter as key and URL as value),
    find the best (lowest) price offer and return the corresponding URL.
    """
    if not offers:
        return None
    best_price = min(offers.keys())
    best_offer_url = offers[best_price]
    return best_price, best_offer_url
