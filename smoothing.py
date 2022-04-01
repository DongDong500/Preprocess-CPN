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
    
    root_dir = os.paht.join(r'C:\Users\singku\google drive ku 175T\_G-Project\datasets')
    dataset = ''    
    