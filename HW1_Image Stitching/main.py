from PIL import Image, ImageDraw
from sympy import *
import time

def equation(x1,y1,x2,y2,x3,y3,x11,y11,x22,y22,x33,y33):
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    d = Symbol('d')
    e = Symbol('e')
    f = Symbol('f')
    
    f1 = x11*a + y11*b + c - x1
    f2 = x22*a + y22*b + c - x2
    f3 = x33*a + y33*b + c - x3

    sol1 = solve((f1, f2, f3), a, b, c)
    
    f4 = x11*d + y11*e + f - y1
    f5 = x22*d + y22*e + f - y2
    f6 = x33*d + y33*e + f - y3
    
    sol2 = solve((f4, f5, f6), d, e, f)
    
    return sol1[a], sol1[b], sol1[c], sol2[d], sol2[e], sol2[f]

def bilinear(x,y,image):
    
    l = int(x)
    k = int(y)
    a = x - l
    b = y - k
    
    R = (1-a) * (1-b) * image.getpixel((l,k))[0] + a * (1-b) * image.getpixel((l+1,k))[0] + \
    (1-a) * b * image.getpixel((l,k+1))[0] + a * b * image.getpixel((l+1,k+1))[0]

    G = (1-a) * (1-b) * image.getpixel((l,k))[1] + a * (1-b) * image.getpixel((l+1,k))[1] + \
    (1-a) * b * image.getpixel((l,k+1))[1] + a * b * image.getpixel((l+1,k+1))[1]

    B = (1-a) * (1-b) * image.getpixel((l,k))[2] + a * (1-b) * image.getpixel((l+1,k))[2] + \
    (1-a) * b * image.getpixel((l,k+1))[2] + a * b * image.getpixel((l+1,k+1))[2]

    return R,G,B

def main(image1_name, image2_name, x1, y1, x2, y2, x3, y3, x11, y11, x22, y22, x33, y33, output_image_name):
    image1 = Image.open(image1_name)  # 需旋轉的圖
    image2 = Image.open(image2_name)  # 原圖
    width1, height1 = image1.size
    width2, height2 = image2.size

    a, b, c, d, e, f = equation(x1,y1,x2,y2,x3,y3,x11,y11,x22,y22,x33,y33) # 使用函式解出a,b,c,d,e,f
    
    newImage = Image.new( "RGB", (width2 + int(width1 * 0.7), int(height2 * 1.1)) , (255, 255, 255)) # 新建一個比原圖稍大的空白圖
    draw = ImageDraw.Draw(newImage)                                           
    
    new_x_range = width2 + int(width1 * 0.7) - 1
    for new_x in range(0, width2 + int(width1 * 0.7) - 1): # 迴圈開始畫圖
        if new_x%50 == 0:
            print(new_x, '/', new_x_range)
        for new_y in range(0, int(height2 * 1.1) - 1):
                      
            if 0 <= new_x <= width2 - 1 and 0 <= new_y <= height2 - 1: # 如果在原圖範圍直接畫上原圖的像素值
                draw.point((new_x , new_y), fill=(image2.getpixel((new_x,new_y))))            
                                                                    # 將像素位置加上長寬後再畫
                                                                    # 使旋轉後超出原圖的像素點可以畫上
            else:
                x = (a * new_x) + (b * new_y) + c                   # 不在原圖範圍內
                y = (d * new_x) + (e * new_y) + f                   # 先經過affine tranform計算
                
                if 0 <= x <= width1 - 1 and 0 <= y <= height1 - 1:  # 算出來的x,y範圍在需旋轉圖的寬高內                                                                                                                       
                    R,G,B = bilinear(x,y,image1)                    # 進行bilinear後將像素值畫上圖
                    draw.point((new_x, new_y), fill=(int(R),int(G),int(B)))  
                else:
                    continue
                   
    newImage.save(output_image_name) # 輸出圖片

if __name__ == '__main__':
    main("P3.jpg", "P2.jpg", x1=92, y1=458, x2=43, y2=466, x3=86, y3=656, x11=520, y11=401, x22=469, y22=411, x33=521, y33=605, output_image_name="temp.jpg")
    main("temp.jpg", "P1.jpg", x1=21, y1=636, x2=243, y2=622, x3=205, y3=689, x11=343, y11=577, x22=545, y22=598, x33=501, y33=653, output_image_name="output.jpg")