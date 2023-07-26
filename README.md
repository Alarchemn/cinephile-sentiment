Letterboxd sentiment analysis
==============================

Sentiment analysis of short reviews of any letterbox's list (for example, [Official Top 250 Narrative Feature Films list](https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/))

This project is based on the huggingface Transformers library using the state-of-the-art machine learning model [RoBERTa](https://arxiv.org/abs/1907.11692) with PyTorch.

Instructions
------------
To use this project, you can follow these steps:

1. Ensure you have the required Python packages installed by running: `pip install -r requirements.txt`
2. Adjust the configuration in config.yaml to customize the behavior of the sentiment analysis process.
    * Configure all the letterboxd list endpoints (pages).
    * Set the number of reviews to extract.
    * Change the huggingface model if you want.
3. Run the `make_dataset.py` script to perform web scraping and gather the dataset. The data will be saved in the `data/raw` directory.
4. Run the `sent_analisys.py` script to perform sentiment analysis on the collected data. The results will be stored in the `data/processed` directory.


Project Organization
------------

    ├── LICENSE
    ├── README.md           <- The top-level README for developers using this project.
    ├── data
    │   ├── external        <- Data from third party sources.
    │   ├── interim         <- Intermediate data that has been transformed.
    │   ├── processed       <- The final result data sets.
    │   └── raw             <- The original, immutable data dump (from scraping).
    │
    ├── models              <- model_name from huggingface
    │
    ├── notebooks           <- Jupyter notebooks.                         
    │
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
    │                          generated with `pip freeze > requirements.txt`
    │
    ├── scrape_utils.py     <- Utility functions to get the list of movies and extract their reviews
    │
    ├── make_dataset.py     <- Script for web scraping and persisting the dataset
    │
    ├── pipeline_utils.py   <- Utility functions for dataset extraction and transformation     
    │
    ├── sent_analisys.py    <- Script to perform sentiment analysis and store results
    │
    ├── config.yaml         <- Configuration file

--------
Note
------------
Script runs on CPU but can be modified for GPU