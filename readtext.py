# import the necessary packages
from PIL import Image
from tesserocr import PyTessBaseAPI, RIL

def readText(filename):
    res = {}
    image = Image.open(filename)
    with PyTessBaseAPI() as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print(('Found {} textline image components.').format(len(boxes)))
        for i, (im, box, _, _) in enumerate(boxes):
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            if ocrResult != '':
                res[ocrResult] = (box['x'] + box['w']/2, box['y'] + box['h']/2)
    return res
    

print(readText('/Users/jennahimawan/Desktop/1_0.png'))
