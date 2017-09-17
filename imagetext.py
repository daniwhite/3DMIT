from PIL import Image, ImageDraw, ImageFont
import getroomdesc

# make the dictionary mapping numbers -> descriptions
numbertodesc = getroomdesc.run()

counter = 0

for number in numbertodesc.keys():
    # just room #, not building #
    txt = number[number.find('-') + 1:]
    
    # make a blank image for the text, initialized to transparent text color
    im = Image.new('RGBA', (200, 200), (255, 255, 255,1))

    # get a font
    fnt = ImageFont.truetype('/Users/jennahimawan/HackMIT/efitypereverse-regular.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(im)

    # draw text
    d.text((50,50), txt, font=fnt, fill=(0, 0, 0, 255))

    # im.show() # show the image you got, for debugging
    im.save(str(counter), 'PNG')

    counter += 1
