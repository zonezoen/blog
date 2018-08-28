import pytesseract
from PIL import Image, ImageDraw, ImageFilter


# 识别验证码
def recognize(imgName):
    im = Image.open(imgName)

    # im = Image.open(io.BytesIO(b))
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('gray-' + imgName)
    # 二值化，采用阈值分割法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    out.save('b' + imgName)
    # 识别
    text = pytesseract.image_to_string(out)
    print("识别结果："+text)
    return text


def open_img(giffile):
    img = Image.open(giffile)  # 打开图片
    img = img.convert('RGB')  # 转换为RGB图
    pixdata = img.load()  # 转换为像素点图
    return img, pixdata


def removeLine(imgName):
    (img, pixdata) = open_img(imgName)
    for x in range(img.size[0]):  # x坐标
        for y in range(img.size[1]):  # y坐标
            if pixdata[x, y][0] < 8 or pixdata[x, y][1] < 6 or pixdata[x, y][2] < 8 or (
                    pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2]) <= 30:  # 确定颜色阈值
                if y == 0:
                    pixdata[x, y] = (255, 255, 255)
                if y > 0:
                    if pixdata[x, y - 1][0] > 120 or pixdata[x, y - 1][1] > 136 or pixdata[x, y - 1][2] > 120:
                        pixdata[x, y] = (255, 255, 255)  # ?

    # 二值化处理
    for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 160 and pixdata[x, y][1] < 160 and pixdata[x, y][2] < 160:
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 深度边缘增强滤波，会使得图像中边缘部分更加明显（阈值更大），相当于锐化滤波
    img.resize(((img.size[0]) * 2, (img.size[1]) * 2), Image.BILINEAR)  # Image.BILINEAR指定采用双线性法对像素点插值#?
    img.save('remove-' + imgName)
    print("除线成功！")

    recognize('remove-' + imgName)


recognize('code.jpg')
# removeLine('logo3.gif')
