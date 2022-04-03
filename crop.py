import os
import argparse
import cv2 as cv
import numpy as np
import pandas as pd

def get_argparser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--root_dir', type=str, 
                        default=r'C:\Users\singku\google drive ku 175T\_G-Project',
                        help='Current working directoy')
    parser.add_argument("--datasets", type=str, default='CPN_all',
                        help='Datasets version/type which we want to trim')
    
    return parser


def cutImage(image, rect):
    
    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[0] + rect[2]
    y2 = rect[1] + rect[3]
    
    return image[y1:y2, x1:x2]


if __name__ == "__main__":
    
    opts = get_argparser().parse_args()
    
    root_dir = os.path.join(opts.root_dir)
    img_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Images')
    mask_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Masks_result')
    
    dst_img = os.path.join(root_dir, 'datasets', opts.datasets, 'Images_crop')
    dst_mask = os.path.join(root_dir, 'datasets', opts.datasets, 'Masks_crop')
    dst_ol = os.path.join(root_dir, 'datasets', opts.datasets, 'Overlap')
    
    f_list = os.listdir(img_dir)
    idx = 0
    for f_name in f_list:
        
        imd = os.path.join(img_dir, f_name)
        mad = os.path.join(mask_dir, f_name.split('.')[-2] + '_mask.' + f_name.split('.')[-1])
        
        imdst = os.path.join(dst_img, f_name)
        madst = os.path.join(dst_mask, f_name.split('.')[-2] + '_mask.' + f_name.split('.')[-1])
        oldst = os.path.join(dst_ol, f_name)
        
        if not os.path.exists(imd) or not os.path.exists(mad):
            raise RuntimeError('File Not exists: \n {}\n {}'.format(imd, mad))
        
        if os.path.exists(imdst):
            continue
        
        df = os.path.join(root_dir, 'datasets', opts.datasets, 'CPN_utf8.csv')
        col = ['ID', 'width', 'height', 'roi']
        if not os.path.exists(df):
            ROI = pd.DataFrame(columns=col)
        else:
            ROI = pd.read_csv(df, encoding='utf-8', index_col=0)
        
        img = cv.imread(imd, cv.IMREAD_GRAYSCALE)
        mask = cv.imread(mad, cv.IMREAD_GRAYSCALE)
        idx += 1
        winname = '{}, {}/{}'.format(f_name, idx, len(f_list))
        
        cv.namedWindow(winname=winname)
        cv.moveWindow(winname, 40,30)
        
        roi = cv.selectROI(windowName=winname, img=img)
        
        if roi[2] == 0 or roi[3] == 0:
            cv.destroyAllWindows()
            continue
        
        x1, y1, x2, y2 = roi[0], roi[1], roi[0]+roi[2], roi[1]+roi[3]
        pro_roi = (mask > 0).sum() / (mask.size)
        new_row = {'ID' : f_name.split('.')[0],
                   'width' : x2,
                   'heigth' : y2,
                   'roi' : np.round(pro_roi, 6)}            
        ROI = ROI.append(new_row, ignore_index=True)
        ROI.to_csv(df, encoding='utf-8')
        img = cutImage(img, roi)
        mask = cutImage(mask, roi)
        ol = cv.addWeighted(img, 1, 255-mask, 0.2, 0)

        cv.imwrite(imdst, img)
        cv.imwrite(madst, mask)
        cv.imwrite(oldst, ol)
        
        cv.destroyAllWindows()
        
        