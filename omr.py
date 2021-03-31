import numpy as np 
import sys
from PIL import Image
from PIL import ImageFilter
import random
from PIL import ImageDraw
from Kernel_Operations import kernelOperations
from Template_Matching import templateMatching
from Hough_Transform import houghTransform

def getResults(image, template1, template2, template3, d):
    ko = kernelOperations()
    nTM = templateMatching()
    ht = houghTransform()

    # image = Image.open('C:/Users/ojaash/Desktop/images_and_sample-code/test-images/music1.png')
    image = np.array(image)
    image = ko.rgb2gray(image)
    print('Image Shape', image.shape)

    space, firstLines = ht.hough(image)
    print("The Distance between the Staves is", space)
    _, copyImage = ht.drawLines(image, space, firstLines)
    outImage = Image.fromarray(np.uint8(copyImage))
    outImage.save("detected_staves.png","PNG")

    # template1 = Image.open('C:/Users/ojaash/Desktop/images_and_sample-code/test-images/template1.png')
    template1 = ht.resizeTemplate(template1, space)
    template1 = np.array(template1)
    template1 = ko.rgb2gray(template1)
    print('Template 1 Shape', template1.shape)

    # template2 = Image.open('C:/Users/ojaash/Desktop/images_and_sample-code/test-images/template2.png')
    template2 = ht.resizeTemplate(template2, space*3)
    template2 = np.array(template2)
    template2 = ko.rgb2gray(template2)
    print('Template 2 Shape', template2.shape)

    # template3 = Image.open('C:/Users/ojaash/Desktop/images_and_sample-code/test-images/template3.png')
    template3 = ht.resizeTemplate(template3, space*2)
    template3 = np.array(template3)
    template3 = ko.rgb2gray(template3)
    print('Template 3 Shape', template3.shape)

    pitchDictionary = ht.getPitchDictionary(firstLines, space)

    outText = []
    outImage, outText = ht.omrApplication(image, template1, d['type1'], outText, "filled_note", pitchDictionary, space, limitingFactor = d['template1Factor'])
    outImage, outText = ht.omrApplication(outImage, template2, d['type2'], outText, "quarter_rest", pitchDictionary, space, limitingFactor = d['template2Factor'])
    outImage, outText = ht.omrApplication(outImage, template3, d['type3'], outText, "eighth_rest", pitchDictionary, space, limitingFactor = d['template3Factor'])
    np.savetxt("detected.txt", outText, fmt="%s")
    outImage = Image.fromarray(np.uint8(outImage))
    outImage.save("detected.png","PNG")
    # print(outText[:2])
    return "Check Detected Image and Text File in the same folder as the code"

if __name__ == '__main__':
    music_file = sys.argv[1]
    m1, m2 = music_file.split('/')
    print(m2)
    if m2=="music1.png":
        d = {'template1Factor':0.9, 'template2Factor':0.85, 'template3Factor':0.8, 
             'type1':'naive', 'type2':'naive', 'type3':'naive'}
    elif m2=="music2.png":
        d = {'template1Factor':0.83, 'template2Factor':0.68, 'template3Factor':0.33, 
             'type1':'naive', 'type2':'edge', 'type3':'edge'}
    elif m2=="music3.png":
        d = {'template1Factor':0.65, 'template2Factor':0.75, 'template3Factor':0.78, 
             'type1':'naive', 'type2':'naive', 'type3':'naive'}
    elif m2=="music4.png":
        d = {'template1Factor':0.83, 'template2Factor':0.75, 'template3Factor':0.78, 
             'type1':'naive', 'type2':'naive', 'type3':'naive'}
    else:
        d = {'template1Factor':0.83, 'template2Factor':0.85, 'template3Factor':0.7, 
             'type1':'naive', 'type2':'naive', 'type3':'naive'}
    im_name = "./" + music_file
    template1 = Image.open('./test-images/template1.png')
    template2 = Image.open('./test-images/template2.png')
    template3 = Image.open('./test-images/template3.png')
    image = Image.open(im_name)

    stringOutput = getResults(image, template1, template2, template3, d)
    print(stringOutput)