from tkinter import Tk
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
import os
import cropping_points2 as crop
import image_transform as transform
import cv2
import numpy as np

application_window = tk.Tk()
source_path = askdirectory(title='Select source image Folder') # shows dialog box and return the path
dest_path = askdirectory(title='Select destination image Folder') # shows dialog box and return the path

filenames = os.listdir(source_path)
for filename in filenames:
    print(filename)
    if filename.endswith('0.bmp'):
        
        source_image_path = os.path.join(source_path, filename)
        img = cv2.imread(source_image_path)  #move below source_image_path to enable file location elsewhere than main
        rect = crop.cropping_points2(img)
        print(rect)
        if not np.any(rect):
                print('no save')
                os.remove(source_image_path)
                continue
        # print(rect)
        small_image = transform.image_transform(img, dest_path, rect)
        # print(small_image_path)
        # cv2.imshow('small' , small_image)
        answer = simpledialog.askstring("Input", "1: OK\n 2:Seaweed \n 3: Other issue\n 4: Faulty cropping-dont save\n 5:Quit", parent=application_window)
        if answer == '5':
                exit()
        elif answer == '4':
                continue
        # cv2.waitKey(0)
        
        small_image_name = filename[0:14]+'.'+answer+'.jpg'
        small_image_path = os.path.join(dest_path, small_image_name) 
        os.remove(source_image_path)
        print(small_image_path)
        print('source: ', source_image_path)
        cv2.imshow('small' , small_image)
        cv2.imwrite(small_image_path, small_image)
        cv2.destroyAllWindows()

