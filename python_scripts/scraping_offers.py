from bs4 import BeautifulSoup
import re
from robot.api.deco import keyword
import pandas as pd

@keyword("Scrape Offers With URL")
def scrape_site_content(html_content):
    """
    This function scrapes price, URL, address (street), number of rooms, surface area, price per square meter, and floor for each offer.
    Returns a list of dictionaries where each dictionary contains 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    offers = []

    # Find all listings (li elements)
    for listing in soup.find_all('li'):
        # Extract price from span containing 'zł'
        price_element = listing.find('span', text=re.compile(r'zł'))
        price_value = price_element.get_text(strip=True).replace("\xa0", " ") if price_element else None

        # Extract URL from the first <a> tag inside the listing
        url_element = listing.find('a', href=True)

        # Extract the address (street) by looking for "ul."
        address_element = listing.find('p', class_=re.compile(r'css-42r2ms'))
        address_value = address_element.get_text(strip=True) if address_element else None

        # Extract the number of rooms
        rooms_element = listing.find('dt', text='Liczba pokoi')
        rooms_value = rooms_element.find_next('dd').get_text(strip=True) if rooms_element else None

        # Extract surface area
        surface_area_element = listing.find('dt', text='Powierzchnia')
        surface_area_value = surface_area_element.find_next('dd').get_text(strip=True) if surface_area_element else None

        # Extract price per square meter
        price_per_sqm_element = listing.find('dt', text='Cena za metr kwadratowy')
        price_per_sqm_value = price_per_sqm_element.find_next('dd').get_text(strip=True) if price_per_sqm_element else None

        # Extract floor (if available)
        floor_element = listing.find('dt', text='Piętro')
        floor_value = floor_element.find_next('dd').get_text(strip=True) if floor_element else None

        # Clean up price per square meter (remove non-numeric characters except decimal)
        clean_price_per_sqm = re.sub(r'[^\d,]', '', price_per_sqm_value).replace(",", ".") if price_per_sqm_value else None

        if clean_price_per_sqm and url_element:
            # Append each offer as a dictionary with 'price', 'url', 'address', 'rooms', 'surface_area', 'price_per_sqm', and 'floor'
            offers.append({
                'price': price_value,
                'url': f'https://www.otodom.pl{url_element["href"]}',
                'address': address_value,
                'rooms': rooms_value,
                'surface_area': surface_area_value,
                'price_per_sqm': float(clean_price_per_sqm) if clean_price_per_sqm else None,
                'floor': floor_value
            })

    return offers

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

    # Filter the offers to include only those with a valid price per square meter
    filtered_offers = [offer for offer in offers if offer['price_per_sqm'] and offer['price_per_sqm'] > 1000]

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

    # Create a DataFrame from the list of offers
    df = pd.DataFrame(offers)

    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)

    print(f"Offers saved to {file_name}")
