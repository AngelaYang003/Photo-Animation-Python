#http://www.scottlogic.co.uk/blog/colin/2009/12/rippling-reflection-effect-with-silverlight-3s-writeablebitmap/
import numpy as np
import scipy as sp
import scipy.signal
import cv2
import math


def loadPicture():

    print "This is wave effect image demo. It works for images that are 450x300 or larger"
    print "Please select a image file from your hard drive by using the file dialog being displayed"
    print "The file selection dialog window may be hidden behind the python window. Mininumize Python window to see it"
   
    try:
        #pictureOriginal = makePicture(pickAFile())

        imageOriginal = cv2.imread("scenery-2.jpg")
        #cv2.imshow('image',imageOriginal)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    except: 
        print "There is an error when opening the file you selected. Please make sure it is an image file"


    originalRows =  imageOriginal.shape[0]
    originalCols  =  imageOriginal.shape[1]
    originalChannels = imageOriginal.shape[2]

    halfRows = originalRows / 2

    print "originalRows " + str(originalRows)
    print "originalCols "  + str(originalCols)
    print "originalChannels "  + str(originalChannels)



    #allFinalImageList = []

    halfImage = shrinkImage(imageOriginal)

    #cv2.imshow('image',halfImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    print "col "  + str(originalCols)
    print "half row "  + str(halfRows)

    reflectionImage = createReflectionImage(halfImage)

    #newImage = combineReflection(imageOriginal, reflectionImage)

    newRows = originalRows + halfImage.shape[0]
    newCols = originalCols
    newChannel = originalChannels

    #the reflection portion to be made
    pictureNew = np.zeros((halfRows, originalCols, newChannel), dtype=imageOriginal.dtype)

    print "height : " + str(pictureNew.shape[0])
    print "wdith  : " + str(pictureNew.shape[1])
  

    #cv2.imshow('image',halfImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    allPictureList = []

    print 'Adding wave effect. It may take 10 ~ 15 minutes depending on the image size'
    time = 0
    count = 0
    for i in range(20):
    	count = count + 1
        print "processing in progress...." + str(i*2) + "%"

        
        pictureCombined =  np.zeros((newRows, newCols, newChannel), dtype=imageOriginal.dtype)
      

        #copy the reflection
        #cv2.imshow('image',halfImage)
        height = pictureNew.shape[0]
        #height = 149
        print "height of new image "  + str(height)
        #for y in range(149,1,-1):
        for y in range(height-1,1,-1):
            amplitude = ComputeAmplitude(y, pictureNew.shape[0]);  #between 1 - 3
            #print "amplitude " + str(amplitude)
            #print amplitude
            sinusoid = computeRipple(y, pictureNew.shape[0], time); # 2 - 0.35
            #print "sinusoid " + str(sinusoid)  
            #print sinusoid


            #the offset to the y value index caused by the ripple
            yOffset = int(sinusoid * amplitude)  #
            #print "yOffset " + str(yOffset)  # 0 - 2
            #yOffset = 0
            #print yOffset
 
            #compute the Y position of the line to copy from the source image
            sourceYLocation = halfImage.shape[0] - 1 - ((y + yOffset) * halfImage.shape[0]) / pictureNew.shape[0];
            print "sourceYLocation "  + str(sourceYLocation)
 
            #check that this value is in range
            #sourceYLocation = min(pictureNew.shape[0] - 1, max(0, sourceYLocation));
            #print "sourceYLocation "  + str(sourceYLocation)
            
 
            #copy the required row
            #sourceIndex = sourceYLocation * getWidth(pictureOld);
            sourceIndex = sourceYLocation
            #print sourceIndex
            #targetIndex = y * getWidth(pictureNew);
            #targetIndex = y
            targetIndex = sourceYLocation
            #print targetIndex

            #print "pictureNew.shape[1] " + str(pictureNew.shape[1])
            for i in range(1,pictureNew.shape[1],1):
               
                #upside down image, move vertically
                #setColor(getPixel(pictureNew, i, y), getColor(getPixel(pictureOriginalHalf, i,sourceIndex)))
                #print y, i, sourceIndex
                #pictureNew[i,y] = halfImage[i, sourceIndex]
                #print "i,y,sourceYLocation" + str(i) +  " " + str(y) + " " + str(sourceIndex)
                if (sourceIndex >= pictureNew.shape[0]):
                	  sourceIndex = sourceIndex - 1

                if ( y < pictureNew.shape[0] ) :
                    pictureNew[y,i] = halfImage[sourceIndex, i]
                
                #pictureNew[i,y] = halfImage[sourceIndex,i]
                #failed try
                #setColor(getPixel(pictureNew, i, y), getColor(getPixel(preflectionImageictureOld, y,sourceIndex)))
                

        #combine orignal picture with its wave effect reflection
        WidthofpictureCombined  =  newCols
        HeightOfpictureCombined =  newRows 
        HeightOfpictureOriginal =  originalRows
        WidthOfpictureOriginal  =  originalCols

        WidthOfpictureNew       =  WidthofpictureCombined
        HeightOfpictureNew      =  HeightOfpictureCombined
        
        HeightOfpictureCombined =  newRows 


        #cv2.imshow('image',pictureNew)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        print "height : " + str(pictureNew.shape[0])
        print "wdith  : " + str(pictureNew.shape[1])

        imageWithReflection = combineReflection(imageOriginal, pictureNew)

        cv2.imwrite("withReflection" + str(count) + ".jpg", imageWithReflection)
        
        #cv2.imshow('image',imageWithReflection)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
       
        """
        for y in range(1,HeightOfpictureCombined):
             = 
            for x in range(1,WidthofpictureCombined):
                #print y,x,y-HeightOfpictureOriginal
                if y < HeightOfpictureOriginal:
                    setColor(getPixel(pictureCombined, x, y), getColor(getPixel(pictureOriginal, x,y)))
                if y > HeightOfpictureOriginal and y < HeightOfpictureCombined-1:
                   setColor(getPixel(pictureCombined, x, y), getColor(getPixel(pictureNew, x,y-HeightOfpictureOriginal+1)))
        
        #imageReflection = Image(p,pictureNew)
        """
       

        #imageWithReflection = Image(p,pictureCombined)
        
                
        allPictureList.append(imageWithReflection)
        time = time + 0.4
        print "total images :" + str(len(allPictureList))


