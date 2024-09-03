from bs4 import BeautifulSoup

from robot.api.deco import keyword


@keyword("Scrape Site content")
def scrape_site_content(html_content):
    """
    This function takes the HTML content as a string and uses BeautifulSoup to parse it.
    It is marked as a Robot Framework keyword using the @keyword decorator.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = [title.get_text() for title in soup.find_all('h1')]


@keyword()