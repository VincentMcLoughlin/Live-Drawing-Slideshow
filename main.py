# Written by: Vincent McLoughlin, keep ya grubby mits to yaself

import glob
from PIL import Image, ImageTk, ExifTags
import tkinter 
from tkinter import filedialog as fd, PhotoImage
import random
import time
import os

def fix_orientation(pilImage):
    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    exif=dict(pilImage._getexif().items())

    if   exif[orientation] == 3 : 
        pilImage=pilImage.rotate(180, expand=True)
    elif exif[orientation] == 6 : 
        pilImage=pilImage.rotate(270, expand=True)
    elif exif[orientation] == 8 : 
        pilImage=pilImage.rotate(90, expand=True)
        
    return pilImage

class FileManager:

    def __init__(self, index_list, pilImages, canvas, canvas_image, w, h):

        self.file_list = pilImages
        self.image_list = list()
        self.index_list = index_list
        self.current_index = 0
        self.canvas = canvas
        self.w = w
        self.h = h
        self.canvas_image = canvas_image
        self.make_image_list()


    def make_image_list(self):

        for file in self.file_list:            
            try:                
                pilImage = Image.open(file)
                pilImage = fix_orientation(pilImage=pilImage)                
            except Exception as e:
                print("failed to open image")
                print(e)
            
            imgWidth, imgHeight = pilImage.size
            if imgWidth > self.w or imgHeight > self.h:
                ratio = min(self.w/imgWidth, self.h/imgHeight)
                imgWidth = int(imgWidth*ratio)
                imgHeight = int(imgHeight*ratio)
                pilImage = pilImage.resize((imgWidth,imgHeight), Image.Resampling.LANCZOS)
                
            image = ImageTk.PhotoImage(pilImage)
            self.image_list.append(image)

class SlideshowManager:
    def __init__(self):
        self.start_time = time.time()
        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        self.master = PhotoImage(master = self.canvas, width = self.w, height = self.h)

    def escape_pressed(self, e):
        exit()

    def right_pressed(self, e, file_manager):
        index = file_manager.current_index    
        
        if index == len(file_manager.file_list):
            print(f"index {index} Out of range")
            return

        if index < len(file_manager.file_list) -1:
            file_manager.current_index += 1
            index = file_manager.current_index

        img_index = file_manager.index_list[index]                
        
        file_manager.canvas.itemconfig(file_manager.canvas_image, image=file_manager.image_list[img_index])        

        self.start_time = time.time()

    def left_pressed(self, e, file_manager):    
                
        index = file_manager.current_index    
        if index < 0:           
            return     
        
        if index > 0:
            file_manager.current_index -= 1
            index = file_manager.current_index

        img_index = file_manager.index_list[index]    

        file_manager.canvas.itemconfig(file_manager.canvas_image, image=file_manager.image_list[img_index])            

        self.start_time = time.time()

    def show_PIL(self, pilImages):                            

        index_list = list(range(0,len(pilImages)))        
        pilImage = Image.open(pilImages[index_list[0]])
        pilImage = fix_orientation(pilImage=pilImage)        
        
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()        

        self.label = tkinter.Label(text="", font=('Helvetica', 16), fg='white', bg='black')
        self.label.pack()
        self.update_clock()
        
        canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        PhotoImage(master = canvas, width = self.w, height = self.h)
        canvas.pack()
        canvas.configure(background='black')        
        
        imgWidth, imgHeight = pilImage.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w/imgWidth, self.h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = canvas.create_image(self.w/2,self.h/2,image=image)    
        self.fil_man = FileManager(index_list, pilImages, canvas, imagesprite, self.w, self.h) 

        self.root.bind("<Escape>", self.escape_pressed)    
        self.root.bind("<Right>", lambda event, arg=self.fil_man: self.right_pressed(event, arg))
        self.root.bind("<Left>", lambda event, arg=self.fil_man: self.left_pressed(event, arg))

        self.root.mainloop()

    def update_clock(self, limit=10):
        
        now = time.time()        
        if now - self.start_time > limit:
            self.right_pressed("",self.fil_man)
            self.start_time = now
        
        elapsed = abs(now - self.start_time )

        if elapsed > limit:
            time_remaining = str(limit)
        else:
            time_remaining = str(round(limit - elapsed))

        self.label.configure(text=time_remaining)
        self.root.after(1000, self.update_clock)

    def show_image(self):
        
        filetypes = (
            ('All files', '*.*'),
            ('*.png files', '*.png'),
            ('*.jpg files', '*.jpg'),
            ('*.gif files', '*.gif')
        )

        filenames = fd.askopenfilenames(
            title='Open files',
            initialdir='/',
            filetypes=filetypes)

        new_pic_list = []
        for file in filenames:
            new_file = file.replace("/", "\\")
            new_pic_list.append(new_file)            
        
        self.show_PIL(new_pic_list)        

if __name__ == '__main__':
    mngr = SlideshowManager()
    mngr.show_image()