#!/usr/bin/env python3
import cgi
import cgitb
import requests
from bs4 import BeautifulSoup
import json

cgitb.enable()  # Enable error reporting for CGI scripts
print("Content-Type: application/json\n")  # Set content type to JSON

def google_search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    params = {'q': query, 'num': 10}

    # Use a session to persist the connection
    session = requests.Session()

    try:
        response = session.get('https://www.google.com/search', headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # Adjust selectors based on current Google search result structure
        for item in soup.find_all('div', attrs={'class': 'g'}, limit=10):
            title_element = item.find('h3')
            link_element = item.find('a')
            snippet_element = item.find('span', attrs={'class': 'aCOpRe'}) or item.find('div', class_='IsZvec')  # Alternate for snippet
            if title_element and link_element:
                title = title_element.get_text()
                link = link_element['href']
                snippet = snippet_element.get_text() if snippet_element else 'No snippet available'

                results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet
                })

                if len(results) >= 5:  # Limit to top 5 results
                    break

        return results

    except requests.RequestException as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': 'An unexpected error occurred: ' + str(e)}

form = cgi.FieldStorage()
query = form.getvalue('query')
results = google_search(query)
print(json.dumps(results))