def shrinkImage(img):



    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    originalRows = img.shape[0]
    originaCols  = img.shape[1]
    originalChannels = img.shape[2]

    newRows = originalRows / 2
    newCols = img.shape[1] 


    print originalRows
    print originaCols
    print newRows
    print newCols

    

    #newImage = np.zeros(shape = (newRows,newCols))
    newImage = np.zeros((newRows, newCols, originalChannels), dtype=img.dtype)


    for i in range(newRows):
        for j in range(newCols):
           #print j, i, 2*j
           newImage[i,j] = img[i * 2, j]

   
    #cv2.imshow('image',newImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return newImage

def createReflectionImage(img):

    originalRows = img.shape[0]
    originaCols  = img.shape[1]
    originalChannels = img.shape[2]

    newImage = np.zeros((originalRows, originaCols, originalChannels), dtype=img.dtype)

    for i in range(originalRows):
        for j in range(originaCols):
           #print j, i, 2*j
           newImage[i,j] = img[originalRows - i - 1, j]

    #cv2.imshow('image',newImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return newImage

def combineReflection(img, reflection):

    originalRows = img.shape[0]
    originaCols  = img.shape[1]
    originalChannels = img.shape[2]

    reflectedRows = reflection.shape[0]

    newRows = originalRows + reflectedRows - 50

    print "newRows " + str(newRows)

    newImage = np.zeros((newRows, originaCols, originalChannels), dtype=img.dtype)

    for i in range(originalRows - 50):
        for j in range(originaCols):
           #print j, i, 2*j
           newImage[i,j] = img[i, j]

    #blend two images
    weight = 1.0
    for i in range(originalRows - 50, originalRows) :

    	for j in range(originaCols):
           #print j, i, 2*j
           
    		newImage[i,j] = img[i, j] * weight + ( 1 - weight ) * reflection[i - originalRows + 51, j]
    		#newImage[i,j] = img[i, j] * weight
    		
    	weight = weight - 0.02

    for i in range(originalRows, newRows):
        for j in range(originaCols):
           #print j, i, 2*j
           newImage[i,j] = reflection[i - originalRows + 50, j]

    #cv2.imshow('image',newImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    cv2.imwrite("withReflection.jpg", newImage)

    return newImage

def ComputeAmplitude(y, height):
    result = y*20.0 / float(height) + 1.0   #from 1 to 3
    return result

def computeRipple(y, height, time):


    #provide a ripple that is the combination of two out of phase sine waves
    
    phaseFactor = float(y) / height
    result = math.sin(time + phaseFactor * 16) + math.sin(time + phaseFactor * 30) + math.sin(time + phaseFactor* 62)
    #print result
    return result



loadPicture()