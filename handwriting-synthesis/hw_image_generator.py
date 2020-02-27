import os
import logging
import timeit

import numpy as np
import svgwrite
import random

from cairosvg import svg2png
from PIL import Image

import drawing
import lyrics
from rnn import rnn

from hw_generator_config import *
from form_presets import *
from customer_data_generators import *

def convert_svg(svg, writetolocation):
    return svg2png(url=svg, write_to=writetolocation)

def white_to_transparency(img):
    x = np.asarray(img.convert('RGBA')).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)

def crop_image(img):
    arr = np.array(img)
    if arr.ndim>2:
        arr=arr[:,:,0]
    fromtop = []
    for i in range(arr.shape[0]):
        if np.mean(arr[i]) !=255:
            fromtop.append(i)     
    fromleft = []
    for i in range(arr.shape[1]):
        if np.mean(arr.T[i]) !=255:
            fromleft.append(i)
    top = fromtop[0]
    bottom = fromtop[-1]
    left = fromleft[0]
    right = fromleft[-1]
    img = img.crop((left,top,right,bottom))
    shapearray = np.array(img)
    bottomx = shapearray.shape[1]
    bottomy = shapearray.shape[0]
    #TO DO - MAKE A SEPARATE X,Y LOCATION GENERATOR
    return img, bottomx, bottomy


    
def interface_read_from_file(input_formid = None ,path_to_field_img = None, path_to_template = None):
    
    field_name_dict= {'Name':(190,255),'BusinessName':(196,331), 'Tax':(183,444),
       'Instructions':(450,630), 'Exemptions':(1405,571),
        'ExemptionCode':(1503,460), 'Address':(197,700),
       'City':(195,760), 'Requester':(1093,695),'Account':(195,830),
        'SocialSeciurityNumber':(1162,935), 'EmpIdentificationNumber':(1162,1069)
          }      
    path_to_field_img = GEN_FOLDER
    path_to_template = ROOT_FOLDER + "/templates/w9_template.png"
    
    return form_id, field_name_dict, path_to_field_img, path_to_template


class Hand(object):

    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        self.nn = rnn(
            log_dir='logs',
            checkpoint_dir='checkpoints',
            prediction_dir='predictions',
            learning_rates=[.0001, .00005, .00002],
            batch_sizes=[32, 64, 64],
            patiences=[1500, 1000, 500],
            beta1_decays=[.9, .9, .9],
            validation_batch_size=32,
            optimizer='rms',
            num_training_steps=100000,
            warm_start_init_step=17900,
            regularization_constant=0.0,
            keep_prob=1.0,
            enable_parameter_averaging=False,
            min_steps_to_checkpoint=2000,
            log_interval=20,
            logging_level=logging.CRITICAL,
            grad_clip=10,
            lstm_size=400,
            output_mixture_components=20,
            attention_mixture_components=10
        )
        self.nn.restore()

    def write(self, filename, lines, biases=None, styles=None, stroke_colors=None, stroke_widths=None):
        valid_char_set = set(drawing.alphabet)
        for line_num, line in enumerate(lines):
            if len(line) > 75:
                raise ValueError(
                    (
                        "Each line must be at most 75 characters. "
                        "Line {} contains {}"
                    ).format(line_num, len(line))
                )

            for char in line:
                 
                if char not in valid_char_set:
                    if char.lower() not in valid_char_set:
                        raise ValueError(
                            (
                                "Invalid character {} or corresponding lowercase {} detected in line {}. "
                                "Valid character set is {}"
                            ).format(char,char.lower(), line_num, valid_char_set)
                            )
                    else:
                        char = char.lower()
                            
#                     raise ValueError(
#                         (
#                             "Invalid character {} detected in line {}. "
#                             "Valid character set is {}"
#                         ).format(char, line_num, valid_char_set)
#                     )
                

        strokes = self._sample(lines, biases=biases, styles=styles)
        self._draw(strokes, lines, filename, stroke_colors=stroke_colors, stroke_widths=stroke_widths)

    def _sample(self, lines, biases=None, styles=None):
        num_samples = len(lines)
        max_tsteps = 40*max([len(i) for i in lines])
        biases = biases if biases is not None else [0.5]*num_samples

        x_prime = np.zeros([num_samples, 1200, 3])
        x_prime_len = np.zeros([num_samples])
        chars = np.zeros([num_samples, 120])
        chars_len = np.zeros([num_samples])

        if styles is not None:
            for i, (cs, style) in enumerate(zip(lines, styles)):
                x_p = np.load('styles/style-{}-strokes.npy'.format(style))
                c_p = np.load('styles/style-{}-chars.npy'.format(style)).tostring().decode('utf-8')

                c_p = str(c_p) + " " + cs
                c_p = drawing.encode_ascii(c_p)
                c_p = np.array(c_p)

                x_prime[i, :len(x_p), :] = x_p
                x_prime_len[i] = len(x_p)
                chars[i, :len(c_p)] = c_p
                chars_len[i] = len(c_p)

        else:
            for i in range(num_samples):
                encoded = drawing.encode_ascii(lines[i])
                chars[i, :len(encoded)] = encoded
                chars_len[i] = len(encoded)

        [samples] = self.nn.session.run(
            [self.nn.sampled_sequence],
            feed_dict={
                self.nn.prime: styles is not None,
                self.nn.x_prime: x_prime,
                self.nn.x_prime_len: x_prime_len,
                self.nn.num_samples: num_samples,
                self.nn.sample_tsteps: max_tsteps,
                self.nn.c: chars,
                self.nn.c_len: chars_len,
                self.nn.bias: biases
            }
        )
        samples = [sample[~np.all(sample == 0.0, axis=1)] for sample in samples]
        return samples

    def _draw(self, strokes, lines, filename, stroke_colors=None, stroke_widths=None):
        stroke_colors = stroke_colors or ['black']*len(lines)
        stroke_widths = stroke_widths or [2]*len(lines)

        line_height = 60
        view_width = 1000
        view_height = line_height*(len(strokes) + 1)

        dwg = svgwrite.Drawing(filename=filename)
        dwg.viewbox(width=view_width, height=view_height)
        dwg.add(dwg.rect(insert=(0, 0), size=(view_width, view_height), fill='white'))

        initial_coord = np.array([0, -(3*line_height / 4)])
        for offsets, line, color, width in zip(strokes, lines, stroke_colors, stroke_widths):

            if not line:
                initial_coord[1] -= line_height
                continue

            offsets[:, :2] *= 1.5
            strokes = drawing.offsets_to_coords(offsets)
            strokes = drawing.denoise(strokes)
            strokes[:, :2] = drawing.align(strokes[:, :2])

            strokes[:, 1] *= -1
            strokes[:, :2] -= strokes[:, :2].min() + initial_coord
            strokes[:, 0] += (view_width - strokes[:, 0].max()) / 2

            prev_eos = 1.0
            p = "M{},{} ".format(0, 0)
            for x, y, eos in zip(*strokes.T):
                p += '{}{},{} '.format('M' if prev_eos == 1.0 else 'L', x, y)
                prev_eos = eos
            path = svgwrite.path.Path(p)
            path = path.stroke(color=color, width=width, linecap='round').fill("none")
            dwg.add(path)

            initial_coord[1] -= line_height

        dwg.save()
        
        
