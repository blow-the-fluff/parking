from InitiateSuperImpose import InitiateSuperImpose
import os

background_img_filename = './w9_blank_form.png'
# fields_imgs_path = '/home/jupyter/forms-ocr/handwriting-synthesis/temp_3fields/'
# folder_to_save = '/home/jupyter/forms-ocr/handwriting-synthesis/temp_3fields_train'
fields_imgs_path = '/home/jupyter/forms-ocr/data/data_16f/'
folder_to_save = '/home/jupyter/forms-ocr/data/data_16f_train/'


def run(background_img_filename, fields_imgs_path, folder_to_save, **kwargs):
    if not os.path.exists(folder_to_save):
        os.mkdir(folder_to_save)    
    init_superimpose = InitiateSuperImpose(
        background_img_filename,
        fields_imgs_path,
        folder_to_save,
        **kwargs)

    init_superimpose.start_save_superimposing()


if __name__ == '__main__':
    run(background_img_filename, fields_imgs_path, folder_to_save)
