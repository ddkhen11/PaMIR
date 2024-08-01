import argparse
from itertools import chain
import shutil
import numpy as np
import os
import glob
import trimesh
from PIL import Image

mesh_dir = os.path.join(os.path.dirname(__file__), '../../../dataset_example/mesh_data')
extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']


def get_mesh_tex_fname(folder):
    obj_list = glob.glob(os.path.join(folder, '*.obj'))
    img_list = list(chain.from_iterable(glob.glob(os.path.join(folder, ext)) for ext in extensions))
    assert len(obj_list)==1 and len(img_list)==1, 'Ony one obj file and texture image allowed!'

    base_name = os.path.basename(img_list[0])
    name, ext = os.path.splitext(base_name)
    jpg_path = img_list[0]
    if ext != '.jpg':
        with Image.open(img_list[0]) as img:
            jpg_path = os.path.join(folder, f"{name}.jpg")
            img.convert('RGB').save(jpg_path, 'JPEG')
        os.remove(img_list[0])

    return obj_list[0], jpg_path


def process_one_data_item(data_item):
    obj_fname, tex_fname = get_mesh_tex_fname(data_item)
    mesh = trimesh.load(obj_fname)

    filename = os.path.split(data_item)[1]
    destination_path = f"{data_item}/original/{filename}.obj"
    if not os.path.isdir(f"{data_item}/original"):
        os.makedirs(f"{data_item}/original")
    shutil.copy(obj_fname, destination_path)

    mesh_v = mesh.vertices
    min_xyz = np.min(mesh_v, axis=0, keepdims=True)
    max_xyz = np.max(mesh_v, axis=0, keepdims=True)
    mesh_v = mesh_v - (min_xyz + max_xyz) * 0.5

    scale_inv = np.max(max_xyz-min_xyz)
    scale = 1.0 / scale_inv * (0.75 + np.random.rand() * 0.15)
    
    with open(f"{data_item}/scale.txt", 'w') as file:
        file.write(str(scale))

    mesh_v *= scale
    mesh.vertices = mesh_v
    trimesh.base.export_mesh(mesh, obj_fname)


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