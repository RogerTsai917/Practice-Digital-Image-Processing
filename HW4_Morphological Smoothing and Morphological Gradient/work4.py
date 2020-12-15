from PIL import Image, ImageDraw
def getpixel(x,y,image,num = 3):
    pixelArray = []
    for i in range(-(int(num/2)),int(num/2)+1):
        for j in range(-(int(num/2)),int(num/2)+1):
            pixel = image.getpixel((x + j ,y + i))
            pixelArray.append(pixel)
    
    return(pixelArray)

def dilation(x, y, image):
    pixel = getpixel(x,y,image)
    result = -1
    for each_pixel in pixel:
        temp = each_pixel + 1
        if temp > result: result = temp
    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result)

def erosion(x, y, image):
    pixel = getpixel(x,y,image)
    result = 256
    for each_pixel in pixel:
        temp = each_pixel - 1
        if temp < result: result = temp
    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result)

def opening(width, height, image):
    OpeningImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(OpeningImage)
    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = erosion(x, y, image)
            draw.point((x,y), fill=(pixel))
    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = dilation(x, y, image)
            draw.point((x,y), fill=(pixel))
    return OpeningImage

def closing(width, height, image):
    ClosingImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(ClosingImage)
    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = dilation(x, y, image)
            draw.point((x,y), fill=(pixel))
    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = erosion(x, y, image)
            draw.point((x,y), fill=(pixel))
    return ClosingImage

def gradient(width, height, image):
    OpeningImage = opening(width, height, image)
    ClosingImage = closing(width, height, image)
    
    GradientImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(GradientImage)
    for x in range(0, width):       
        for y in range(0, height):
            pixel = OpeningImage.getpixel((x,y))-ClosingImage.getpixel((x,y))
            if pixel > 255: pixel = 255 
            elif pixel < 0: pixel = 0
            draw.point((x,y), fill=(int(pixel)))
    return GradientImage

def main():
    image = Image.open( 'dog.jpg' )
    width, height = image.size

    GrayImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(GrayImage)

    for x in range(0, width):       
        for y in range(0, height):
            Grayscale = (image.getpixel((x,y))[0]+image.getpixel((x,y))[1]+image.getpixel((x,y))[2])/3
            draw.point((x,y), fill=(int(Grayscale)))
    # GrayImage.show()
    GrayImage.save("GrayImage.jpg")
    
    SmoothingImage = opening(width, height, GrayImage)
    SmoothingImage = closing(width, height, SmoothingImage)
    # SmoothingImage.show()
    SmoothingImage.save( "SmoothingImage.jpg" )
    
    GradientImage = gradient(width, height, GrayImage)
    # GradientImage.show()
    GradientImage.save( "GradientImage.jpg" )

if __name__ == '__main__':
    main()