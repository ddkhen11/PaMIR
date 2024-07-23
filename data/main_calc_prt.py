import argparse
import os
import glob

import prt.prt_util as prt_util

mesh_dir = os.path.join(os.path.dirname(__file__), '../../../dataset_example/mesh_data')


def get_mesh_tex_fname(folder):
    obj_list = glob.glob(os.path.join(folder, '*.obj'))
    jpg_list = glob.glob(os.path.join(folder, '*.jpg'))
    assert len(obj_list)==1 and len(jpg_list)==1, '[ERROR] More than one obj/jpg file are found!'
    return obj_list[0], jpg_list[0]


def process_one_data_item(data_item):
    item_name = os.path.split(data_item)[1]
    obj_fname, tex_fname = get_mesh_tex_fname(data_item)
    prt_util.testPRT(obj_fname)
    print('Processed ' + item_name)


def main(mesh_folder_name):
    data_item = os.path.join(mesh_dir, mesh_folder_name)
    process_one_data_item(data_item)
    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--mesh-folder-name', dest='mesh_folder_name', 
                        required=True, type=str,
                        help='The name of the folder containing your mesh data')
    args = parser.parse_args()
    main(args.mesh_folder_name)