
# Takes an image and finds two horisontal lines. 
# returns the endpoints of the lines and displays lines on top of image
# Version 2 adds selection of lines depending on whitespace above/below line - in order to only select block edges
import cv2
import numpy as np

def cropping_points2(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)             # Gray image needed for edge detection
    edges = cv2.Canny(gray,20,70,apertureSize = 3)
    
    lines = cv2.HoughLines(edges,2,np.pi/180,80, 50, 10, min_theta = 1.4, max_theta = 1.75)    # analyse image to find lines - thetha setting looks for horizontal
    x, y, z = img.shape               # get size of image, for line and point selection below
    print('X: ', x, 'y: ', y)
    select_lines = lines[:, 0]                                          # undo wierd array form
    top_lines = select_lines[(select_lines[:,0]<x*0.33) & (select_lines[:,0]>0)]                   # select lines close to top of image
    top_lines = top_lines[0:3]              #chose only the top 3 lines - for efficiency and avoiding very high angle lines
   
    
    
    
    bottom_lines = select_lines[select_lines[:,0]>x*0.66]                # select lines close to bottom of image
    bottom_lines = bottom_lines[0:3]


    # Selection of only block edges by seeing if a whitspace is on the wrong side of the image
    block_top_lines = []
    block_bottom_lines = []
    for rho,theta, in top_lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        x3 = int(x0 + 50*(b))
        y3 = int(y0 + 50*(a))+2
        x4 = x3+10
        y4 = y3+10

        rect = img[y3:y4,x3:x4]
        #rect2 = img[y3-5:y4-5,x3:x4]        # 2 cases of white area below line, narrow gap or line not by edge of aperture
        print (rect.mean(), rect.max())
        if rect.max() < 254:        #and rect2.mean() < 230:                    # control if there is a white area below line - to avoid including slit
            block_top_lines.append([rho, theta])
        #     cv2.line(img,(x1,y1),(x2,y2),(0,70,255),2)
        # cv2.rectangle(img, (x3, y3), (x4, y4), (255,255,56), 1) 
        
        # cv2.imshow('Top  of block',img)                       # Show lines
        # cv2.waitKey(0)
    for rho,theta, in bottom_lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        x3 = int(x0 + 50*(b))
        y3 = int(y0 + 50*(a))-2
        x4 = x3+10
        y4 = y3-10



        rect = img[y4:y3,x3:x4]

        print('x4: ', x4,' x3: ',x3,' y4: ', y4,' y3: ', y3)
        #rect2 = img[y3-5:y4-5,x3:x4]
        #print ('mena', rect.mean(), rect.max())
        if rect.max() < 254:             # and rect2.mean() < 230: 
            block_bottom_lines.append([rho, theta])
        #     cv2.line(img,(x1,y1),(x2,y2),(0,60,255),2)
        # cv2.line(img,(x1,y1),(x2,y2),(255,60,255),2)
        # cv2.rectangle(img, (x3, y3), (x4, y4), (255,255,56), 1)
        
        # cv2.imshow('Bottom of block',img)                       # Show lines
        # cv2.waitKey(0)

    best_lines = np.zeros((2,2))
    
    if not np.any(block_top_lines):   # checks if top_lines is empty
        print('no top lines')
        return
    else:    
        
        best_lines[0] = block_top_lines[0]  # take the highest available top_line and put in best lines
    if not np.any(block_bottom_lines):
        print('no bottom lines')
        return
    else:
        best_lines[1] = block_bottom_lines[0]

    # print('lines \n', lines)
  
    #print('top lines \n', top_lines)
    #print('bottom lines \n', bottom_lines)
    print('best lines \n', best_lines)
   

    for rho,theta, in best_lines:                         # Each line described by polar coordinates
        a = np.cos(theta)                                   # Draw lines on image after converting to cartesian
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))                            # define some points outside of the image
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imshow('Top and bottom of block',img)                       # Show lines
    # cv2.waitKey(0)
    
    print ('row x:', x )
    print ('row y:', y)
    rho1, theta1 = best_lines[0]                               # take polar coordinates of the lines and transform to edge points
    rho2, theta2 = best_lines[1]
    y1= rho1/np.sin(theta1)
    x1= 0
    y2= -(np.cos(theta1)/np.sin(theta1))*y+rho1/np.sin(theta1)
    x2= y
    y3= rho2/np.sin(theta2)
    x3= 0
    y4= -(np.cos(theta2)/np.sin(theta2))*y+rho2/np.sin(theta2)
    x4= y

    if y1<y3:                                               # Make sure that the top line in image is on the first row in array
        rect = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    else:
        rect = np.array([[x3,y3],[x4,y4],[x1,y1],[x2,y2]])

    return rect

# test = cropping_points(cv2.imread('ES201945339-03.zipImage_00_00_00_00.bmp'))
# print(test)