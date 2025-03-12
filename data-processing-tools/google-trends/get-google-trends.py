import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def google_search_requests(query, num_results=10):
    """
    Basic Google search using requests (unofficial method)
    WARNING: This may violate Google's Terms of Service
    """
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    # URL encode the query
    encoded_query = urllib.parse.quote(query)
    
    params = {
        "q": encoded_query,
        "num": num_results
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract search results
        results = []
        for result in soup.find_all('div', class_='yuRUbf'):
            link = result.find('a')
            title = result.find('h3')
            
            if link and title:
                results.append({
                    'title': title.text.strip(),
                    'link': link['href']
                })
        
        return results
    
    except requests.RequestException as e:
        logger.error(f"Error performing Google search: {e}")
        return []

def google_custom_search(query, api_key, cx, num_results=10):
    """
    Official Google Custom Search API
    Requires:
    1. Google Cloud Console API Key
    2. Custom Search Engine ID
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'num': num_results  # Add number of results parameter
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse and extract relevant search results
        data = response.json()
        results = []
        
        if 'items' in data:
            for item in data['items']:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
        
        return results
    
    except requests.RequestException as e:
        logger.error(f"Error in Custom Search API: {e}")
        return None

def serpapi_search(query, api_key, num_results=10):
    """
    Uses SerpAPI for Google searches
    Requires SerpAPI account and key
    """
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse and extract relevant search results
        data = response.json()
        results = []
        
        if 'organic_results' in data:
            for result in data['organic_results']:
                results.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
        
        return results
    
    except requests.RequestException as e:
        logger.error(f"Error in SerpAPI search: {e}")
        return None

def main():
    # Example usage demonstrating different search methods
    query = "Python programming best practices"
    
    # Method 1: Requests-based scraping (use with caution)
    print("--- Requests-based Search Results ---")
    requests_results = google_search_requests(query)
    for result in requests_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}\n")
    
    # Method 2: Google Custom Search API (requires setup)
    # Uncomment and replace with your actual keys
    # print("--- Google Custom Search API Results ---")
    # custom_api_key = "YOUR_GOOGLE_CUSTOM_SEARCH_API_KEY"
    # custom_cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
    # custom_results = google_custom_search(query, custom_api_key, custom_cx)
    # if custom_results:
    #     for result in custom_results:
    #         print(f"Title: {result['title']}")
    #         print(f"Link: {result['link']}")
    #         print(f"Snippet: {result['snippet']}\n")
    
    # Method 3: SerpAPI (requires account)
    # Uncomment and replace with your actual key
    # print("--- SerpAPI Search Results ---")
    # serpapi_key = "YOUR_SERPAPI_KEY"
    # serpapi_results = serpapi_search(query, serpapi_key)
    # if serpapi_results:
    #     for result in serpapi_results:
    #         print(f"Title: {result['title']}")
    #         print(f"Link: {result['link']}")
    #         print(f"Snippet: {result['snippet']}\n")

if __name__ == "__main__":
    main()