class FormFiller(Hand):
    def __init__(self):
        super().__init__()
        self.bias = 0.75
        self.style = 12
        
    def generate_image(self,input_text="test",output_image_path="test.svg",handwriting_style = HANDWRITING_FIXED):
        lines = [input_text]
        
        if (handwriting_style==HANDWRITING_FIXED):
            biases = [self.bias for i in lines]
            styles = [self.style for i in lines]
        else :
            biases = self.bias *np.flip(np.cumsum([len(i) == 0 for i in lines]), 0)
            styles = np.cumsum(np.array([len(i) for i in lines]) == 0).astype(int)
            


        self.write(
          filename=output_image_path,
          lines=lines,
          biases=biases,
          styles=styles,
          )
        
    def generate_image_transparent(self,input_text="test",output_image_path="test.png",handwriting_style = HANDWRITING_FIXED):

        lines = [input_text]
        try:
            if (handwriting_style==HANDWRITING_FIXED):
                pass
            elif (handwriting_style==HANDWRITING_PRESET_FLAG):
                self.set_handwriting()     
            else :
                biases = self.bias *np.flip(np.cumsum([len(i) == 0 for i in lines]), 0)
                styles = np.cumsum(np.array([len(i) for i in lines]) == 0).astype(int)
                
            biases = [self.bias for i in lines]
            styles = [self.style for i in lines]
            
            self.write(
              filename="temp.svg",
              lines=lines,
              biases=biases,
              styles=styles,
            )        
            convert_svg("temp.svg", output_image_path)
            img = Image.open(output_image_path)
            img = crop_image(img)[0]
            img = white_to_transparency(img)
            img.save(output_image_path)
            
        except:
            try:
                biases = [0.9 for i in lines]
                styles = [10 for i in lines]

                self.write(
                  filename="temp.svg",
                  lines=lines,
                  biases=biases,
                  styles=styles,
              )        
                convert_svg("temp.svg", output_image_path)
                img = Image.open(output_image_path)
                img = crop_image(img)[0]
                img = white_to_transparency(img)
                img.save(output_image_path)
            except:
                # Failed even the second time
                print('empty image ' , output_image_path)
            
            
    def set_handwriting(self,handwriting_presets=None,in_bias=None,in_style=None):
        if in_bias is not None and in_style is not None:
            self.bias = in_bias
            self.style = in_style
        else:
            preset_dict = HANDWRITING_PRESET            
            
            if handwriting_presets is None:
                handwriting_presets = random.randint(0,len(preset_dict)-1)

            self.bias,self.style = preset_dict[str(handwriting_presets)]
            
    def generate_data(self,size=1,in_positions=None,start_id = 0):
        self.info_df = generate_data(size,positions=in_positions)
        self.info_df.index+=start_id
        self.info_df.index.names=["uid"]
        
    def data_to_csv(self,output_file = "metadata.csv"):
        self.info_df.to_csv(output_file)
           
    def field_iterator(self, input_field_dict = None, start_id = 0, input_root = "./", input_df = None,x_bias=0,y_bias=0,handwriting_style=None,**kwargs):
        if input_df is None:
            temp_info_df = generate_data(1)
            for key in input_field_dict:
                temp_x, temp_y = generate_position(header_name = key,bias_x=x_bias,bias_y=y_bias)
                temp_path = input_root + "/" + str(start_id) + "_" + key + \
                                        "_" + str(temp_x) + "_" + \
                                        str(temp_y) + ".png"
                self.generate_image_transparent(input_text=temp_info_df.iloc[0][key],
                                           output_image_path=temp_path,handwriting_style=handwriting_style)
        else:
            for ii in range(len(input_df)):
                for key in input_field_dict:
                    temp_x, temp_y = generate_position(header_name = key,bias_x=x_bias,bias_y=y_bias)
                    temp_path = input_root + "/" + str(ii+start_id) + "_" + key + \
                                            "_" + str(temp_x) + "_" + \
                                            str(temp_y) + ".png"
                    self.generate_image_transparent(input_text=input_df.iloc[ii][key],
                                               output_image_path=temp_path,handwriting_style=handwriting_style)
            