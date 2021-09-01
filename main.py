import requests
import urllib
import csv
from requests_html import HTMLSession

def parse_results(response):
    css_identifier_count_results = "#result-stats"
    count_results = response.html.find(css_identifier_count_results)[0].text.split()

    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"

    results = response.html.find(css_identifier_result)

    output = []
    #output.append(count_results[1])

    for result in results:
        item = result.find(css_identifier_link, first=True).attrs['href']

        output.append(item)

    return output

def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=site:https://www.searchenginejournal.com/%20" + query)

    return response

def google_search(query):
    response = get_results(query)

    return parse_results(response)


with open('keywords.txt') as f:
    keywords = f.read().splitlines()


# open the file in the write mode
with open("C:\\Users\\Przemek\\PycharmProjects\\onely_scraping\\test.csv", 'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    for keyword in keywords:
        links = google_search(keyword)

        #writer.writerow([keyword])

        # write a rows to the csv file
        for link in links:
            writer.writerow([link])

