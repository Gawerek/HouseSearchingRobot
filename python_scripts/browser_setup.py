from selenium import webdriver


def get_chrome_options(profile_path):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={profile_path}')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    return options