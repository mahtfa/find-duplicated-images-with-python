from PIL import Image
import glob
import os
import shutil
import datetime

date_today = str(datetime.datetime.now())
date_todayf = date_today.replace(":","-")
com = []
pngs = glob.glob("*.png")
square = 50
repcount = 0
f = open(f"log - {date_todayf}.txt", "a")
f1 = open(f"per_log - {date_todayf}.txt", "a")
totaltries = 0

print ("check with high accuracy? it takes 3 time more than normal (y/n)")
acc = input()

print ("grayout pics? (y/n)")
gray = input()
if gray == "y":
    gray = "L"
else:
    gray = "RGB"
def checkpixels (img1,img2):
    pix = img1.load()
    pix2 = img2.load()
    #print (image.size)  # Get the width and hight of the image for iterating over
    sim = [True,0,0,0]

    RDT = 0
    GDT = 0
    BDT = 0
    for y in range(0, 50, 5):
        for x in range(0, 50, 5):
            RGB1 = str(pix[x,y]).split(",")
            RGB2 = str(pix2[x,y]).split(",")
            if len(RGB1) > 1:
                #R
                R1 = int(RGB1[0].replace("(",""))
                R2 = int(RGB2[0].replace("(",""))
                #G
                G1 = int(RGB1[1])
                G2 = int(RGB2[1])
                #B
                B1 = int(RGB1[2].replace(")",""))
                B2 = int(RGB2[2].replace(")",""))
                #Diffrences
                RD = R2 - R1
                GD = G1 - G2
                BD = B1 - B2
                if RD >= 20 or RD <= -20:
                    RDT += 1
                if GD >= 20 or GD <= -20:
                    GDT += 1
                if BD >= 20 or BD <= -20:
                    BDT += 1
            else:
                #R
                R1 = int(RGB1[0].replace("(",""))
                R2 = int(RGB2[0].replace("(",""))
                #Diffrences
                RD = R2 - R1
                if RD >= 20 or RD <= -20:
                    RDT += 1
                    
            if RDT > 20 or GDT > 20 or BDT > 20:
                    sim[0] = False
                    break
        if RDT > 20 or GDT > 20 or BDT > 20:
                sim[0] = False
                break
    sim[1] = RDT
    sim[2] = GDT
    sim[3] = BDT
    return sim

def createsquare (loc, sq):
    left = (loc[0] - sq)/2
    top = (loc[1] - sq)/2
    right = (loc[0] + sq)/2
    bottom = (loc[1] + sq)/2
    
    locs = [left, top, right, bottom]
    return locs

for im1 in pngs:
    for im2 in pngs:
        #print(pngs)
        moved = "nothing!"
        if im1 not in com:
            com.append(im1)
        if im1  == im2 or im2 in com:
            continue
        size1 = os.stat(im1).st_size
        size2 = os.stat(im2).st_size

        png1 = Image.open(im1)
        png2 = Image.open(im2)

        im2resize = png2.resize((png1.size[0], png1.size[1]))
        
        if acc == "y":
            #center
            locs = createsquare(png1.size, square)
            
            imc1 = png1.crop((locs[0], locs[1], locs[2], locs[3]))
            imc2 = im2resize.crop((locs[0], locs[1], locs[2], locs[3]))

            imc1 = imc1.convert(gray)
            imc2 = imc2.convert(gray)

            same1 = checkpixels(imc1, imc2)
            #left
            locs = createsquare([png1.size[0]-50,png1.size[1]], square)
            
            imc1 = png1.crop((locs[0], locs[1], locs[2], locs[3]))
            imc2 = im2resize.crop((locs[0], locs[1], locs[2], locs[3]))

            imc1 = imc1.convert(gray)
            imc2 = imc2.convert(gray)


            same2 = checkpixels(imc1, imc2)
            #right
            locs = createsquare([png1.size[0]+50,png1.size[1]], square)
            
            imc1 = png1.crop((locs[0], locs[1], locs[2], locs[3]))
            imc2 = im2resize.crop((locs[0], locs[1], locs[2], locs[3]))

            imc1 = imc1.convert(gray)
            imc2 = imc2.convert(gray)

            same3 = checkpixels(imc1, imc2)
            same = same1[0]+same2[0]+same3[0]
            samed1 = (same1[0],same1[1],same1[2],same1[3])
            samed2 = (same2[0],same2[1],same2[2],same2[3])
            samed3 = (same3[0],same3[1],same3[2],same3[3])
            print(same)
        else:
            locs = createsquare(png1.size, square)
            
            imc1 = png1.crop((locs[0], locs[1], locs[2], locs[3]))
            imc2 = im2resize.crop((locs[0], locs[1], locs[2], locs[3]))

            same1 = checkpixels(imc1, imc2)
            if same1[0]:
                same = 3
            else:
                same = 0
            samed1 = (same1[0],same1[1],same1[2],same1[3])
            samed2 = "-"
            samed3 = "-"

        #center
        '''
        left = (png1.size[0] - square)/2
        top = (png1.size[1] - square)/2
        right = (png1.size[0] + square)/2
        bottom = (png1.size[1] + square)/2

        imc1 = png1.crop((left, top, right, bottom))
        imc2 = im2resize.crop((left, top, right, bottom))

        same = checkpixels(imc1, imc2)
        '''
        print(im1,"vs",im2)
        print(same)
        totaltries += 1
        print("------------------------")
        
        if same >= 2:
            repcount += 1
            if size1 >= size2:
                shutil.move(im2, "repeat/" + im2)
                pngs.remove(im2)
                moved = im2
                print(f"'{im2}' removed")
            elif size1 < size2:
                shutil.move(im1, "repeat/" + im1)
                os.rename(im2,im1)
                pngs.remove(im2)
                moved = im1
                print(f"'{im2}' removed")
                
            f.write(f"{im1} & {im2}\n{im1}:{round(size1/1024)}KB \n{im2}:{round(size2/1024)}KB \n{moved} moved\n{samed1}\n{samed2}\n{samed3}\n-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-\n")

        f1.write(f"{im1} & {im2}\n{im1}:{round(size1/1024)}KB \n{im2}:{round(size2/1024)}KB \n{moved} moved\n{samed1}\n{samed2}\n{samed3}\n-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-\n")


print("finished you can see details on log.txt file repeated images:",repcount,"total try: ",totaltries)

f.write(f"repeated images: {repcount} total try: {totaltries}")
f1.write(f"repeated images: {repcount} total try: {totaltries}")

f.close()
f1.close()
print("press enter to close program")
input()
