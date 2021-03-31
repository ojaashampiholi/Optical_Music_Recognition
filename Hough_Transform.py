import numpy as np
from PIL import Image
from PIL import ImageFilter
import random
from PIL import ImageDraw, ImageFont
from Template_Matching import templateMatching
nTM = templateMatching()

class houghTransform():

    def __init__(self):
        self.randomCount = 0

    def hough(self, image):
        space = 0
        image = np.where(image<128,0,1)
        x, y = image.shape
        votesDict = {}
        for i in range(x):
            votesDict[i] = 0
            for j in range(y):
                if image[i][j]==0:
                    votesDict[i] +=1
        l = [key for key,value in votesDict.items() if value > int(0.5*y)]
        
        # Calculating the Space between the lines.
        for i in range(0,len(l)-1):
            if l[i]+1 != l[i+1]:
                if space == 0:
                    space = l[i+1]-l[i]
                elif space == l[i+1]-l[i]:
                    break
        # Finding the row coordinates for the first lines
        firstLines = [l[0]]
        currentLine = l[0]
        for i in range(1,len(l)):
            if l[i] - currentLine > space*2:
                firstLines.append(l[i])
            currentLine = l[i]
        
        return space, firstLines

    def drawLines(self, image, space, firstLines):
        outArr = []
        for i in firstLines:
            for j in range(5):
                outArr.append(i + j*space)
        # print(outArr)
        copyImage = np.zeros_like(image)
        # print(copyImage.shape)
        for elem in outArr:
            copyImage[elem,:] = 255
        return outArr, copyImage

    def resizeTemplate(self, template, space):
        factor = space/template.height
        temp = template.resize((int(template.width * factor), int(template.height * factor)))
        return temp

    def getPitchDictionary(self, lines,dist):
        p = {}
        j = 1
        for i in lines:
            if j%2 ==0:
                p[int(i-dist*1.5)] = 'D'
                p[int(i-dist)] = 'C'
                p[int(i-dist*0.5)] = 'B'
                p[i] = 'A'
                p[int(i+dist*0.5)] = 'G'
                p[int(i+dist)] = 'F'
                p[int(i+dist*1.5)] = 'E'
                p[int(i+dist*2)] = 'D'
                p[int(i+dist*2.5)] = 'C'
                p[int(i+dist*3)] = 'B'
                p[int(i+dist*3.5)] = 'G'
                p[int(i+dist*4)] = 'F'
                p[int(i+dist*4.5)] = 'E'
            else:
                p[int(i-dist*0.5)] = 'G'
                p[i] = 'F'
                p[int(i+dist*0.5)] = 'E'
                p[int(i+dist)] = 'D'
                p[int(i+dist*1.5)] = 'C'
                p[int(i+dist*2)] = 'B'
                p[int(i+dist*2.5)] = 'A'
                p[int(i+dist*3)] = 'G'
                p[int(i+dist*3.5)] = 'F'
                p[int(i+dist*4)] = 'E'
                p[int(i+dist*4.5)] = 'D'
                p[int(i+dist*5)] = 'B'
            j += 1
        return p

    def omrApplication(self, image, template, matchingType, textArray, symbol_type, p, dist, limitingFactor = 0.9):
        imgH, imgW = image.shape
        tempH, tempW = template.shape
    #     outImage = Image.fromarray(np.uint8(image)).convert("RGB")
        copy_image = image.copy()
        padding = 2
        if matchingType=='naive':
            maxScore = tempH * tempW
            matchesForTemplate1 = nTM.naiveTemplateMatching(image, template, confidenceInterval = limitingFactor)
        elif matchingType=='edge':
            templateEdge, _, _ = nTM.getEdges(template)
            maxScore = np.sum(templateEdge)
            matchesForTemplate1 = nTM.edgeDetectionTemplateMatching(image, template, thresholdFactor=limitingFactor)
        else:
            print("Enter Valid Template Matching Type")
            return copy_image, textArray
        
        print("Matches for Template", len(matchesForTemplate1))
        if matchesForTemplate1==[]:
            return copy_image, textArray
        for score, start_x, start_y, end_x, end_y in matchesForTemplate1:
            if end_x >= copy_image.shape[0]-3 or end_y >= copy_image.shape[1]-3:
                continue
            copy_image[start_x-padding:end_x+(padding*2),start_y-padding] = 5
            copy_image[start_x-padding:end_x+(padding*2),end_y+padding] = 5
            copy_image[start_x-padding,start_y-padding:end_y+(padding*2)] = 5
            copy_image[end_x+padding,start_y-padding:end_y+(padding*2)] = 5
            pitch = '_'
            
            if symbol_type == 'filled_note':
                for q in range(int(dist/2)):
                    if q+start_x in p:
                        pitch = p[q+start_x]
                    elif start_x-q in p:
                        pitch = p[start_x-q]
                copy_image = Image.fromarray(np.uint8(copy_image))
                draw = ImageDraw.Draw(copy_image)
                font = ImageFont.truetype('C:/Users/ojaash/Desktop/images_and_sample-code/fonts/Lato-BoldItalic.ttf', 15) 
                draw.text((start_y-12, start_x-12),pitch,(1),font=font)
                copy_image = np.array(copy_image)
            textArray.append([start_x, start_y, end_x, end_y, symbol_type, pitch, float(np.round(((score/maxScore)*100), 2))])
            
        return copy_image, textArray

