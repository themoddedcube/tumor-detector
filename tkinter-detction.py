import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2
from PIL import Image as im

my_w = tk.Tk()
my_w.geometry("155x30")
my_w.title('tumor scanner')
my_font1=('times', 18, 'bold')
b1 = tk.Button(my_w, text='Upload File', width=20,command = lambda:upload_file())
b1.grid(row=2,column=1) 

def format_image(filename):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    x,y,w,h = cv2.boundingRect(thresh)
    ROI = image[y:y+h, x:x+w]

    hsv = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 152])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    x, y, w, h = 0, 0, ROI.shape[1]//2, ROI.shape[0]
    left = mask[y:y+h, x:x+w]
    right = mask[y:y+h, x+w:x+w+w]

    left_pixels = cv2.countNonZero(left)
    right_pixels = cv2.countNonZero(right)
    leftzz = round(((left_pixels)/(left_pixels + right_pixels)) * 100, 2)
    rightzz = round(((right_pixels)/(left_pixels + right_pixels)) * 100, 2)

    if left_pixels > right_pixels:
        cv2.putText(image,'On Left', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
        cv2.putText(image, str(leftzz) + '%', (7, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
        
    if right_pixels > left_pixels:
        cv2.putText(image,'On Right', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
        cv2.putText(image, str(rightzz) + '%', (7, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
    
    if int(leftzz) >= 100.00 or int(rightzz) >= 100.00:
        cv2.putText(image,'No Tumor detected', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)


    image = cv2.resize(image, (540, 540))
    return image



def upload_file():
    filename = filedialog.askopenfilename()

    filenameList = filename.rsplit('/', 2) 
    tempName = f'{filenameList[-2]}/{filenameList[-1]}'
    img = im.fromarray(format_image(tempName)) 
    img.show()

my_w.mainloop()