import cv2
import numpy as np

# takes in four points in a 4x2 x,y matrix and performs a transformation on the image
# after which a cropping and size reduction is mage

def image_transform(img, dest_path, array):

    #before = np.float32([[x1,y1], [x2,y2],[x3,y3],[x4,y4]])
    after = np.float32([[0,0],[640,0],[0,400],[640,400]])
    array= array.astype('float32')                  #Array comes in as float64
       
    M = cv2.getPerspectiveTransform(array,after)    # get translation matrix

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    dst = cv2.warpPerspective(gray,M,(640,400))
    #equ = cv2.equalizeHist(dst)                     #Use equ for better contrast in images in imgshow below
    cv2.imshow(dest_path, dst)
    resize =cv2.resize(dst,(30,30))

    cv2.imwrite('cropped_image.jpg',dst)        # fixa path och namn
    return resize


