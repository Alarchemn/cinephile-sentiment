import pandas as pd
import pickle

def et_data(path: str):
    """
    Process the DataFrame from the CSV file located at 'path' to extract and clean the 'RATINGS' and 'REVIEWS' columns.

    Parameters:
        path (str): The file path of the CSV file containing a DataFrame with columns 'NAME', 'RATINGS', and 'REVIEWS'.

    Returns:
        dict: A dictionary with the processed data, where the 'NAME' column serves as the keys.
              The 'RATINGS' key in the dictionary contains a list of numerical ratings.
              The 'REVIEWS' key in the dictionary contains a list of cleaned review texts.

    Dictionary Structure:
    {
        'RATINGS': {
            'NAME1': [stars1, stars2, ...],
            'NAME2': [stars1, stars2, ...],
            ...
        },
        'REVIEWS': {
            'NAME1': [comment1, comment2, ...],
            'NAME2': [comment1, comment2, ...],
            ...
        }
    }

    'RATINGS': Primary key representing numerical ratings for each movie.
    'REVIEWS': Secondary key representing cleaned review texts for each movie.
    'NAME1', 'NAME2', ...: Movie names serving as keys for the nested dictionaries.
    stars1, stars2, ...: List of numerical ratings (float) for each movie.
    comment1, comment2, ...: List of cleaned review texts (string) for each movie.
    """
    df = pd.read_csv(path)

    df['RATINGS'] = df['RATINGS'].str[1:-1].str.split(', ')
    df['REVIEWS'] = df['REVIEWS'].str[1:-1].str.split('\*\*\*')

    data_dict = df[['NAME','RATINGS','REVIEWS']].set_index('NAME').to_dict()

    rev_dict = {}
    for key, value in data_dict['REVIEWS'].items():
        clean_rev = []
        
        for review in value:
            # Remove unwanted characters from each review
            string = review.replace("',","").replace("' ","").replace("\'","").replace('AAAA','')
            clean_rev.append(string)
            
        #Drop the last empty comment    
        rev_dict[key] = clean_rev[:-1]
        
    # Update the 'REVIEWS' key in data_dict with the cleaned review texts
    data_dict['REVIEWS'] = rev_dict

    num_dict = {}
    for key,value in data_dict['RATINGS'].items():
        num_values = []
        
        for stars in value:
            # Call the get_num_rating() function to extract the numerical rating
            num_values.append(get_num_rating(stars))
        num_dict[key] = num_values
        
    # Update the 'RATINGS' key in data_dict with the extracted numerical ratings
    data_dict['RATINGS'] = num_dict

    return data_dict


def get_num_rating(raw_string):
    """
    Extract the numerical rating from the raw_data string.

    Parameters:
        raw_string (str): A string representing the raw rating data, which may contain '★' for full stars and '½' for half star.

    Returns:
        float: The numerical rating extracted from the raw_data string. If raw_data is 'None', it returns 0.0.
    """
    
    # Remove the leading and trailing characters
    stars = raw_string[2:-2]  
    count = 0.0

    if stars != 'None':
        # Iterate over each character in stars
        for char in stars:
            if char == '★':
                count += 1
            elif char == '½':
                count += 0.5

    return count

def get_labels(scores):
    """
    Map the model output scores to human-readable labels.

    Parameters:
        scores (numpy.ndarray): An array containing the model's output scores for each class.

    Returns:
        dict: A dictionary where the keys are human-readable labels ('Negative', 'Neutral', 'Positive')
              and the values are the corresponding scores from the model.
    """
    
    # Define a dictionary to map class indices to human-readable labels
    # info in: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
    labels = {
    0:'Negative',
    1:'Neutral',
    2:'Positive'
    }
    
    result = {}
    for i in range(scores.shape[0]):
        result[labels[i]] = scores[i]
    return result

def save_results(data, path: str):
    """
    Save the 'data' object to a file specified by 'path' using the Pickle library.

    Parameters:
        data: The data object to be saved.
        path (str): The file path where the data will be saved.

    Returns:
        None
    """

    with open(path, 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

