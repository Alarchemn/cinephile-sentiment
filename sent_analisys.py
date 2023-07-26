from pipeline_utils import et_data, get_labels, save_results
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import hydra
from hydra import utils
import logging
import time

log = logging.getLogger(__name__)

@hydra.main(config_name='config.yaml')
def analyze(config):
    start = time.time()

    current_path = utils.get_original_cwd() + '/'
    
    MODEL_NAME = config.model.name
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    data_dict = et_data(current_path + config.dataset.raw)

    sentiment_dict = {}
    for key,values in data_dict['REVIEWS'].items():
        
        sentiment_list = []
        for review in values:
            # Tokenize the review text and convert it to PyTorch tensors
            encoded_input = tokenizer(review, return_tensors='pt')
            try:
                output = model(**encoded_input)
            except:
                # If an exception occurs, set labels to 'Wrong input'
                labels = 'Wrong input'
                log.exception(f'Wrong input:\n{review}\nIt will ignore.')
            else:
                # Extract the model's output scores, apply softmax, and get human-readable labels
                scores = softmax(output[0][0].detach().numpy())
                labels = get_labels(scores)
            finally:
                sentiment_list.append(labels)
        
        # Assign the sentiment_list to the key in sentiment_dict
        sentiment_dict[key] = sentiment_list

    save_results(sentiment_dict,path=current_path + config.dataset.processed)

    end = time.time()
    total_time = round(end-start,2)

    log.info(f'Sucess!\nExcecution time: {total_time} seconds')
    log.debug(f'RESULTS: {sentiment_dict}')

if __name__ == '__main__':
    analyze()
