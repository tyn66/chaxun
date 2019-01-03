from PIL import Image
import tesserocr
def sbyzm(cc):
    im = Image.open(cc) #用pil打开这个图片
    im = im.convert('L')
    # im = im.point(lambda x: 0 if x<100 else x>=100, '1') # 二值化 100为分割灰度的点（阀值），二值化就是将图片的颜色转换成非黑即白的图片
    # im1.show()  # 查看图片
    # 调用方法image_to_text() ,完成Image对象的识别
    resul = tesserocr.image_to_text(im)
    try :
        a = int(resul[0])
        b = int(resul[2])
        if resul[1] =="+":
            c = a + b
            return c
        else:
            c = a - b
            return c
    except:
        return "1"