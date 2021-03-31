import numpy as np
from Kernel_Operations import kernelOperations

ko = kernelOperations()

class templateMatching():

    def __init__(self):
        self.randomInit = 0

    def nonMaximalSupression(self, scoreArr, threshold = 0.5):
    # The function is based on Intersection over union formula and slightly 
    # based on the source code found at the following link -
    # https://github.com/amusi/Non-Maximum-Suppression/blob/master/nms.py

        if scoreArr==[]:
            return []
        scoreArr = np.array(scoreArr)
        scores = scoreArr[:, 0]
        start_x = scoreArr[:, 1]
        start_y = scoreArr[:, 2]
        end_x = scoreArr[:, 3]
        end_y = scoreArr[:, 4]
        picked_boxes = []
        areas = (end_x - start_x + 1) * (end_y - start_y + 1)
        order = np.argsort(scores)
        while order.size > 0:
            index = order[-1]
            picked_boxes.append(scoreArr[index])
            x1 = np.maximum(start_x[index], start_x[order[:-1]])
            x2 = np.minimum(end_x[index], end_x[order[:-1]])
            y1 = np.maximum(start_y[index], start_y[order[:-1]])
            y2 = np.minimum(end_y[index], end_y[order[:-1]])
            w = np.maximum(0.0, x2 - x1 + 1)
            h = np.maximum(0.0, y2 - y1 + 1)
            intersection = w * h
            ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)
            left = np.where(ratio < threshold)
            order = order[left]
        return picked_boxes

    def naiveTemplateMatching(self, image, template1, confidenceInterval = 0.90):
        image = np.where(image>128,1,0)
        template1 = np.where(template1>128,1,0)
        h, w = image.shape
        tempH, tempW = template1.shape
        scoreArr = []
        threshold = int(confidenceInterval*tempH*tempW)
        for i in range(h-tempH):
            for j in range(w - tempW):
                subImage = image[i:i+tempH, j:j+tempW]
                score = np.sum((subImage * template1) + (1-subImage) * (1- template1))
                # temp = np.round((score/(tempH*tempW)),1)
                if score>=threshold:
                    scoreArr.append([int(score), i, j, i+tempH, j+tempW])
        scoreArr1 = self.nonMaximalSupression(scoreArr)
        # print(scoreArr[-2:])
        return scoreArr1

    def getEdges(self, im, threshold = 128):
        hx, hy = ko.seperableSobelY()
        imageEdgey = ko.seperableKernel(im, hx, hy)

        hx, hy = ko.seperableSobelX()
        imageEdgex = ko.seperableKernel(im, hx, hy)

        imageEdge = np.sqrt(imageEdgex**2 + imageEdgey**2)
        imageEdge = np.where(imageEdge>threshold, 255, 0)
        
        return imageEdge, imageEdgex, imageEdgey

    #  Reference for the functions scanRange and distanceTransform 
    # is http://www.logarithmic.net/pfh/blog/01185880752
    def scanRange(self, f):
        for i, fi in enumerate(f):
            if fi == np.inf: continue
            for j in range(1,i+1):
                x = fi+j*j
                if f[i-j] < x: break
                f[i-j] = x

    def distanceTransform(self, inputArray):
        f = np.where(inputArray, 0.0, np.inf)
        for i in range(f.shape[0]):
            self.scanRange(f[i,:])
            self.scanRange(f[i,::-1])
        for i in range(f.shape[1]):
            self.scanRange(f[:,i])
            self.scanRange(f[::-1,i])
        # np.sqrt(f,f)
        return f


    def edgeDetectionTemplateMatching(self, image, template1, thresholdFactor = 0.25):
        imageEdge, imageEdgex, imageEdgey = self.getEdges(image)
        templateEdge1, templateEdgex1, templateEdgey1 = self.getEdges(template1)
        D_imageEdge = self.distanceTransform(imageEdge)
        h, w = D_imageEdge.shape
        h1, w1 = templateEdge1.shape
        outArr, threshold = [], int(np.sum(templateEdge1)*thresholdFactor)
        for i in range(0, h - h1 + 1):
            for j in range(0, w - w1):
                temp = D_imageEdge[i:i+h1,j:j+w1] * templateEdge1
                score = np.sum(temp)
                if score <= threshold:
                    outArr.append([int(score), i, j, i+h1, j+w1])
        scoreArr1 = self.nonMaximalSupression(outArr)
        return scoreArr1

    def drawBoundingBox(self, image, matchesForTemplate1):
        copy_image = image.copy()
        padding = 2
        if matchesForTemplate1==[]:
            return copy_image
        for score, start_x, start_y, end_x, end_y in matchesForTemplate1:
            if end_x >= copy_image.shape[0]-3 or end_y >= copy_image.shape[1]-3:
                continue
            copy_image[start_x-padding:end_x+(padding*2),start_y-padding] = 5
            copy_image[start_x-padding:end_x+(padding*2),end_y+padding] = 5
            copy_image[start_x-padding,start_y-padding:end_y+(padding*2)] = 5
            copy_image[end_x+padding,start_y-padding:end_y+(padding*2)] = 5
            textArray.append([start_x, start_y, end_x, end_y, np.round(((score/maxScore)*100), 2)])
        return copy_image, textArray

