# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:15:05 2019

@author: Zcy
"""

import tkinter as tk
from tkinter import filedialog,ttk
from PIL import Image, ImageTk
import os
import getRGB 
class MainWindow(): 
    def __init__(self):  
      
        self.frame = tk.Tk() 
        self.frame.title('Strength Detection Of PHT')
        self.frame.geometry('800x600')
        self.hello_label = tk.Label(self.frame, text='Strength Detection Of PHT',justify = 'center', font = ('黑体',12), bg='#00c1de', width=120, height=2)
        self.hello_label.grid(row = 0,column = 1,columnspan=6)
        
        self.label_name = tk.Label(self.frame,text = "Picture path:",height = "2",width = 30) 
        self.label_file = tk.Label(self.frame,text = "Target image:",height = "2",width = 30)

        self.number = tk.StringVar()
        self.numberChosen = ttk.Combobox(self.frame, textvariable=self.number,height = "2",width = 48)
       
        self.text_name = tk.Text(self.frame,height = "1",width = 50)  
        self.text_name.focus()
        
        self.label_name.grid(row = 1,column = 1)
        self.label_file.grid(row = 2,column = 1)
        self.text_name.grid(row = 1,column = 2,columnspan=4)
        self.numberChosen.grid(row = 2,column = 2,columnspan=4)

        self.button_ok = tk.Button(self.frame,text = "Select image path",width = 15,command=self.select_Path) 
        self.button_select = tk.Button(self.frame,text = "Read target image",width = 15,command =lambda:self.find_file(path1=file_for_path))
        self.button_judge = tk.Button(self.frame,text = "Calculation",width = 10,command = lambda:self.getXml(file_name_=self.file_for_path+self.numberChosen.get()))
        self.button_cancel = tk.Button(self.frame,text = "Close",width = 10,command=self.destroy)  

        self.button_ok.grid(row = 4,column = 1)  
        self.button_select.grid(row = 4,column = 2)
        self.button_judge.grid(row = 4,column = 3)
        self.button_cancel.grid(row = 4,column = 4)  
        
        self.run_label = tk.Label(self.frame, text='Calculation result display',justify = 'center',font = ('黑体',12), bg='#00c2de', width=120, height=2)
        self.run_label.grid(row = 6,column = 1,columnspan=6, pady=8)
              
        self.w_box = 800  
        self.h_box = 300
        
        self.label_img = tk.Label(self.frame)    
        self.label_img.grid(row = 7,column = 0,columnspan=6,rowspan=6)
        
        self.showImg(r'timg.jpg')
        self.frame.mainloop()
        
    def img_resize(self,w_box,h_box,pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size #获取图像的原始大小   
        f1 = 1.0*w_box/w 
        f2 = 1.0*h_box/h    
        factor = min([f1, f2])   
        width = int(w*factor)    
        height = int(h*factor)    
        return pil_image.resize((width, height), Image.ANTIALIAS)  
    
    def select_Path(self):
        global file_for_path
        path = tk.StringVar()
        file_path=filedialog.askdirectory()
        path.set(file_path)
        file_for_path=file_path+"/"
        self.text_name.insert(tk.INSERT,file_path)
        self.file_for_path=file_for_path
        
    def find_file(self,path1):
        global Files
        f = []
        for root, dirs, files in os.walk(path1):
            for file in files:
                if os.path.splitext(file)[1] == '.png' or os.path.splitext(file)[1] == '.tif' or os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.bmp':
                    t = os.path.splitext(file)
                    s = str(t[0])+str(t[1])
                    f.append(s)  # 将所有的文件名添加到F列表中
        Files = f
        self.numberChosen['values'] = Files  # 设置下拉列表的值
        self.numberChosen.current(0)

    def destroy(self):
        self.frame.quit()
        self.frame.destroy()
        
    def showImg(self,file_name):
        pil_image = Image.open(file_name)
        pil_image_resized =self.img_resize(self.w_box,self.h_box,pil_image)
        self.tk_image = ImageTk.PhotoImage(image=pil_image_resized)
        self.label_img.configure(image=self.tk_image)
        self.frame.update()
        
    def showImgr(self,file_name):
        pil_image = Image.open(file_name)
        pil_image_resized =self.img_resize(self.w_box,self.h_box,pil_image)
        self.tk_imager = ImageTk.PhotoImage(image=pil_image_resized)
        self.label_imgr.configure(image=self.tk_imager)
        self.frame.update()
        
    def getXml(self,file_name_):
        self.showImg(file_name_)
        y=getRGB.getRGB(file_name_)
        if (isinstance(y,float)):
            res= 'Mechanical strength:' + str(y) + ' MPa'
            self.result_label = tk.Label(self.frame, text=res,justify = 'left',font = ('黑体',14), bg='green', width=40, height=3)
            self.result_label.grid(row = 22,column = 1,columnspan=5, pady=8)
        else:
            self.result_label = tk.Label(self.frame, text=str(y),justify = 'left',font = ('黑体',14), bg='red', width=40, height=3)
            self.result_label.grid(row = 22,column = 1,columnspan=5, pady=8)
            
        self.frame.mainloop()

frame = MainWindow() 
      
        
        
        
        
    