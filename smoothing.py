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


def on_mouse(event, x, y, flags, param):
    
    global oldx, oldy

    if event == cv.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y
    elif event == cv.EVENT_RBUTTONDOWN:
        oldx, oldy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        print('Event LB button UP: {}, {}'.format(x, y))
    elif event == cv.EVENT_RBUTTONUP:
        print('Event RB button UP: {}, {}'.format(x, y))
    elif event == cv.EVENT_MOUSEMOVE:
        if flags & cv.EVENT_FLAG_LBUTTON:
            cv.circle(img, center=(x, y), radius=12, color=0, thickness=-1)
            oldx, oldy = x, y
        elif flags & cv.EVENT_FLAG_RBUTTON:
            cv.line(img, (oldx, oldy), (x, y), (255), 8, cv.LINE_4)
            oldx, oldy = x, y
        
        
if __name__ == "__main__":
    
    opts = get_argparser().parse_args()
    
    root_dir = os.path.join(opts.root_dir)
    data_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Masks')
    
    if not os.path.exists(data_dir):
        raise RuntimeError('file not found error: {}'.format(data_dir))

    idx = 0
    f_list = os.listdir(data_dir)
    for f_name in f_list:
        file_dir = os.path.join(data_dir, f_name)
        idx += 1
        winname = '{}, {}/{}'.format(f_name, idx, len(f_list))
        dst_dir = os.path.join(root_dir, 'datasets', opts.datasets, 'Masks_result', f_name)
        
        if not os.path.exists(dst_dir):
            img = cv.imread(file_dir, cv.IMREAD_GRAYSCALE)
        else:
            continue
        
        cv.namedWindow(winname=winname)
        cv.moveWindow(winname, 40,30)
        
        drawing = False
        mode = True
        oldx, oldy = -1, -1
        
        cv.setMouseCallback(winname, on_mouse, img)

        while True:
            cv.imshow(winname, img)
            k = cv.waitKey(1)
            if k == ord('s'):
                cv.imwrite(dst_dir, img)
            elif k == 27: # ESC
                break

        cv.destroyAllWindows()
        
        
        
        
    
    