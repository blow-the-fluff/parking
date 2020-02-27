import tensorflow as tf
import numpy as np
from network.model import HTRModel
from data import preproc as pp
from data.generator import Tokenizer
import string
import os

# global variable model
model = None

arch = "flor"
input_size = (1024, 128, 1)
max_text_length = 128
charset_base = string.printable[:95]
tokenizer = Tokenizer(charset_base, max_text_length)
model_checkpoint = '../htr_saved_model_v1/htr_saved_checkpoints_v1/checkpoint_weights.hdf5'


def load_model_from_checkpoint(arch=arch,
                               input_size=input_size,
                               tokenizer=tokenizer,
                               model_checkpoint=model_checkpoint,
                               learning_rate=0.001):
    assert os.path.exists(model_checkpoint)
    model = HTRModel(architecture=arch, input_size=input_size, vocab_size=tokenizer.vocab_size)
    model.compile(learning_rate=learning_rate)
    model.load_checkpoint(target=model_checkpoint)
    return model

def preprocess_img(img, input_size=input_size, np_array=False):
    pp_img = pp.preproc(img, input_size, np_array)
    pp_img = pp_img.reshape(*input_size)
    pp_img = pp.normalization(pp_img)
    return pp_img

def predict(img, input_size=input_size, np_array=False):
    global model
    if model is None:
        model = load_model_from_checkpoint()

    pp_imgs = preprocess_img(img, input_size, np_array)
    pp_imgs = np.asarray(pp_imgs)
    pp_imgs = pp_imgs.reshape(-1, *input_size)
    predicts, _= model.predict(x=pp_imgs,
                            steps=1,
                            ctc_decode=True,
                            verbose=1,
                            use_multiprocessing=True)
    predicts = [tokenizer.decode(x[0]) for x in predicts]
    return predicts

# test_img = '../0_BusinessName_196_331.png'
# print(predict(test_img))
# test_img = '../102000_Signature.png'
# print(predict(test_img))
