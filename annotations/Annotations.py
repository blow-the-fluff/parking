from os import listdir
from os.path import join
from PIL import Image
import numpy as np


class Annotations():
    def __init__(
        self,
        background_img_filename,
        fields_imgs_path,
        folder_to_save,
        field_label_mapping,
        filetype='png',
        sep='_',
        field_margin=5,
        **kwargs
    ):
        '''
        Inputs:
        background_img_filename: String - background image filename with absolute path
        fields_imgs_path: String - path to folder where field images are saved
                                    files name format: `formid_fieldname_locx_locy.ext`
        filetype: String - filetype of field images eg: 'png', 'jpg'
        folder_to_save: String - folder/location where to save output
        field_label_mapping: Dict - Dictionary mapping of field label mapping to integer values.
        sep: String - used to split filenames
        margin: Int - additional margin around bounding box, will be added to yolo height and width
        '''
        self.background_img_filename = background_img_filename
        self.fields_imgs_path = fields_imgs_path
        self.folder_to_save = folder_to_save
        self.field_label_mapping = field_label_mapping
        self.filetype = filetype
        self.sep = sep
        self.kwargs = kwargs
        self.field_margin=field_margin

    def load_img(self, filename):
        '''
        Input:
        filename: String - image filename to load using PIL.Image
        Return:
        img: PIL object - loaded image
        '''
        try:
            img = Image.open(filename)
            return img
        except IOError:
            print('Error oppening file: {}'.format(filename))

    def get_files(self, folder, filetype):
        '''
        Inputs:
        folder: String - folder from where to extract files
        filetype: String - filetype of field images eg: 'png', 'jpg'
        Return:
        files: List - list of files in folder of given filetype
        '''
        files = listdir(folder)
        files = list(filter(lambda f: '.{}'.format(filetype) in f, files))
        return files

    def remove_file_extn(self, f):
        '''
        Input:
        f: String - filename
        Return:
        r_f: String - filename without extension i.e. part after `.` removed
        '''
        r_f = f.split('.')[0]
        return r_f

    def split_filename(self, f):
        '''
        Input:
        f: String - filename
        Return:
        s_f: list - list containing split filename string
        '''
        s_f = f.split(self.sep)
        return s_f

    @property
    def split_files(self):
        '''
        Return:
        split_files: nested list - list of split filenames
        Note:
        Can be set using `split_files` kwargs or will lazy instatiate it
        '''
        if hasattr(self, '_split_files'):
            return self._split_files
        elif self.kwargs.get('split_files'):
            self._split_files = self.kwargs['split_files']
        else:
            self._split_files = self.set_split_files()
        return self._split_files

    def set_split_files(self):
        '''
        Return:
        split_files: nested list - list of split filenames
        Note:
        Function instantiates and sets split_files property
        '''
        files = self.get_files(self.fields_imgs_path, self.filetype)
        files = list(map(self.remove_file_extn, files))
        # Split files names to extract form id, field name and loc x, loc y
        # split_files is a list of list / nested list
        split_files = list(map(self.split_filename, files))
        return split_files

    @property
    def form_ids(self):
        '''
        Return:
        form_ids: list - list of unique form ids
        Note:
        Can be set using `form_ids` kwargs or will lazy instatiate it
        '''
        if hasattr(self, '_form_ids'):
            return self._form_ids
        elif self.kwargs.get('form_ids'):
            self._form_ids = self.kwargs['form_ids']
        else:
            self._form_ids = self.set_form_ids()
        return self._form_ids

    def set_form_ids(self):
        '''
        Return:
        form_ids: list - list of unique form ids
        Note:
        Function instantiates and sets form_ids property
        '''
        form_ids = [s_f[0] for s_f in self.split_files]
        form_ids = list(set(form_ids))
        return form_ids

    @property
    def forms_annot_dict(self):
        '''
        Return:
        forms_annot_dict: nested dict - {form_id: {field_name: (x, y, w, h)}}
        Note:
        Can be set using `forms_annot_dict` kwargs or will lazy instatiate it
        '''
        if hasattr(self, '_forms_annot_dict'):
            return self._forms_annot_dict
        elif self.kwargs.get('forms_annot_dict'):
            self._forms_annot_dict = self.kwargs['forms_annot_dict']
        else:
            self._forms_annot_dict = self.set_forms_annot_dict()
        return self._forms_annot_dict

    def get_fields(self, f_id):
        '''
        Input:
        f_id: String - form id
        Return:
        fields: nested list - nested list of all fields that belong to same form id
        '''
        fields = list(filter(lambda s_f: s_f[0] == f_id, self.split_files))
        return fields

    
    def convert(self, shape, box, field_margin):
        '''
        Converts data to YOLO format: https://stackoverflow.com/questions/56115874/how-to-convert-bounding-box-x1-y1-x2-y2-to-yolo-style-x-y-w-h
        Inputs:
        shape: tuple: (Num_of_Rows:Int, Num_of_Columns:Int) - 
                        shape of background image, used to normalize values
        box: list/tuples: (X_min, X_max, Y_min, Y_max) - i.e.:
                           X_min = loc_x (left corner top X point of diagonal), 
                           X_max = loc_x + img_num_of_cols (right corner bottom X point of diagonal)
                           Y_min = loc_y (left corner top Y point of diagonal), 
                           Y_max = loc_y + img_num_of_rows (right corner bottom Y point of diagonal)
        margin: int: pixels to add around handwriting (defaults to 0 for tight bounding box)
        Returns:
        (x, y, w, h): tuple: x,y - centre points, w - width, h - height
        '''
        
        if field_margin is None:
            field_margin = 0.0
        
        dw = 1./shape[1]
        dh = 1./shape[0]
        x = (box[0] + box[1])/2.0
        y = (box[2] + box[3])/2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = (w + field_margin) * dw
        y = y*dh
        h = (h + field_margin) * dh
        return (x, y, w, h)

    def get_form_annots_dict(self, f_id):
        '''
        Input:
        f_id: String - form id
        Return:
        form_annots_dict: dict - a dictionary of fields and locations for given form id:
                                    {field_name: (x, y, w, h)}
        '''
        form_annots_dict = {}
        fields_dict = {}
        fields = self.get_fields(f_id)
        for data in fields:
            field_name = data[1]
            loc_x = int(data[2])
            loc_y = int(data[3])
            img_filename = '{}_{}_{}_{}.{}'.format(f_id, field_name, loc_x, loc_y, self.filetype)
            img_filename = join(self.fields_imgs_path, img_filename)
            img = self.load_img(img_filename)
            img_shape = np.array(img).shape
            # box = (X_min, X_max, Y_min, Y_max) i.e.diagonal point values
            box = (loc_x,loc_x + img_shape[1], loc_y, loc_y + img_shape[0])
            #  Normalize w.r.t background image
            background_img = self.load_img(self.background_img_filename)
            background_img_shape = np.array(background_img).shape
            annot = self.convert(background_img_shape, box, self.field_margin)
            fields_dict[field_name] = annot
        form_annots_dict[f_id] = fields_dict
        return form_annots_dict

    def set_forms_annot_dict(self):
        '''
        Return:
        forms_annot_dict: nested dict - {form_id: {field_name: (x, y, w, h)}}
        Note:
        Function instantiates and sets forms_annot_dict property
        '''
        forms_annot_dict_list = list(map(self.get_form_annots_dict, self.form_ids))
        forms_annot_dict = {f_id: f_d for f_f_d in forms_annot_dict_list for f_id, f_d in f_f_d.items()}
        return forms_annot_dict

    def write_annot(self, filename, annot_string):
        '''
        Inputs:
        filename: String - filename with path to write data/annotated string
        annot_string: String - A single/data to written
        '''
        annot_file = open(filename, 'w')
        annot_file.write(annot_string)
        annot_file.close()

    def start_annotating(self):
        '''
        Creates annotation strings and writes them to file.
        '''
        for f_id, f_dict in self.forms_annot_dict.items():
            annot_strings_list = []
            for f_name, annot in f_dict.items():
                field_label = self.field_label_mapping[f_name]
                template_string = '{} {} {} {} {}'.format(field_label, *annot)
                annot_strings_list.append(template_string)
            annot_strings_list.sort(key=lambda s: int(s.split()[0]))
            annot_string = '\n'.join(annot_strings_list)
            annot_filename = '{}.txt'.format(f_id)
            annot_filename = join(self.folder_to_save, annot_filename)
            self.write_annot(annot_filename, annot_string)
