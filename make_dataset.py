import hydra
from hydra import utils
import time
import logging
from scrape_utils import get_movies, get_reviews, build_dataset

log = logging.getLogger(__name__)

@hydra.main(config_name='config.yaml')
def extract_data(config):

    start = time.time()

    current_path = utils.get_original_cwd() + '/'
    
    all_endpoints = config.endpoints
    all_endpoints = [endpoint for endpoint_list in all_endpoints for endpoint in endpoint_list.values()]

    # Define a list to store all movie links
    all_movies = []

    # Create an empty dictionary to store data for each movie
    data = {
            'NAME': [],
            'YEAR': [],
            'DIRECTOR': [],
            'SYNOPSYS': [],
            'RATINGS': [],
            'REVIEWS': []
        }

    # Iterate over each endpoint in the list ALL_250_ENDOPOINTS
    for endpoint in all_endpoints:
        all_movies += get_movies(endpoint)

    # Iterate over each movie in the list all_movies
    count = 0
    for movie in all_movies:
        row = get_reviews(movie,max_reviews=config.reviews.max)
        
        data['NAME'].append(row['NAME'])
        data['YEAR'].append(row['YEAR'])
        data['DIRECTOR'].append(row['DIRECTOR'])
        data['SYNOPSYS'].append(row['SYNOPSYS'])
        data['RATINGS'].append(row['RATINGS'])
        data['REVIEWS'].append(row['TEXT'])

        count += 1

    # Create a DataFrame from the data dictionary
    df = build_dataset(data)

    df.to_csv(current_path + config.dataset.raw)

    end = time.time()
    total_time = round(end-start,2)
    total_reviews = count * config.reviews.max

    log.info(f'Sucess!\nExcecution time: {total_time} seconds\nTotal reviews: {total_reviews}')


if __name__ == '__main__':
    extract_data()
