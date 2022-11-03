import json
import os
from pathlib import PosixPath
from typing import Dict, List

from utils.encoder_json import Encoder


def read_json(file_name: str,
              key: str):
    with open(file_name, 'r') as f:
        json_content = json.load(f)
        return json_content[key]

def rename_file_tail(file_name: str,
                     form_suffix: str = '.webp',
                     new_suffix: str = '.jpg') -> str:
    if file_name.endswith(form_suffix):
        return os.path.splitext(file_name)[0] + new_suffix
    else:
        return file_name

def rename_file_suffix(file_path: PosixPath,
                       form_suffix: str = '.webp',
                       new_suffix: str = '.jpg'):
    if isinstance(file_path, list):
        for file in file_path:
            rename(file, form_suffix, new_suffix)
    else:
        rename(file_path, form_suffix, new_suffix)


def rename(file_path, form_suffix, new_suffix):
    if file_path.name.endswith(form_suffix):
        new_name = os.path.splitext(file_path.name)[0] + new_suffix
        os.rename(os.path.join(file_path.parent, file_path.name), os.path.join(file_path.parent, new_name))


def rename_files_tail(dir_path: str) -> None:
    file_list = os.listdir(dir_path)
    for file in file_list:
        os.rename(os.path.join(dir_path, file), os.path.join(dir_path, rename_file_tail(file)))

def dir_if_exists(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        print(f'>> Create new directory {dir_path}')
        os.makedirs(dir_path)


def write_json(save_path: str, json_file: Dict):
    mkfile(save_path)

    with open(save_path, 'w') as fp:
        j = json.dumps(json_file, indent=4)
        fp.write(j)


def write_str2json(save_path: str, json_object: str):
    with open(save_path, "w") as outfile:
        outfile.write(json_object)


def write_list2json(save_path: str, json_objects: List):
    json_string = json.dumps(json_objects, cls=Encoder, sort_keys=True, indent=4, ensure_ascii=False)
    write_str2json(save_path, json_string)


def mkfile(filepath: str):
    file = os.path.exists(filepath)
    if not file:
        file = open(filepath, 'w')
        file.close()
    else:
        print("---  file exists!  ---")


if __name__ == '__main__':
    pass
    # print(read_json('../setting/config.json', 'password'))
    # rename_files_tail('../photos/album')
    # post = Post()
    # post.pk = '0000'
    # post.id = "sdsdsdddd"
    # post.title = 'ssdsdsdsd'
    # post.taken_at = 'sddsdsfsfdsf'
    # print(post.__dict__.keys())
    # post_d = pd.DataFrame([post])
    # post_d.to_csv('test.csv', header=True, index=False)
    # with open('test.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(post.__dict__)
