#-*- coding:utf-8 -*-
from PIL import Image
import hashlib
import time
import math
import os
import pytesseract

class VectorCompare(object):
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)
 
    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word , count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))




class LetterRec(object):
    def train_imgdata(self):
        self.iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.imageset = []
        for letter in self.iconset:
            for fname in os.listdir('python_captcha/iconset/%s'%letter):
                tmp = []
                if fname != "Thumbs.db" and fname != ".DS_Store":
                    tmp.append(self.buildvector(Image.open("python_captcha/iconset/%s/%s"%(letter,fname))))
                self.imageset.append({letter:tmp})
        return self.imageset

    def buildvector(self, im):
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1

    def find_letters_cut(self, image):
        inletter = False
        foundletter = False
        start = 0
        end = 0
        letters = []
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pix = image.getpixel((x,y))
                if pix != 255:
                    inletter = True
                    break
            if foundletter == False and inletter == True:
                foundletter = True
                start = x
            if foundletter == True and inletter == False:
                foundletter = False
                end = x
                letters.append((start,end))
            inletter = False
        return letters

    def img_blackwhite_deal(self,im):
        im2 = Image.new("P",im.size,255)  #deal im as  black-white pic
        for x in range(im.size[1]):
            for y in range(im.size[0]):
                pix = im.getpixel((y,x))
                if pix == 220 or pix == 227: # these are the numbers to get
                    im2.putpixel((y,x),0)
        return im2
         
    def rec_one_pic(self,im):
        rec_result = []
        v = VectorCompare()
        im2 = self.img_blackwhite_deal(im)
        letters = self.find_letters_cut(im2)
        for letter in letters:
        #    m = hashlib.md5()
            guess = []
            im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))  #generate single letter
            for image in self.imageset:
                for key_letter, valuelist_image in image.iteritems():
                    if len(valuelist_image ) != 0:
                        for value_image in valuelist_image:
                            guess.append((v.relation(value_image, self.buildvector(im3)), key_letter))
            #print guess
            guess.sort(reverse = True)
            #print guess[0:3]
            rec_result.append(guess[0][1])
        return rec_result

    def rec_pics(self, pics_path):
        #import pdb
        #pdb.set_trace()
        pics = []
        for fname in os.listdir(pics_path):
            if fname.endswith(".gif"):
                img = Image.open(os.path.join(pics_path,fname))
                pics.append((img,fname.split(".")[0]))
        print len(pics)
        right = 0
        wrong = 0
        for pic_tuple in pics:
            pic = pic_tuple[0]
            name = pic_tuple[1]
            rec_result = self.rec_one_pic(pic)
            rec_name = "".join(rec_result)
            if rec_name == name:
                right += 1
                print rec_name, name
            else:
                wrong += 1
        print right, wrong

    def rec_pics_with_pytesser(self, pics_path):
        pics = []
        for fname in os.listdir(pics_path):
            if fname.endswith(".gif"):
                img = Image.open(os.path.join(pics_path,fname))
                pics.append((img,fname.split(".")[0]))
        right = 0
        wrong = 0
        for pic_tuple in pics:
            pic = pic_tuple[0]
            name = pic_tuple[1]
            rec_name = pytesseract.image_to_string(pic).lower().strip(",.`’' ‘:")
            if rec_name == name:
                print rec_name, name
                right += 1
            else:
                wrong += 1
        print right, wrong
             
        



if __name__ == "__main__":

    im = Image.open("python_captcha/captcha.gif")
    #his = im.histogram()
    letter_rec = LetterRec()
    letter_rec.train_imgdata()
    #letter_rec.rec_one_pic(im)
    letter_rec.rec_pics("python_captcha/examples")
    letter_rec.rec_pics_with_pytesser("python_captcha/examples")


#values = dict(zip([i for i in range(256)], his))
#print values
#for j,k in sorted(values.items(), key = lambda x:x[1], reverse = True)[:10]: 
#    print j,k
