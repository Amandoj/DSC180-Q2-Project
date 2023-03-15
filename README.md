# DSC180-Q2-Project
Abstract: In this study, we will be exploring the gut microbiome of Latin American immigrants to determine what factors of their gut microbiome affect metabolic diseases. The goal of our project is to determine what metabolic diseases/disorders an individual has based on their gut microbiome and other supporting information on the individual. To achieve our goal, we will be exploring machine learning and data analysis techniques to summarize the key points of the data and understand the patterns and relationships in the data.


## Retrieving the data locally:
(1) Download the data files from the following Google Drive: https://drive.google.com/drive/folders/1cpUvpXbh3YEHHaW4jmeKhL8DYfE7tE5V?usp=sharing

(2) Place files in `data/raw` directory

## Activating Qiime2
After launching container, open terminal and type in the following command before running `run.py`:

`conda activate qiime2-2022.11`

To use within jupyter notebook also type in the following commands: 

`pip install -–user ipykernel`

`python -m ipykernel install -–user -–name=qiime2-2022.11`

then refresh jupyter hub

and select the qiime2 kernel

## Running the Project:
* To revert to a clean repository, from the project root dir, run `python run.py clean`
  * This deletes all built files
* To run the entire project on test data, from the project root dir, run `python run.py test`
  * This fetches the test data, creates features, cleans the data, creates machine learning models and model performance graphs
  for given disease types
* To run the entire project on the real data, from the project root dir, run `python run.py all`
  * This fetches the original data, creates features, cleans the data, creates machine learning models and model performance graphs
  for given disease types
  
## Model Performance
To view model performance graphs, permanova tests, and pcoa plots after running `run.py`, download `.qzv` files from `data/out` and upload to https://view.qiime2.org/

Collaborator: Amando Jimenez, Emerson Chao, Renaldy Herlim
