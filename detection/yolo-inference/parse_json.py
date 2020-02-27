import json, os

def get_filename(json_obj):
    return json_obj['filename']

def get_index(json_obj):
    temp_filename = get_filename(json_obj).split('/')
    return temp_filename[-1].split('.')[0]

def get_field_name(field_obj):
    return field_obj['name']

def get_center_x(field_obj):
    return field_obj['relative_coordinates']['center_x']
def get_center_y(field_obj):
    return field_obj['relative_coordinates']['center_y']
def get_height(field_obj):
    return field_obj['relative_coordinates']['height']
def get_width(field_obj):
    return field_obj['relative_coordinates']['width']
from PIL import Image

def get_size(json_obj):
    fname = get_filename(json_obj)
    im = Image.open(fname)
    width, height = im.size
    return width,height


input_json ='../yolo/result_rwdata_70iou.json'
output_directory = './out_rwdata/'
DEBUG = False

if __name__ == '__main__':
    temp_out_dir = output_directory
    if not os.path.exists(output_directory):
        os.mkdir(temp_out_dir)      
    with open(input_json) as f:
        data = json.load(f)
    
    

    # Parse entire file and convert to image
    for distro in data:
        if DEBUG: print(get_filename(distro))
        im = Image.open(get_filename(distro))    
        width_px, height_px = get_size(distro)
        index = get_index(distro)
        obj = distro['objects']
        for field in obj:
            fieldname = get_field_name(field)
            center_x_px = get_center_x(field)*width_px
            center_y_px = get_center_y(field)*height_px
            width = get_width(field) * width_px* 1.03
            height = get_height(field)* height_px * 1.03
            top_left_x = int(center_x_px-width/2)
            top_left_y = int(center_y_px-height/2)
            btm_right_x = int(center_x_px+width/2)
            btm_right_y = int(center_y_px+height/2)


            out_filename = '%s_%s.png'%(index,fieldname)
            if DEBUG: print(out_filename)

            im1 = im.crop((top_left_x, top_left_y, btm_right_x, btm_right_y)) 
            im1.save(temp_out_dir+out_filename, 'png')

            if DEBUG: break
        if DEBUG: break