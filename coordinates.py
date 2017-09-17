import difflib
import readtext
import getroomdesc

def roomNumToXandY(filename):
    numbertodesc = getroomdesc.run()
    floorplan = readtext.readText(filename)
    readings = []
    for key in floorplan:
        for reading in key.split():
            readings.append(reading)
    print(readings)
    res = {}
    for number in numbertodesc.keys():
        if number[:number.find('-')] == filename[:filename.find('_')] and
    number[number.find('-')+1:] == filename[filename.find('_')+1:]:
            txt = number[number.find('-') + 1:]
        try:
            closest = difflib.get_close_matches(txt, readings)[0]
        except IndexError:
            print('Unable to find', number)
            pass
        for key in floorplan:
            if closest in key:
                res[number] = floorplan[key]
    return res

print(roomNumToXandY('/Users/jennahimawan/Desktop/1_0.png'))
