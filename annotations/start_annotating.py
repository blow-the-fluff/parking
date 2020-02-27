from Annotations import Annotations


background_img_filename = '/home/jupyter/forms-ocr/superimpose/w9_blank_form.png'
# fields_imgs_path = '../../field_img_data/img/'
fields_imgs_path = '../data/data_16f/'

# /home/jupyter/forms-ocr/handwriting-synthesis/temp_annotations/
folder_to_save = '../data/data_16f_train/'

field_margin = 10.0

# ## 3 fields
# field_label_mapping = {
#     'Name': '0',
#     'Tax': '1',
#     'Address': '2'
# }

## 7 fields
# field_label_mapping = {
#     'Name': '0',
#     'Tax': '1',
#     'Address': '2',
#     'BusinessName': '3',
#     'City': '4',
#     'Requester': '5',
#     'Signature': '6'
# }

# ## SSN
# field_label_mapping = {
#     'ssn1': '0',
#     'ssn2': '1',
#     'ssn3': '2',
#     'ssn4': '3',
#     'ssn5': '4',
#     'ssn6': '5',
#     'ssn7': '6',
#     'ssn8': '7',
#     'ssn9': '8'
# }

## SSN + info
field_label_mapping = {
    'Name': '0',
    'Tax': '1',
    'Address': '2',
    'BusinessName': '3',
    'City': '4',
    'Requester': '5',
    'Signature': '6',
    'ssn1': '7',
    'ssn2': '8',
    'ssn3': '9',
    'ssn4': '10',
    'ssn5': '11',
    'ssn6': '12',
    'ssn7': '13',
    'ssn8': '14',
    'ssn9': '15'
}

# ## SSN
# field_label_mapping = {
# #     'Name': '0',
# #     'Tax': '1',
# #     'Address': '2',
# #     'BusinessName': '3',
# #     'City': '4',
# #     'Requester': '5',
# #     'Signature': '6',
#     'ssn1': '7',
#     'ssn2': '8',
#     'ssn3': '9',
#     'ssn4': '10',
#     'ssn5': '11',
#     'ssn6': '12',
#     'ssn7': '13',
#     'ssn8': '14',
#     'ssn9': '15'
# }

# FORM_FIELD_OUTPUT = {'Name':True,'BusinessName':True, 'Tax':True,
#        'Instructions':True, 'Exemptions':True,
#         'ExemptionCode':True, 'Address':True,
#        'City':True, 'Requester':True,'Account':True,
#         'SocialSeciurityNumber':True, 'EmpIdentificationNumber':True
#           }


def run(background_img_filename, fields_imgs_path, folder_to_save, field_label_mapping, field_margin, **kwargs):
    annotations = Annotations(background_img_filename, fields_imgs_path, folder_to_save, field_label_mapping, field_margin=field_margin, **kwargs)
    annotations.start_annotating()


if __name__ == '__main__':
    run(background_img_filename, fields_imgs_path, folder_to_save, field_label_mapping, field_margin)
