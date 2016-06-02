import os
import sys
import Image
import string

###to do: #functionality to choose excerpt
        # resize image
        # divide sfactor    instance! tiles can only be resized by common factors (max=8)! add second instance to resize after merge!

####Control Arguments
#shrink factor: controls resize in form of originalimagewidth/sfactor. Enlargement will be filtered!
sfactor=2 #use only common factors for this! 2,4,8!

lens=10.0 # set lens magnification of images ALWAYS USE FLOAT!
interleaving=2.0#set pyramid level, for rawdata use 1.0 ALWAYS USE FLOAT
interleaving=interleaving*sfactor

prefix=str(sys.argv[2])
filetype='.png'

cwd=os.path.abspath('')
workpath=os.path.abspath(sys.argv[1])

files=os.listdir(workpath)

xmax=0
ymax=0
counter=0

print len(os.listdir(workpath))
for file in os.listdir(workpath):#get dimension of full extent

    file=str(file)
    if filetype in file:
        file=string.strip(file, filetype)
        dimensions=file.split('x')
        xincr=int(dimensions[2])
        yincr=int(dimensions[3])
        #print dimensions
        x=int(dimensions[0])
        y=int(dimensions[1])
        counter=counter+1


        if x>xmax:
             xmax=x
        if y>ymax:
            ymax=y
            
#define size of output tiles
numtiles_x=(xmax/sfactor)/xincr+1
numtiles_y=(ymax/sfactor)/yincr+1
print "dimensions: "+str(numtiles_x)+" by "+str(numtiles_y)+" tiles"    
outsizex=xincr*2 #size of the outputfiles in px
outsizey=yincr*2


if sfactor >1:
    xmax=xmax/sfactor
    ymax=ymax/sfactor

    print "resize is set to 1/%s " %sfactor

#calculate number of output tiles
numoutx=int((xmax/outsizex)+1)
numouty=int((ymax/outsizey)+1)
numout=numoutx*numouty
print "numoutx is: "
print numoutx 
print "numouty is: "
print numouty 
counter=1
for outy in range(numouty):
    #print str(n)
    
   # print "Imagesize is %s pixels x %s pixels" % (xmax+xincr, ymax+yincr)




    for outx in range(numoutx):
        print "create mergefile"
        mergefile=Image.new("RGB",(outsizex,outsizey), "white")
        print "mergefile created"


        for tile in os.listdir(workpath):
            if filetype in str(tile):
                tileobj=Image.open(str(workpath)+"/"+str(tile))
                dimensions=string.strip(str(tile), filetype).split('x')                       
                x=int(dimensions[0])
                y=int(dimensions[1])
                xincr=int(dimensions[2])
                yincr=int(dimensions[3])
                if sfactor >1:
                    x=int(x/sfactor)
                    y=int(y/sfactor)
                    xincr=int(xincr/sfactor)
                    yincr=int(yincr/sfactor)
                if x>=(outx*outsizex) and x<((outx+1)*outsizex):
                    if y>=(outy*outsizey) and y<((outy+1)*outsizey):
                        tileobj=Image.open(str(workpath)+"/"+str(tile))
                        tileobj=tileobj.resize((xincr,yincr), Image.ANTIALIAS)
                        mergefile.paste(tileobj, (x-(outx*outsizex),y-(outy*outsizey)))

                       
        print "saving file %s of %s" % (counter, numout)
        mergefile.save(str(prefix)+"_"+str(counter)+".tiff","TIFF",)

        
        orthofile=open(str(prefix)+"_"+str(counter)+".tfw", 'w') #create file for rectification in Arcgis.
        pixelscale=(3.45/lens)*interleaving / 1000 #unit is now millimeter
        xcord=(counter-1) % numoutx  #remainder of division
        ycord=(counter-1) // numoutx #

        orthofile.write(str(pixelscale))
        orthofile.write('\n')
        orthofile.write("0")
        orthofile.write('\n')
        orthofile.write("0")
        orthofile.write('\n')
        orthofile.write(str(pixelscale * (-1)))
        orthofile.write('\n')
        orthofile.write(str(xcord*outsizex* pixelscale))
        orthofile.write('\n')
        orthofile.write(str(ycord*outsizey*pixelscale*(-1)))
        orthofile.write('\n')
                                       
        counter=counter+1
print "done!"
