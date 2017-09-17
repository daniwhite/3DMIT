import difflib
import readtext
import getroomdesc
from PIL import Image, ImageDraw

def roomNumToXandY(filename):
    numbertodesc = getroomdesc.numberToDesc(filename)
    floorplan = readtext.readText(filename)
    print(floorplan)
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)
    filename = filename.split('/')[-1]
    readings = []
    for key in floorplan:
        for reading in key.split():
            readings.append(reading)
##    print(readings) # debug print statement

    res = {}
    for number in numbertodesc.keys():
        if (number[:number.find('-')] == filename[:filename.find('_')]) and \
    (number[number.find('-')+1:number.find('-')+2] == filename[filename.find('_')+1:filename.find('_')+2]):
            txt = number[number.find('-') + 1:]
        else:
            continue
        try:
            closest = difflib.get_close_matches(txt, readings, 2)[0]
            for key in floorplan:
                if closest in key.split():
                    res[number] = floorplan[key]
                    draw.ellipse([floorplan[key][0], floorplan[key][1], floorplan[key][0] + 20, floorplan[key][1] + 20], fill = 'blue', outline ='blue')
        except IndexError:
            print('Unable to find', number)
            pass
    filename = filename.replace('.png', '')
    image.save(filename + 'withdots.png')
    return res

# Coordinate system for ImgDraw and the X Y coordinates uses top left as (0,0)!

print(roomNumToXandY('/Users/jennahimawan/Desktop/1_0-005.png'))
