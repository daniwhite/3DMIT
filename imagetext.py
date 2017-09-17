from PIL import Image, ImageDraw, ImageFont
# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', (200, 200), (255, 255, 255,1))

# get a font
fnt = ImageFont.truetype('/Users/jennahimawan/HackMIT/efitypereverse-regular.ttf', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((50,50), "HELLO", font=fnt, fill=(0, 0, 0, 255))

txt.show()
txt.save('sometitle', 'PNG')

# can modify later to run getroomdesc.py, use the keys from the dictionary,
# and generate images that have room names on them
