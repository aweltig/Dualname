"""
 * TextTango: dual letter illusion
 * License: Creative Commons - Non Commercial - Share Alike License 4.0 (CC BY-NC-SA 4.0)
 * Copyright: Luca Monari 2023
 * URL: https://www.printables.com/it/model/520333-texttango-dual-letter-illusion
 """
import cadquery as cq
from math import pi, sin, cos

text1='STOP' # first text
text2='WORK' # second text
fontname = 'Arial' # select the font name
fontPath = '' # Optional: path to the .ttf file for a custom font
fontsize = 20 # size of the letter
space_percentage = 0.3 # percentage of fontzise to use as space between letters
b_h = 2 # base height
b_fil_per = 0.8 # base fillet percentage of the smallest side
b_pad = 2 # base padding for the letters border
export_name = 'TextTango' # nome of the exporting file

###################################

extr = fontsize*2 # extrude letter
space = fontsize*space_percentage # spece between letter
res = cq.Assembly() # start assembly

def letter(let, angle):
    """Extrude a letter, center it and rotate of the input angle"""
    wp = (cq.Workplane('XZ')
         .text(let, fontsize, extr,fontPath=fontPath, font=fontname, valign='bottom')
         )
    b_box = wp.combine().objects[0].BoundingBox()
    x_shift = -(b_box.xlen/2 + b_box.xmin )
    y_shift = b_box.ylen/2 
    wp = (wp.translate([x_shift,extr/2,0])
         .rotate((0,0,0),(0,0,1),angle)
         )
    return wp
    
last_ymax = 0
for ind, ab in enumerate(zip(text1, text2)):
    try:
        """Intersect the two letter and translate it to last y position + space"""
        a = letter(ab[0], 45)
        b = letter(ab[1], 135)
        a_inter_b = a & b
        b_box = a_inter_b.objects[0].BoundingBox()
        a_inter_b = a_inter_b.translate([0,-b_box.ymin,0])
        if ind:
            a_inter_b = a_inter_b.translate([0,last_ymax + space,0])
        last_ymax = a_inter_b.objects[0].BoundingBox().ymax
        res.add( a_inter_b) # add the intersection to the assebmly
    except: 
        """Bounding box is void, add a space"""
        last_ymax += space*1.5

b_box = res.toCompound().BoundingBox() # calculate the bounding box
# add the base to the assembly
res.add(cq.Workplane()
        .box(b_box.xlen+b_pad*2, b_box.ylen+b_pad*2, b_h, centered=(1,0,0))
        .translate([0, -b_pad, -b_h])
        .edges('|Z')
        .fillet(b_box.xlen/2*b_fil_per)
        )
# convert the assemly toa shape and center it
res = res.toCompound()
res = res.translate([0, -b_box.ylen/2,0])
# export the files
cq.exporters.export(res, f"{export_name}.step")
cq.exporters.export(res, f"{export_name}.stl")
show_object(res)


