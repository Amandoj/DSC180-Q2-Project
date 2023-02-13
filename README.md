# DSC180-Q2-Project
Abstract: 


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
To view model performance graphs, after running `run.py`, download files from `data/out` and upload to https://view.qiime2.org/

Collaborator: Amando Jimenez, Emerson Chao, Renaldy Herlim
