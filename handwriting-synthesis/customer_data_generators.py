import os
import logging
import timeit

import numpy as np
import random
import svgwrite

import pandas as pd
from faker import Faker

from hw_generator_config import *
from hw_image_generator import *

############################### 
### Field Generator ###########
############################### 


def generate_name(flag=0,t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.name()
    #elif (flag==SOME OTHER GENERATOR)
    
    return name

def generate_bname(flag=0,t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.company()
    return name

def generate_tax(flag=0):
    if (flag==0):
        name="x"
    elif(flag==FAKER_GENERATOR):
        pass
    return name

def generate_instructions(flag=0, t_faker = None):
    if (flag==0):
        name='instructions '
    elif(flag==FAKER_GENERATOR):
        t_faker.text(max_nb_chars=10, ext_word_list=None)
        pass
    return name

def generate_exemptions(flag=0):
    if (flag==0):
        name='exemptions  '
    elif(flag==FAKER_GENERATOR):
        pass
    return name


def generate_exemptioncode(flag=0):
    if (flag==0):
        name='ex code '
    elif(flag==FAKER_GENERATOR):
        pass
    return name

def generate_address(flag=0,t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name = (t_faker.street_address().replace('\n', ' '))
    return name

def generate_city(flag=0, t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.street_address().replace('\n', ' ')
    return name

def generate_requester(flag=0, t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.name()+ ' ' + t_faker.city()
    return name

def generate_account(flag=0, t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.name()
    return name

def generate_social(flag=0, t_faker = None):
    if (flag==0):
        letter_set='0123456789'
        name = ''.join((random.choice(letter_set) for i in range(9)))
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker()
        name=t_faker.itin()
    return name

def generate_empid(flag=0, t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.bban()
    return name


def generate_signature(flag=0,t_faker = None, full_name=None):
    if (flag==0):
        if full_name is None:
            name='- '
        else:
            name = full_name
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name=t_faker.name()
    #elif (flag==SOME OTHER GENERATOR)
    return name

def generate_date(flag=0,t_faker = None):
    if (flag==0):
        name='- '
    elif(flag==FAKER_GENERATOR):
        if t_faker is None:
            t_faker=Faker(LOCALE)
        name = t_faker.date(pattern='%Y-%m-%d', end_datetime=None)    
        
    #elif (flag==SOME OTHER GENERATOR)
    return name

def generate_position(header_name=None, bias_x=0, bias_y = 0, field_locations=None):
    if field_locations is None:
        field_locations= {'Name':(190,255),
                          'BusinessName':(196,331), 
                          'Tax':(183,444),
                          'Instructions':(450,630), 
                          'Exemptions':(1405,571),
                          'ExemptionCode':(1503,460), 
                          'Address':(197,700),
                          'City':(195,760), 
                          'Requester':(1093,695),
                          'Account':(195,830),
                          'SocialSeciurityNumber':(1162,935), 
                          'EmpIdentificationNumber':(1162,1069),
                          'Signature':(366,1517),
                          'ssn1':(1162,933),
                          'ssn2':(1201,933),  
                          'ssn3':(1240,933),  
                          'ssn4':(1318,933),  
                          'ssn5':(1362,933),  
                          'ssn6':(1440,933),  
                          'ssn7':(1480,933),  
                          'ssn8':(1520,933),  
                          'ssn9':(1560,933),
                          'Tax2':(499,439),
                          'Tax3':(700,439),
                          'Tax4':(899,439),
                          'Tax5':(1100,439),
                          'Tax6':(183,511),
                          'Tax7':(183,638),
                          'Date':(1194,1519)     
              }      
        
    #     more Y-biasfor the character boxes
    if header_name.startswith('ssn'): 
        bias_y = int((random.random()-0.1) * 60)
        bias_x = int((random.random()-0.5) * 16)
    #     not too much bias for checkbox
    if header_name.startswith('Tax'): 
        bias_y = int((random.random()-0.5) * 5)
        bias_x = int((random.random()-0.5) * 5)    
    out_x = field_locations[header_name][0] + bias_x
    out_y = field_locations[header_name][1] + bias_y

    return out_x, out_y


def generate_data(size=1, metadata=False,output_flag="df",positions=None,x_bias=0,y_bias=0):
    i_faker = Faker(LOCALE)
    if positions is None:
        df = pd.DataFrame( columns=['Name','BusinessName','Tax','Instructions','Exemptions',
                                             'ExemptionCode','Address','City','Requester','Account',
                                             'SocialSeciurityNumber','EmpIdentificationNumber'])
        for i in range(size):
            name = generate_name(flag=1, t_faker = i_faker)
            bname = generate_bname(flag=FAKER_GENERATOR, t_faker = i_faker)
            tax = generate_tax()
            instructions = generate_instructions()
            exemptions = generate_exemptions()        
            exemptionCode = generate_exemptioncode()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            city = generate_city(flag=FAKER_GENERATOR, t_faker = i_faker)
            requester = generate_requester(flag=FAKER_GENERATOR, t_faker = i_faker)
            account = generate_account()
            social = generate_social(flag=FAKER_GENERATOR, t_faker = Faker())
            empid = generate_empid(flag=FAKER_GENERATOR, t_faker = i_faker)

            load= {'Name':name,'BusinessName':bname, 'Tax':tax,
               'Instructions':instructions, 'Exemptions':exemptions,
                'ExemptionCode':exemptionCode, 'Address':address,
               'City':city, 'Requester':requester,'Account':account,
                'SocialSeciurityNumber':social, 'EmpIdentificationNumber':empid
                  }  
            df = df.append(load, ignore_index=True)
    elif(positions==3):
        df = pd.DataFrame( columns=['Name','Tax','Address'])
        for i in range(size):
            name = generate_name(flag=1, t_faker = i_faker)
            tax = generate_tax()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            load= {'Name':name,'Tax':tax,
               'Address':address
                  }  
            df = df.append(load, ignore_index=True)        
            
    elif(positions==7):
        df = pd.DataFrame( columns=['Name','BusinessName','Tax',
                                             'Address','City','Requester',
                                             'Signature'])
        for i in range(size):
            name = generate_name(flag=1, t_faker = i_faker)
            bname = generate_bname(flag=FAKER_GENERATOR, t_faker = i_faker)
            tax = generate_tax()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            city = generate_city(flag=FAKER_GENERATOR, t_faker = i_faker)
            requester = generate_requester(flag=FAKER_GENERATOR, t_faker = i_faker)
            signature = generate_signature(flag=0, t_faker = i_faker,full_name=name)

            load= {'Name':name,'BusinessName':bname, 'Tax':tax,
               'Address':address,
               'City':city, 'Requester':requester, 
                'Signature':signature
                  }  
            df = df.append(load, ignore_index=True)  
            
    elif(positions==9):
        # SSN Only
        df = pd.DataFrame( columns=['ssn1','ssn2','ssn3','ssn4','ssn5','ssn6','ssn7','ssn8','ssn9'])
        for i in range(size):
            ssn=str(generate_social(flag=0))
            load= {'ssn1':ssn[0],
                   'ssn2':ssn[1],
                   'ssn3':ssn[2],
                   'ssn4':ssn[3],
                   'ssn5':ssn[4],
                   'ssn6':ssn[5],
                   'ssn7':ssn[6],
                   'ssn8':ssn[7],
                   'ssn9':ssn[8]
                  }  
            df = df.append(load, ignore_index=True)              

    elif(positions==16):
        # INFO + SSN Only
        df = pd.DataFrame( columns=['Name',
                                    'BusinessName',
                                    'Tax',
                                    'Address',
                                    'City',
                                    'Requester',
                                    'Signature',
                                    'ssn1',
                                    'ssn2',
                                    'ssn3',
                                    'ssn4',
                                    'ssn5',
                                    'ssn6',
                                    'ssn7',
                                    'ssn8',
                                    'ssn9'])
        for i in range(size):
            
            name = generate_name(flag=1, t_faker = i_faker)
            bname = generate_bname(flag=FAKER_GENERATOR, t_faker = i_faker)
            tax = generate_tax()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            city = generate_city(flag=FAKER_GENERATOR, t_faker = i_faker)
            requester = generate_requester(flag=FAKER_GENERATOR, t_faker = i_faker)
            signature = generate_signature(flag=0, t_faker = i_faker,full_name=name)
            ssn=str(generate_social(flag=0))
            load= {'Name':name,
                   'BusinessName':bname, 
                   'Tax':tax,
                   'Address':address,
                   'City':city, 
                   'Requester':requester, 
                   'Signature':signature,
                   'ssn1':ssn[0],
                   'ssn2':ssn[1],
                   'ssn3':ssn[2],
                   'ssn4':ssn[3],
                   'ssn5':ssn[4],
                   'ssn6':ssn[5],
                   'ssn7':ssn[6],
                   'ssn8':ssn[7],
                   'ssn9':ssn[8]
                  }  
            df = df.append(load, ignore_index=True)              

    elif(positions==23):
        # INFO + SSN Only
        df = pd.DataFrame( columns=['Name',
                                    'BusinessName',
                                    'Tax',
                                    'Address',
                                    'City',
                                    'Requester',
                                    'Signature',
                                    'ssn1',
                                    'ssn2',
                                    'ssn3',
                                    'ssn4',
                                    'ssn5',
                                    'ssn6',
                                    'ssn7',
                                    'ssn8',
                                    'ssn9',
                                    'Tax2',
                                    'Tax3',
                                    'Tax4',
                                    'Tax5',
                                    'Tax6',
                                    'Tax7',
                                    'Date'
                                   ])
        for i in range(size):
            
            name = generate_name(flag=1, t_faker = i_faker)
            bname = generate_bname(flag=FAKER_GENERATOR, t_faker = i_faker)
            tax = generate_tax()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            city = generate_city(flag=FAKER_GENERATOR, t_faker = i_faker)
            requester = generate_requester(flag=FAKER_GENERATOR, t_faker = i_faker)
            signature = generate_signature(flag=0, t_faker = i_faker,full_name=name)
            ssn=str(generate_social(flag=0))
            date=str(generate_date(flag=FAKER_GENERATOR))
            load= {'Name':name,
                   'BusinessName':bname, 
                   'Tax':tax,
                   'Address':address,
                   'City':city, 
                   'Requester':requester, 
                   'Signature':signature,
                   'ssn1':ssn[0],
                   'ssn2':ssn[1],
                   'ssn3':ssn[2],
                   'ssn4':ssn[3],
                   'ssn5':ssn[4],
                   'ssn6':ssn[5],
                   'ssn7':ssn[6],
                   'ssn8':ssn[7],
                   'ssn9':ssn[8],
                   'Tax2':tax,
                   'Tax3':tax,
                   'Tax4':tax,
                   'Tax5':tax,
                   'Tax6':tax,
                   'Tax7':tax,
                   'Date':date
                  }  
            df = df.append(load, ignore_index=True)                      
                    
    else:
        #TO DO Add other field location
            
        df = pd.DataFrame( columns=['Name','Name_loc','BusinessName','Tax','Instructions','Exemptions',
                                             'ExemptionCode','Address','City','Requester','Account',
                                             'SocialSeciurityNumber','EmpIdentificationNumber'])
        for i in range(size):
            name = generate_name(flag=1, t_faker = i_faker)
            bname = generate_bname(flag=FAKER_GENERATOR, t_faker = i_faker)
            tax = generate_tax()
            instructions = generate_instructions()
            exemptions = generate_exemptions()        
            exemptionCode = generate_exemptioncode()
            address = generate_address(flag=FAKER_GENERATOR, t_faker = i_faker)
            city = generate_city(flag=FAKER_GENERATOR, t_faker = i_faker)
            requester = generate_requester(flag=FAKER_GENERATOR, t_faker = i_faker)
            account = generate_account()
            social = generate_social(flag=FAKER_GENERATOR, t_faker = Faker())
            empid = generate_empid(flag=FAKER_GENERATOR, t_faker = i_faker)
            
            #TO DO prettify/refactor 
            t_posx,t_posy = generate_position(header_name='Name',bias_x=x_bias,bias_y=y_bias)    

            load= {'Name':name,'Name_loc':(t_posx,t_posy), 
                'BusinessName':bname, 'Tax':tax,
               'Instructions':instructions, 'Exemptions':exemptions,
                'ExemptionCode':exemptionCode, 'Address':address,
               'City':city, 'Requester':requester,'Account':account,
                'SocialSeciurityNumber':social, 'EmpIdentificationNumber':empid
                  }  
            df = df.append(load, ignore_index=True)
            
    if metadata:
        print("CSV output file is : " + metadata)
        df.index_label="uid"
        df.to_csv(metadata,index_label=None)
        
    if (output_flag=="df"):   
        return df
    elif (output_flag=="dict"):
        return df.to_dict()

