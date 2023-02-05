#!/usr/bin/env python


## NECESSARY IMPORTS
import sys
import json
import os
import shutil

from src.data import make_dataset
from src.features import build_features
from src.models import train_model
from src.visualization import visualize


#!/usr/bin/env python


## NECESSARY IMPORTS
import sys
import json
import os
import shutil

from src.data import make_dataset
from src.features import build_features
from src.models import train_model
from src.visualization import visualize



def main(targets):
    if "test" in targets:
        if not os.path.exists("data/temp"):
            os.makedirs("data/temp")
        if not os.path.exists("data/out"):
            os.makedirs("data/out")
        
#         test_path_metadata="test/test_metadata.tsv"
#         test_path_feature_table = "test/test_feature_table.qza"

#         metadata = make_dataset.read_metadata(test_path_metadata)
#         feature_table = make_dataset.read_feature_table(test_path_feature_table)

        return 

    
    if "all" in targets:
        if not os.path.exists("data/temp"):
            os.makedirs("data/temp")
        if not os.path.exists("data/out"):
            os.makedirs("data/out")
            
        with open("config/data-params.json") as fh:
            file_paths = json.load(fh)
        return
        
    if 'clean' in targets:
        try:
#             os.remove('final_figure.png')
        except OSError as e: 
            print ("Error: %s - %s." % (e.filename, e.strerror))
        try:
            shutil.rmtree("data/temp")
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
        try:
            shutil.rmtree("data/out")
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":
    # python run.py test
    targets = sys.argv[1:]
    main(targets)
    