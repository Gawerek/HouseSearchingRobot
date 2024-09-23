from bs4 import BeautifulSoup
import re
import os
import pandas as pd
from robot.api.deco import keyword
from datetime import datetime
from urllib.parse import urlparse, urlunparse


@keyword("Scrape Offers With URL")
def scrape_site_content(html_content):
    """
    This function scrapes price, URL, address (street), number of rooms, surface area, price per square meter, and floor for each offer.
    Returns a list of dictionaries where each dictionary contains 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    offers = []
    unique_urls = set()  # Set to store unique URLs

    # Find all listings (li elements)
    for listing in soup.find_all('li'):
        # Extract price from span containing 'zł'
        price_element = listing.find('span', text=re.compile(r'zł'))
        price_value = price_element.get_text(strip=True).replace("\xa0", " ") if price_element else None

        # Extract URL from the first <a> tag inside the listing
        url_element = listing.find('a', href=True)

        # Only include URLs that contain '/oferta'
        if url_element and '/oferta' in url_element['href']:
            # Normalize the URL: remove any potential trailing slashes, and ensure consistent formatting
            offer_url = normalize_url(f"https://www.otodom.pl{url_element['href']}")

            # Check if the URL is already in the unique set
            if offer_url not in unique_urls:
                unique_urls.add(offer_url)  # Add the URL to track uniqueness

                # Extract other details
                address_element = listing.find('p', class_=re.compile(r'css-42r2ms'))
                address_value = address_element.get_text(strip=True) if address_element else None

                rooms_element = listing.find('dt', text='Liczba pokoi')
                rooms_value = rooms_element.find_next('dd').get_text(strip=True) if rooms_element else None

                surface_area_element = listing.find('dt', text='Powierzchnia')
                surface_area_value = surface_area_element.find_next('dd').get_text(
                    strip=True) if surface_area_element else None

                price_per_sqm_element = listing.find('dt', text='Cena za metr kwadratowy')
                price_per_sqm_value = price_per_sqm_element.find_next('dd').get_text(
                    strip=True) if price_per_sqm_element else None

                floor_element = listing.find('dt', text='Piętro')
                floor_value = floor_element.find_next('dd').get_text(strip=True) if floor_element else None

                clean_price_per_sqm = re.sub(r'[^\d,]', '', price_per_sqm_value).replace(",",
                                                                                         ".") if price_per_sqm_value else None

                if clean_price_per_sqm:
                    offers.append({
                        'price': price_value,
                        'url': offer_url,
                        'address': address_value,
                        'rooms': rooms_value,
                        'surface_area': surface_area_value,
                        'price_per_sqm': float(clean_price_per_sqm),
                        'floor': floor_value
                    })

    return offers


def normalize_url(url):
    """
    Normalize the given URL by ensuring consistent formatting (e.g., removing trailing slashes, ignoring query parameters).
    """
    parsed_url = urlparse(url)
    # Rebuild the URL without query parameters or fragment and ensure no trailing slash
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path.rstrip('/'), '', '', ''))
    return normalized_url


@keyword("Find Best Offer By Price")
def find_best_offer(offers, n=10):
    """
    Given a list of offers (each as a dictionary with 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'),
    find the `n` best (lowest) price offers and return them.

    Args:
    - offers: List of dictionaries with 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'.
    - n: Number of top offers to return (default is 10).

    Returns:
    - A list of the `n` best offers sorted by price per square meter.
    """
    if not offers:
        return None

    # Remove duplicate offers based on the URL
    unique_offers = []
    seen_urls = set()
    for offer in offers:
        if offer['url'] not in seen_urls and 'inwesty' not in offer['url']:
            unique_offers.append(offer)
            seen_urls.add(offer['url'])

    # Filter the offers to include only those with a valid price per square meter
    filtered_offers = [offer for offer in unique_offers if offer['price_per_sqm'] and offer['price_per_sqm'] > 1000]

    # Sort the offers by price per square meter (ascending order)
    sorted_offers = sorted(filtered_offers, key=lambda x: x['price_per_sqm'])

    # Return the top `n` offers
    return sorted_offers[:n]



@keyword("Save Offers to Excel")
def save_offers_to_excel(offers, file_name="offers.xlsx"):
    """
    Save the list of offers to an Excel file with columns 'Price', 'URL', 'Address', 'Rooms', 'Surface Area', 'Price per sqm', and 'Floor'.

    Args:
    - offers: List of dictionaries with 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'.
    - file_name: The name of the Excel file (default is 'offers.xlsx').
    """
    if not offers:
        print("No offers to save.")
        return

    # Add a timestamp to the file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name_with_timestamp = f"{file_name.split('.')[0]}_{timestamp}.csv"

    # Define the relative path for the Data folder
    relative_path = os.path.join('Data', file_name_with_timestamp)

    # Ensure the 'Data' directory exists
    if not os.path.exists('Data'):
        os.makedirs('Data')

    # Create a DataFrame from the list of offers
    df = pd.DataFrame(offers)

    # Save the DataFrame to an Excel file
    df.to_csv(relative_path, index=False)

    print(f"Offers saved to {relative_path}")
