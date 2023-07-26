import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup

def get_movies(endpoint):
    """
    Get a list of movie links from the specified endpoint.

    Parameters:
        endpoint (str): The URL endpoint to scrape movie links from.

    Returns:
        list: A list of movie links (URLs).
    """

    BASE_ENDPOINT = 'https://letterboxd.com/'
    all_movies = []

    # Send a GET request to the endpoint and parse the HTML response
    response = requests.get(endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.find_all(class_='poster-container numbered-list-item')

    for element in elements:
        # Extract the 'data-target-link' attribute from the 'poster' div
        site = element.find('div', class_='poster').get('data-target-link')
        all_movies.append(BASE_ENDPOINT + site)

    return all_movies


def get_reviews(endpoint,max_reviews):
    """
    Scrape review data for a movie from the specified endpoint.

    Parameters:
        endpoint (str): The URL endpoint to scrape review data from.
        max_reviews (int, optional): The maximum number of reviews to scrape. Default is 20.

    Returns:
        dict: A dictionary containing movie review data with keys 'NAME', 'YEAR', 'DIRECTOR', 'SYNOPSIS',
              'RATINGS', and 'TEXT'.
    """
    
    response = requests.get(endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract relevant movie information from the webpage
    film_name = soup.find(class_='headline-1 js-widont prettify').text
    film_year = soup.find(class_='number').text
    film_director = soup.find('span', class_='prettify').text
    film_synopsys = soup.find(class_='truncate').text
    
    rating_review = []
    text_review = []
    
    count_rev = 0 # Initialize the review count
    page = 1  # Start with the first page of reviews
    
    # Loop until the desired number of reviews is reached
    while count_rev < max_reviews:
        response = requests.get(f'{endpoint}reviews/by/activity/page/{page}/')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all review elements on the page
        reviews = soup.find_all(class_='film-detail-content')

        # Iterate over each review element
        for review in reviews:
            text = review.find(class_='-prose').text
            stars = review.find(class_='rating')
            
            # Check if the review text is long enough and not truncated
            if len(text) > 5:
                if not (text[-3] == '…' or text[-4] == '…'):
                    text_review.append(text+'***') # '***' is a separator
                    
                    # Check if a rating is available or set it to 'None'
                    if stars is None:
                        rating_review.append(' None ')
                    else:
                        rating_review.append(stars.text)
                        
                    count_rev += 1
                    if count_rev == max_reviews:
                        break
                
        # Move to the next reviews page
        page += 1
    
    # Create a dictionary with the movie review data
    data = {
        'NAME': film_name,
        'YEAR': film_year,
        'DIRECTOR': film_director,
        'SYNOPSYS': film_synopsys,
        'RATINGS': rating_review,
        'TEXT': text_review
    }
    
    return data

def build_dataset(data):
    df = pd.DataFrame(data=data)
    return df

def format_date():
    date = datetime.datetime.now()
    
    year = date.year
    month = date.month
    day = date.day

    return f'{year}-{month}-{day}'