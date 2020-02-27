DO_RUN_BIAS_TEST=False
DEBUG = False
INPUT_CSV=False
ROOT_FOLDER="/home/jupyter/forms-ocr"
OUTPUT_FOLDER= ROOT_FOLDER + "/sample_images"
GEN_FOLDER = OUTPUT_FOLDER + "/img"
LOCALE = "en_GB"
DUMMY_GENERATOR=0
FIELD_DICT_3FIELDS= {'Name':(0,0),'Tax':(0,0),
        'Address':(0,0)
          }     

FIELD_DICT_7FIELDS= {'Name':(0,0),'BusinessName':(0,0), 'Tax':(0,0),
        'Address':(0,0),
        'City':(0,0), 'Requester':(0,0),
        'Signature':(0,0) 
          }

FIELD_DICT_16FIELDS= {'Name':(0,0),'BusinessName':(0,0), 'Tax':(0,0),
        'Address':(0,0),
        'City':(0,0), 'Requester':(0,0),
        'Signature':(0,0),
                    'ssn1':(0,0),
                    'ssn2':(0,0),  
                    'ssn3':(0,0),  
                    'ssn4':(0,0),  
                    'ssn5':(0,0),  
                    'ssn6':(0,0),  
                    'ssn7':(0,0),  
                    'ssn8':(0,0),  
                    'ssn9':(0,0)                         
          }

FIELD_DICT_23FIELDS= {'Name':(0,0),'BusinessName':(0,0), 'Tax':(0,0),
        'Address':(0,0),
        'City':(0,0), 'Requester':(0,0),
        'Signature':(0,0),
                    'ssn1':(0,0),
                    'ssn2':(0,0),  
                    'ssn3':(0,0),  
                    'ssn4':(0,0),  
                    'ssn5':(0,0),  
                    'ssn6':(0,0),  
                    'ssn7':(0,0),  
                    'ssn8':(0,0),  
                    'ssn9':(0,0),
                    'Tax2':(0,0),
                    'Tax3':(0,0),
                    'Tax4':(0,0),
                    'Tax5':(0,0),
                    'Tax6':(0,0),
                    'Tax7':(0,0),
                    'Date':(0,0)
          }

FIELD_DICT_SSN= {'ssn1':(0,0),
                    'ssn2':(0,0),  
                    'ssn3':(0,0),  
                    'ssn4':(0,0),  
                    'ssn5':(0,0),  
                    'ssn6':(0,0),  
                    'ssn7':(0,0),  
                    'ssn8':(0,0),  
                    'ssn9':(0,0)                   
                }
FIELD_DICT= {'Name':(0,0),'BusinessName':(0,0), 'Tax':(0,0),
       'Instructions':(0,0), 'Exemptions':(0,0),
        'ExemptionCode':(0,0), 'Address':(0,0),
       'City':(0,0), 'Requester':(0,0),'Account':(0,0),
        'SocialSeciurityNumber':(0,0), 'EmpIdentificationNumber':(0,0)
          }     
############################### 
FAKER_GENERATOR=1
HANDWRITING_FIXED=0
HANDWRITING_PRESET_FLAG=1

