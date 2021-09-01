import requests
import urllib
import csv
from requests_html import HTMLSession

def parse_results(response):
    """ data selection """

    # define selectors for scraping the desired data
    css_identifier_count_results = "#result-stats"
    css_identifier_result = ".tF2Cxc"
    css_identifier_link = ".yuRUbf a"

    output = []

    # add number of results for keyword to list
    count_results = response.html.find(css_identifier_count_results)[0].text.split()
    output.append(count_results[1])

    # add links from each result to list
    results = response.html.find(css_identifier_result)
    for result in results:
        item = result.find(css_identifier_link, first=True).attrs['href']

        output.append(item)

    return output

def get_source(url):
    """ return response.url (object) """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def google_search(keyword):
    """ pass the keyword to the url, get source """

    url = "https://www.google.co.uk/search?q=site:https://www.searchenginejournal.com/%20" + keyword
    response = get_source(url)

    # parse returned response object
    return parse_results(response)


def read_keywords():
    """ read keywords from .txt file and return them as a list """

    with open('keywords.txt') as f:
        keywords = f.read().splitlines()

    return keywords

def scraping_data_to_files():
    """ save data """

    # open the files in the write mode
    # first file has links pointing to SearchEngineJournal from Google Search (page 1)
    with open("scraped_links.csv", 'w', newline='') as file_links:
        # second file has keywords with amount of results
        with open("count_keyword_results.csv", 'w', newline='') as file_nKeys:
            # create the csv writers
            writer_links = csv.writer(file_links)
            writer_nKeys = csv.writer(file_nKeys)

            # looping through a keywords list
            for keyword in read_keywords():
                #
                links = google_search(keyword)

                # write a rows to the csv files
                for index, link in enumerate(links):
                    if index == 0:
                        # writing to second file - keywords with amount of results
                        writer_nKeys.writerow([keyword + ', ' + link])
                    else:
                        # writing to first file - links
                        writer_links.writerow([link])

def main():
    scraping_data_to_files()

if __name__ == "__main__":
    main()