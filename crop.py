import os
import argparse
import cv2 as cv
import numpy as np

def get_argparser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--root_dir', type=str, 
                        default=r'C:\Users\singku\google drive ku 175T\_G-Project',
                        help='Current working directoy')
    parser.add_argument("--datasets", type=str, default='CPN_all',
                        help='Datasets version/type which we want to trim')
    
    return parser


if __name__ == "__main__":
    
    opts = get_argparser().parse_args()
    
    root_dir = os.path.join(opts.root_dir)
    img_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Images')
    mask_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Mask_result')
    
    dst_img = os.path.join(root_dir, 'datasets', opts.datasets, 'Images_crop')
    dst_mask = os.path.join(root_dir, 'datasets', opts.datasets, 'Mask_crop')
    dst_ol = os.path.join(root_dir, 'datasets', opts.datasets, 'Overlap')
    
    