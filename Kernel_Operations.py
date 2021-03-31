import numpy as np 
import random

class kernelOperations:
    
    def __init__(self):
        self.randomInit = 0

    def rgb2gray(self, rgb):
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

    def inseperableKernel(self, im, kernel):
        kernel = np.flipud(np.fliplr(kernel))
        im_arr = np.array(im)
        # im_arr = self.rgb2gray(im_arr)
        n = kernel.shape[0]
        midPt = int(np.floor(n/2))
        divisionFactor = np.sum(kernel)
        if divisionFactor==0:
            divisionFactor = n*n
        arr = np.pad(im_arr, midPt, mode='constant')
        # print(arr)
        h, w = arr.shape

        # kernel = np.random.uniform(0,1,n*n).reshape(n,n)
        outImg = np.random.randn(im_arr.shape[0], im_arr.shape[1])
        for i in range(0,h-n+1):
            for j in range(0,w-n+1):
                ex = arr[i:i+n,j:j+n]*kernel  
                sum1 = np.sum(ex)
                # outImg[i,j] = ex[midPt,midPt]
                outImg[i,j] = int(sum1/divisionFactor)

        outImg = outImg.astype(int)
        outImg = np.where(outImg>255,255,outImg)
        outImg = np.where(outImg<0,0,outImg)
        return outImg

    def seperableKernel(self, im, hx, hy):
        
        im_arr = np.array(im)
        n = hy.shape[1]
        midPt = int(np.floor(n/2))
        arr = np.pad(im_arr, midPt, mode='constant')
        h, w = arr.shape
        tempImg = np.random.randn(h-(2*midPt), w)
        # print(tempImg.shape)
        for i in range(h-n+1):
            for j in range(w):
                temp = arr[i:i+n,j].reshape(n,1) * hx.T
                # tempImg[i,j] = int((np.sum(np.abs(temp)))/(divisionFactor)) 
                tempImg[i,j] = np.abs(np.sum(temp))
        divisionFactor = np.sum(hx.T*hy)
        if divisionFactor==0:
            divisionFactor = n
        outImg = np.random.randn(tempImg.shape[0], tempImg.shape[1]-(2*midPt))

        # print(outImg.shape)
        for i in range(tempImg.shape[0]):
            for j in range(tempImg.shape[1]-n):
                temp = tempImg[i,j:j+n] * hy
                outImg[i,j] = int((np.abs(np.sum(temp)))/(divisionFactor))
        outImg = outImg.astype(int)
        outImg = np.where(outImg>255,255,outImg)
        outImg = np.where(outImg<0,0,outImg)
        
        return outImg

    def inseperableSobelX(self):
        arr = np.array([[1,2,1],
                        [0,0,0],
                        [-1,-2,-1]])
        return arr

    def inseperableSobelY(self):
        arr = np.array([[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]])
        return arr

    def inseperableRandomIntegers(self, kernel_size=3):
        arr = np.random.randint(0,3,size=(kernel_size,kernel_size))
        arr = np.array(arr)
        return arr   

    def inseperableRandomNumbers(self, kernel_size=3):
        arr = np.abs(np.random.randn(kernel_size,kernel_size))
        arr = np.array(arr)
        return arr

    def seperableSobelX(self):
        hx = np.array([[1,0,-1]])
        hy = np.array([[1,2,1]])
        return hx,hy

    def seperableSobelY(self):
        hx = np.array([[1,2,1]])
        hy = np.array([[-1,0,1]])
        return hx,hy

    def seperableRandomNumbers(self):
        scaling1, scaling2 = np.random.randint(1,4),np.random.randint(1,4)
        hx = np.abs(np.random.randn(1,3)*scaling1)
        hy = np.abs(np.random.randn(1,3)*scaling2)
        return hx, hy