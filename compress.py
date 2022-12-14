from PIL import Image
import sys
import os


rgb_map = {(0,0,0): 0x0, (0, 0, 255): 0x1, (0, 128, 0): 0x2, (0, 255, 255): 0x3, (255, 0, 0): 0x4, (255, 0, 255): 0x5, (150, 75, 0): 0x6, (255, 255, 255): 0x7,(0, 150, 255): 0x9
,  (170, 255, 0):0xa, (65, 253, 254): 0xb, (238, 75, 43): 0xc, (255, 0, 205): 0xd, (255, 255, 0): 0xe, (253, 254, 255):0xf  }

def extract_colors(image, pixels_per_row, rows):
    pix = image.load()
    pixel_colors = [[0] * pixels_per_row for i in range(rows)]
    
    print(len(pixel_colors))
    for r in range(rows):
        for c in range(pixels_per_row): 
            pixel_colors[r][c] = rgb_map[pix[r,c]]
    print(pixel_colors)
def customConvert(silf, palette, dither=False):
    ''' Convert an RGB or L mode image to use a given P image's palette.
        PIL.Image.quantize() forces dither = 1. 
        This custom quantize function will force it to 0.
        https://stackoverflow.com/questions/29433243/convert-image-to-specific-palette-using-pil-without-dithering
    '''

    silf.load()

    # use palette from reference image made below
    palette.load()
    im = silf.im.convert("P", 0, palette.im)
    # the 0 above means turn OFF dithering making solid colors
    return silf._new(im)


if __name__ == "__main__":
    for filename in os.listdir('/Users/jackiedong/Desktop/CSProjects/images/animals'):
        # path = sys.argv[1]
        path = filename
        palette = (
            0,0,0, # black
            0,0,255, # blue
            0, 128, 0, # green
            0, 255, 255, # cyan
            255,0, 0, # red
            255, 0, 255, # magenta
            150, 75, 0, # brown
            255, 255, 255, # white
            128, 128, 128, # gray
            0, 150, 255, # bright blue
            170, 255, 0,# bright green
            65, 253, 254, # bright cyan
            238, 75, 43, # bright red
            255, 0, 205, # bright magenta
            255, 255, 0, # yellow
            253, 254, 255, # bright white
        )


        # a palette image to use for quant
        paletteImage = Image.new('P', (1, 1))
        paletteImage.putpalette(palette + (0,0,0)*240)


        old_image = Image.open(f'/Users/jackiedong/Desktop/CSProjects/images/animals/{path}')
        # open the source image
        # resized_image = old_image.resize((640, 480)).convert('RGB')

        imageNew = old_image.convert('RGB').quantize(palette=paletteImage)

        # imageCustomConvert = customConvert(old_image, paletteImage, dither=False).convert('RGB')
        imageNew.save(f'new-images/new-{path}', 'PNG')
        
        # old_image = Image.open('new.png')

        # extract_colors(old_image, 480, 640)
        px = imageNew.load()
        
        pixel_colors = [[0] * 640 for i in range(480)]


        for r in range(480): 
            for c in range(640):
                pixel_colors[r][c] = str(px[c,r])
                
        rowstrs = []
        for r in range(480):
            rowstr = '{' + ','.join(pixel_colors[r]) + '}'
            rowstrs.append(rowstr)
            
        # print('{' + ','.join(rowstrs) + '}')
        
        f = open(f'bitmap/{path.replace(".jpeg","")}.inc', 'w')
        f.write(','.join(rowstrs))
            