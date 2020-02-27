from os import listdir
from os.path import join
from SuperImposeFieldsFromFiles import SuperImposeFieldsFromFiles


class InitiateSuperImpose():
    '''
    A utility/helper class to encapsulate creating SuperImpose objects and saving outputs
    '''
    def __init__(
        self,
        background_img_filename,
        fields_imgs_path,
        folder_to_save,
        filetype='png',
        sep='_',
        **kwargs
    ):
        '''
        Inputs:
        background_img_filename: String - background image filename with absolute path
        fields_imgs_path: String - path to folder where field images are saved
                                    files name format: `formid_fieldname_locx_locy.ext`
        filetype: String - filetype of field images eg: 'png', 'jpg'
        folder_to_save: String - folder/location where to save output
        sep: String - used to split filenames
        '''
        self.background_img_filename = background_img_filename
        self.fields_imgs_path = fields_imgs_path
        self.folder_to_save = folder_to_save
        self.filetype = filetype
        self.sep = sep
        self.kwargs = kwargs

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
    def forms_fields_dict(self):
        '''
        Return:
        forms_fields_dict: nested dict - {form_id: {field_name: (loc_x, loc_y)}}
        Note:
        Can be set using `forms_fields_dict` kwargs or will lazy instatiate it
        '''
        if hasattr(self, '_forms_fields_dict'):
            return self._forms_fields_dict
        elif self.kwargs.get('forms_fields_dict'):
            self._forms_fields_dict = self.kwargs['forms_fields_dict']
        else:
            self._forms_fields_dict = self.set_forms_fields_dict()
        return self._forms_fields_dict

    def get_fields(self, f_id):
        '''
        Input:
        f_id: String - form id
        Return:
        fields: nested list - nested list of all fields that belong to same form id
        '''
        fields = list(filter(lambda s_f: s_f[0] == f_id, self.split_files))
        return fields

    def get_form_fields_dict(self, f_id):
        '''
        Input:
        f_id: String - form id
        Return:
        form_fields_dict: dict - a dictionary of fields and locations for given form id:
                                    {field_name: (loc_x, loc,y)}
        '''
        form_fields_dict = {}
        fields_dict = {}
        fields = self.get_fields(f_id)
        for data in fields:
            field_name = data[1]
            loc_x = data[2]
            loc_y = data[3]
            fields_dict[field_name] = (int(loc_x), int(loc_y))
        form_fields_dict[f_id] = fields_dict
        return form_fields_dict

    def set_forms_fields_dict(self):
        '''
        Return:
        forms_fields_dict: nested dict - {form_id: {field_name: (loc_x, loc_y)}}
        Note:
        Function instantiates and sets forms_fields_dict property
        '''
        forms_fields_dict_list = list(map(self.get_form_fields_dict, self.form_ids))
        forms_fields_dict = {f_id: f_d for f_f_d in forms_fields_dict_list for f_id, f_d in f_f_d.items()}
        return forms_fields_dict

    def start_save_superimposing_single_form(self, f_id):
        '''
        A helper function that is mapped/can be used for parallel processing.
        This function creates the SuperImposeFieldsFromFiles object for given id
        and saves the output to defined location with predefined name using form_id
        Input:
        f_id: String - form id
        '''
        field_dict = self.forms_fields_dict[f_id]
        super_impose = SuperImposeFieldsFromFiles(
            f_id,
            field_dict,
            self.background_img_filename,
            self.fields_imgs_path,
            self.filetype
        )
        filename = '{}.{}'.format(f_id, self.filetype)
        filename = join(self.folder_to_save, filename)
        super_impose.save_superimposed_img(filename, self.filetype)

    def map_func(self):
        '''
        Return:
        map_func: function - map function to use
        Note:
        Can set a pool.map using `map_func` kwargs or else will return default map
        '''
        if self.kwargs.get('map_func'):
            return self.kwargs['map_func']
        else:
            return map

    def start_save_superimposing(self):
        '''
        A helper/utility function to map: `start_save_superimposing_single_form` on all form ids.
        '''
        _ = list(self.map_func()(self.start_save_superimposing_single_form, self.form_ids))
