from SuperImpose import SuperImpose


class SuperImposeFields(SuperImpose):
    '''
    SuperImpose subclass implementing specific functionality to
    super-impose all field images on background image
    '''
    @staticmethod
    def run_super_impose_on_all_fields(back_rgba_img, fields_img_loc_dict):
        '''
        Inputs:
        back_rgba_img: PIL object - background image in RGBA format
        fields_img_loc_dict: Dict - dictionary i.e.:
                            {field_name: {img: PIL object, loc: (x,y) }}
        Return:
        superimposed_img: PIL object - superimposed image in RGBA format
        '''
        superimposed_img = back_rgba_img.copy()
        for field_name, img_loc in fields_img_loc_dict.items():
            field_img = img_loc['img']
            field_loc = img_loc['loc']
            superimposed_img = SuperImpose.super_impose(superimposed_img, field_img, field_loc[0], field_loc[1])
        return superimposed_img
