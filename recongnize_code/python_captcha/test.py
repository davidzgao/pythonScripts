#-*- coding:utf8 -*-
from PIL import Image
import pytesseract
#import subprocess



im = Image.open("captcha.gif")
vcode = pytesseract.image_to_string(im)

print (vcode)

