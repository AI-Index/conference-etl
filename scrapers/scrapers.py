import os
from time import sleep
from subprocess import call
from requests import get, head
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1200x600')

#########################################################################
# Third Party Code


# Source - https://bit.ly/2l4P84Q

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# Source - https://bit.ly/2PRM1v9

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

#########################################################################
# Scraper Classes

pdf_dir = "pdfs"


class Scraper(object):
    def __init__(self):
        self.pdf_dir = "pdfs"
        self.txt_dir = "txts"

    def scrape(self, source: str):
        raise NotImplementedError()

    def download_pdf(self, url: str, outname: str, force=True):
        """
        Download the given url if it's a pdf and save it to the correct
        directory
        """
        outfile = outname + ".pdf"
        filepath = os.path.join(pdf_dir, outfile)

        # Make sure we don't have this pdf already
        have = set(os.listdir(self.pdf_dir))
        if not force and outfile in have:
            print("Skipping {}, we have a pdf of this name".format(outfile))
            print("To force redownload pass force=True. (--force from the command line")

        assert is_downloadable(url)
        print("Downloading and parsing pdf ...")
        r = get(url, allow_redirects=True)

        with open(filepath, 'wb') as fh:
            fh.write(r.content)

    def parse_pdfs(self):
        call(["python", "lib/parse_pdf_to_text.py"])


class ICRA2018(Scraper):

    def doi_to_url(self, doi):
        url = "http://dx.doi.org/{}".format(doi)
        return url

    def extract_doi_urls(self, text_lines):
        """
        Return paper URLs from DOI's in the given text
        """
        urls = []
        for line in text_lines:
            if "DOI:" in line:
                ind = line.find("DOI:")
                line_end = line[ind:].strip()
                _, doi = line_end.split(" ")
                url = self.doi_to_url(doi)
                urls.append(url)
        return urls

    def scrape_authors_from_page(self, driver, url: str) -> list:
        print("Scraping {}".format(url))
        driver.get(url)
        author_elems = driver.find_elements_by_css_selector(".stats-author-container")
        authors = []
        for author_elem in author_elems:

            name_elem = author_elem.find_element_by_css_selector("a > span")
            name = name_elem.get_attribute("innerHTML")
            child_divs = author_elem.find_elements_by_css_selector("div")
            affil = None
            for child_div in child_divs:
                val = child_div.get_attribute("ng-bind-html")
                if val and "affiliation" in val:
                    affil = child_div.get_attribute("innerHTML")
                    break
            author_dict = {
                "name": name,
                "affiliation": affil
            }
            authors.append(author_dict)

        return authors

    def scrape(self, source: str):
        print("Scraping ICRA 2018 page ...")
        # These should be PDF links
        url = source["link"]
        filebase = "ICRA-2018"

        # Download and parse given PDF
        # Existing PDFs will be skipped
        # Parsed PDFs will be text files in the txt dir
        self.download_pdf(url, filebase)
        self.parse_pdfs()

        # Parse per-paper urls out of the extracted text files
        text_path = os.path.join(self.txt_dir, filebase+".pdf.txt")
        with open(text_path, 'r') as fh:
            text_lines = fh.readlines()

        paper_urls = self.extract_doi_urls(text_lines)

        data = []
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            for paper_url in paper_urls:
                authors = self.scrape_authors_from_page(driver, paper_url)
                data.append(authors)
                sleep(0.2)  # Try not to get IP banned
        finally:
            driver.quit()

        return data


class ICML2018(Scraper):

    def scrape(self, source: str):
        print("Scraping ICML 2018 page ...")
