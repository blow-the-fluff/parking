from os.path import join
from SuperImposeFields import SuperImposeFields


class SuperImposeFieldsFromFiles(SuperImposeFields):
    '''
    SuperImposeFields subclass implementing specific functionality to
    load image files using form id and to create `fields_img_loc_dict` dictionary
    To initiate super imposing call property: `superimposed_img`
    Note: Once `superimposed_img` is set it cannot be changed/updated.
    '''
    def __init__(self, form_id, fields_dict, background_img_filename, fields_imgs_path, filetype):
        '''
        Inputs:
        form_id: String - form id (to be used to load relevant field images)
        fields_dict: Dict - dictionary i.e.: {field_name: (loc_x, loc_y)}
        background_img_filename: String - background image filename with absolute path
        fields_imgs_path: String - path to folder where field images are saved
                                    files name format: `formid_fieldname_locx_locy.ext`
        filetype: String - filetype of field images eg: 'png', 'jpg'
        '''
        self.form_id = form_id
        self.fields_dict = fields_dict
        self.background_img_filename = background_img_filename
        self.fields_imgs_path = fields_imgs_path
        self.filetype = filetype
        self._fields_img_loc_dict = None
        self._superimposed_img = None

    @property
    def fields_img_loc_dict(self):
        '''
        Return:
        self._fields_img_loc_dict: dict - {field_name: {img: PIL object, loc: (x,y) }}
        Note:
        if self._fields_img_loc_dict is not set then will set/intialise it by calling:
        self.set_fields_img_loc_dict()
        '''
        if self._fields_img_loc_dict is None:
            self.set_fields_img_loc_dict()
        return self._fields_img_loc_dict

    def set_fields_img_loc_dict(self):
        '''
        Function sets self._fields_img_loc_dict dictionary value
        '''
        fields_img_loc_dict = {}
        for field_name, loc in self.fields_dict.items():
            field_img_filename = '{}_{}_{}_{}.{}'.format(
                self.form_id, field_name, loc[0], loc[1], self.filetype)
            field_img_filename = join(self.fields_imgs_path, field_img_filename)
            field_img = self.load_img(field_img_filename)
            field_img = self.convert_2_rgba(field_img)
            fields_img_loc_dict[field_name] = {'img': field_img, 'loc': loc}
        self._fields_img_loc_dict = fields_img_loc_dict

    @property
    def superimposed_img(self):
        '''
        Return:
        self._superimposed_img: PIL object - superimposed image in RGBA format
        Note:
        if self._superimposed_img is not set then will set/intialise it by calling:
        self.set_superimposed_img()
        '''
        if self._superimposed_img is None:
            self.set_superimposed_img()
        return self._superimposed_img

    def set_superimposed_img(self):
        '''
        Function sets self._superimposed_img PIL image object
        '''
        background_img = self.load_img(self.background_img_filename)
        background_img = self.convert_2_rgba(background_img)
        self._superimposed_img = self.run_super_impose_on_all_fields(
            background_img, self.fields_img_loc_dict)

    def save_superimposed_img(self, filename, filetype, verbose=True):
        if verbose:
            print('Saving superimpose image at: {} as: {} type image'.format(filename, filetype))
        self.save_img(self.superimposed_img, filename, filetype)
        if verbose:
            print('Done!')
