'''
Created on 18 sept. 2014

@author: gtheurillat
'''

import PIL
from PIL import Image
## Static imports from PIL for py2exe
from PIL import GifImagePlugin
from PIL import JpegImagePlugin

class ImageUtil(object):
    ""
    
    def __init(self):
        ""
        
    def resize(self, input, output, basewidth):
        ""
        img = Image.open(input)
        
        width = float(img.size[0])
        height = float(img.size[1])
        
        if float(width > basewidth):
            
            wpercent = (basewidth/width)
            hsize = int((height*float(wpercent)))
            
            img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        
            img.save(output)