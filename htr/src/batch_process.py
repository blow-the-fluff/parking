import os
import pandas as pd
import predict

def read_folder(folder, filetype='png'):
    files = os.listdir(folder)
    files = list(filter(lambda f: '.{}'.format(filetype) in f, files))
    return files


def split_filename(f, sep='_'):
    s_f = f.split(sep)
    return s_f

def split_the_files(files):
    # split_files is a list of list / nested list
    split_files = list(map(split_filename, files))
    return split_files

def get_form_ids(split_files):
    form_ids = [s_f[0] for s_f in split_files]
    form_ids = list(set(form_ids))
    return form_ids

def process_form(f_id, f_id_split_files, source_folder):
    data = {}
    for s_f in f_id_split_files:
        field_name = s_f[1].split('.')[0]
        filename = '_'.join(s_f)
        filename = os.path.join(source_folder, filename)
        data[field_name] = predict.predict(filename)
    return data

def process_write_data(source_folder):
    files = read_folder(source_folder)
    split_files = split_the_files(files)
    form_ids = get_form_ids(split_files)
    f_id = form_ids[0]
    f_id_split_files = list(filter(lambda s_f: s_f[0]==f_id, split_files))
    transcriptions = process_form(f_id, f_id_split_files, source_folder)
    transcriptions_df = pd.DataFrame.from_dict(transcriptions)
    out_csv_filename = '{}.csv'.format(f_id)
    out_csv_filename = os.path.join(source_folder, out_csv_filename)
    transcriptions_df.to_csv(out_csv_filename, index=False)

if __name__ == '__main__':
    source_folder = '/home/jupyter/hw-text/data_23f_test_outfield_text'
    output_csv_folder = '/home/jupyter/temp/'
    files = read_folder(source_folder)
    split_files = split_files(files)
    form_ids = get_form_ids(split_files)
#     transcriptions = {}
    for i, f_id in enumerate(form_ids):
        if i > 50:
            break
        f_id_split_files = list(filter(lambda s_f: s_f[0]==f_id, split_files))
        transcriptions = process_form(f_id, f_id_split_files, source_folder)
        transcriptions_df = pd.DataFrame.from_dict(transcriptions)
        out_csv_filename = '{}.csv'.format(f_id)
        out_csv_filename = os.path.join(output_csv_folder, out_csv_filename)
        transcriptions_df.to_csv(out_csv_filename, index=False)