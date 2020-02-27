##################################################################
# 1. See how many fields will be set: hw_generator_config
# 2. Set new field coordinates from 
#    - customer_data_generatiors.py -> generate_data
# 3. Select how many fields to generate
#    - hw_generator_config.py -> FIELD_DICT_(N)FIELDS
# 4. Set output folders and metadata csv in this file
# 5. Run run_generator.py
##################################################################

# Run this
import os
import random

# from form_field import *
from form_presets import *
from hw_image_generator import *
from customer_data_generators import *


# Modify Config File
from hw_generator_config import *


# tempdir = "../data/data_16f_batch2"
# tempdir = "../data/data_16f_test"
tempdir = "../data/data_23f_train"

temp_csv = "metadata_23f_train.csv"
continue_index = 102100
n_data = 2000
fields = 23
temp_fields = FIELD_DICT_23FIELDS
# temp_fields = FIELD_DICT_16FIELDS
# temp_fields = FIELD_DICT_7FIELDS

def run(tempdir,continue_index,temp_csv,n_data,fields,temp_fields, **kwargs):
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    form_filler= FormFiller()
    form_filler.generate_data(n_data,in_positions=fields,start_id=continue_index)
    # Save the text to csv file
    form_filler.data_to_csv(temp_csv)
    form_filler.set_handwriting()
    form_filler.field_iterator(input_field_dict=temp_fields,start_id = continue_index,
                               input_root=tempdir,input_df = form_filler.info_df,
                               x_bias = int((random.random()-0.5) * 40),
                               y_bias = int((random.random()-0.5) * 30)
                              )

if __name__ == '__main__':
    run(tempdir,continue_index,temp_csv,n_data,fields,temp_fields)
