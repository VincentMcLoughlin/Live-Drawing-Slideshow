# Written by: Vincent McLoughlin, keep ya grubby mits to yaself

import glob
from PIL import Image, ImageOps, ImageTk
import tkinter 
import random

class FileManager:

    def make_image_list(self):

        for file in self.file_list:            
            pilImage = Image.open(file)
            pilImage = ImageOps.exif_transpose(pilImage)        
            imgWidth, imgHeight = pilImage.size
            if imgWidth > self.w or imgHeight > self.h:
                ratio = min(self.w/imgWidth, self.h/imgHeight)
                imgWidth = int(imgWidth*ratio)
                imgHeight = int(imgHeight*ratio)
                pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
                
            image = ImageTk.PhotoImage(pilImage)
            self.image_list.append(image)
        
    def __init__(self, pilImages, canvas, canvas_image, w, h):

        self.file_list = pilImages
        self.image_list = list()
        self.index_list = list(range(0,len(pilImages)))
        random.shuffle(self.index_list)
        print(self.index_list)
        self.current_index = 0
        self.canvas = canvas
        self.w = w
        self.h = h
        self.canvas_image = canvas_image
        self.make_image_list()

def display_image():
    pass

def escape_pressed(e):
    exit()

def right_pressed(e, file_manager):
    index = file_manager.current_index    

    if index == len(file_manager.file_list):
        print(f"index {index} Out of range")
        return

    img_index = file_manager.index_list[index]
    
    print(file_manager.index_list[index])
    print(f"Right index is {index}")
    
    file_manager.canvas.itemconfig(file_manager.canvas_image, image=file_manager.image_list[img_index])

    if index < len(file_manager.file_list) -1:
        file_manager.current_index += 1

def left_pressed(e, file_manager):    

    index = file_manager.current_index

    if index < 0:        
        return     
    
    img_index = file_manager.index_list[index]

    print(file_manager.index_list[index])
    print(f"Left index is {index}")

    file_manager.canvas.itemconfig(file_manager.canvas_image, image=file_manager.image_list[img_index])

    if index > 0:
        file_manager.current_index -= 1

def show_PIL(pilImages):    

    root = tkinter.Tk()
    #root = tkinter.Toplevel()
    pilImage = Image.open(pilImages[0])
    pilImage = ImageOps.exif_transpose(pilImage)

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()        

    canvas = tkinter.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='black')        
    
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)    
    fil_man = FileManager(pilImages, canvas, imagesprite, w, h) 

    root.bind("<Escape>", escape_pressed)    
    root.bind("<Right>", lambda event, arg=fil_man: right_pressed(event, arg))
    root.bind("<Left>", lambda event, arg=fil_man: left_pressed(event, arg))

    root.mainloop()

def show_image():
    jpg_files = glob.glob("input_pics/*.jpg")
    png_files = glob.glob("input_pics/*.png")
    pic_list = jpg_files + png_files        
    
    show_PIL(pic_list)

if __name__ == '__main__':
    show_image()