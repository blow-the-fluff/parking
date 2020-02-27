from PIL import Image


class SuperImpose():
    '''
    Utility superclass abstracting common functionality.
    '''
    @staticmethod
    def load_img(filename):
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

    @staticmethod
    def convert_2_rgba(img):
        '''
        Input:
        img: PIL object - RGB image
        Return:
        rgba_img: PIL object - RGBA image
        '''
        rgba_img = img.convert('RGBA')
        return rgba_img

    @staticmethod
    def super_impose(back_rgba_img, fore_rgba_img, loc_x, loc_y):
        '''
        Inputs:
        back_rgba_img: PIL object - background image in RGBA format
        fore_rgba_img: PIL object - foreground image in RGBA format
        loc_x, loc_y: Int - x,y locations  pixel co-ordinates
                            where forground is to be superimposed on background
                            Note: top left corner is 0,0
        Return:
        superimposed_img: PIL object - super imposed image
        '''
        # Need to copy due to in place manipulation of object,
        # if not copied will manipulate reference and will return None
        superimposed_img = back_rgba_img.copy()
        superimposed_img.paste(fore_rgba_img, (loc_x, loc_y), fore_rgba_img)
        return superimposed_img

    @staticmethod
    def save_img(img, filename, filetype):
        '''
        Inputs:
        img: PIL object - image
        filename: String - file to save image with path and file extension
        filetype: Sting - filetype eg: 'PNG'
        '''
        try:
            img.save(filename, filetype.upper())
        except IOError:
            print('Error saving image as: {} at: {}'.format(
                filetype.upper(), filename))
