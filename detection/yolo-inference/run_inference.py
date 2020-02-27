import os, shutil, json
from PIL import Image


ROOT_PATH='/home/jupyter/demo/forms-ocr/detection/yolo-inference/'
DETECTION_PATH=ROOT_PATH+'../'
YOLO_PATH=DETECTION_PATH+'/yolo/'
DARKNET_PATH=YOLO_PATH+'darknet/'

IMG_FILENAME=YOLO_PATH+'104641.png'

OUTPUT_FOLDER='/home/jupyter/demo/forms-ocr/detection/yolo-inference/output/'

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

def get_size(json_obj):
    fname = get_filename(json_obj)
    im = Image.open(fname)
    width, height = im.size
    return width,height

def run_annotation(img_filename, folder_to_save, **kwargs):
    
    cmd = DARKNET_PATH + 'darknet detect ' +  YOLO_PATH+'yolov3-tiny-23f-b2-832.cfg ' + \
    YOLO_PATH + 'backup/yolov3-tiny-23f-b2-832_last.weights ' + img_filename
    
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    os.chdir(DARKNET_PATH)
    cmd ='./darknet detect ../yolov3-tiny-23f-b2-832.cfg ../backup/yolov3-tiny-23f-b2-832_last.weights ' + img_filename    
    os.system(cmd)
    shutil.move("predictions.jpg",OUTPUT_FOLDER)
    os.chdir(ROOT_PATH)        
        
def generate_json(img_filename, folder_to_save, **kwargs):
    
    os.chdir(YOLO_PATH)    
    
    cmd2 = DARKNET_PATH + 'darknet detector test obj-23f-b2.data  yolov3-tiny-23f-b2-832.cfg ' + \
    YOLO_PATH + 'backup/yolov3-tiny-23f-b2-832_last.weights -iou_thresh 0.70 -ext_output ' + \
    '-dont_show -out predictions.json ' + img_filename    
    
    os.system(cmd2)        
    shutil.move("predictions.json",OUTPUT_FOLDER)
    
    
    os.chdir(ROOT_PATH)   
    
def generate_cropped_images(img_filename, folder_to_save, **kwargs):
    
    os.chdir(YOLO_PATH)    
    with open(OUTPUT_FOLDER+'predictions.json') as f:
        data = json.load(f)

    DEBUG = False
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
            
            im1.save(OUTPUT_FOLDER+out_filename, 'png')

            if DEBUG: break
        if DEBUG: break        
            
    os.chdir('../yolo-inference')   
    
def run_infer(img_filename, folder_to_save, **kwargs):
    run_annotation(img_filename, folder_to_save)

    generate_json(img_filename, folder_to_save)
    
    generate_cropped_images(img_filename, folder_to_save)
            
if __name__ == '__main__':

    run_infer(img_filename=IMG_FILENAME, folder_to_save=OUTPUT_FOLDER)
