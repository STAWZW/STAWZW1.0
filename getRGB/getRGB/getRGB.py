# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:48:16 2019

@author: Administrator
"""

from PIL import Image
import numpy as np

def getRGB(img_path):
    try:
        im = Image.open(img_path)
    
        h1 = (im.size[0]/2)-10
        w1 = (im.size[1]/2)-10
        h2 = (im.size[0]/2)
        w2 = (im.size[1]/2)
    
        cropped = im.crop((h1, w1, h2, w2))
        #Image._show(cropped)
        pix = cropped.load()
        width = cropped.size[0]
        height = cropped.size[1]
    
        rb = []
        gb = []
        bb = []
        for x in range(width):
            for y in range(height):
                if len(pix[x, y]) == 3:
                    r, g, b = pix[x, y]
                    rb.append(r)
                    gb.append(g)
                    bb.append(b)
                else:
                    r, g, b, c = pix[x, y]
                    rb.append(r)
                    gb.append(g)
                    bb.append(b)
                
        rbb = np.mean(rb)             #mean取平均值
        gbb = np.mean(gb)
        bbb = np.mean(bb)
    
        
        I = 1-(rbb+gbb+bbb)/363
        
        if -0.05<=I<0.45:
            y = 106.55105 + 7.66077*I + 263.25535*I*I
            return y
        if 0.45<=I<=0.82:
            y = 256.2504 - 178.80774*I + 64.3805*I*I
            return y
        if I<-0.05:
            return "Not Recognized"
        if I>0.82:
            return "Intensity is low"
    except:
        return "Please select the correct picture!"
