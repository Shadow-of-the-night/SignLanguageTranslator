import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # 过滤日志输出

#对图像进行图像预处理 阈值分割图像截取需要的信息 并将此图像存在当前路径的temp.jpg文件
def pre_pic(path):

    lower_green = np.array([50, 43, 46])
    upper_green = np.array([99, 255, 255])

    img = cv2.imread(path)
    background = np.zeros([img.shape[0], img.shape[1]], np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(img, lower_green, upper_green)

    kernel = np.ones((1, 1), np.uint8)  # 定义卷积核

    binary = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel, iterations=2)

    canny = cv2.Canny(binary, 50, 100)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    area = []
    for k in contours:
        area.append(cv2.contourArea(k))
    max_idx = np.argmax(np.array(area))

    cv2.drawContours(background, contours, max_idx, 255, cv2.FILLED)

    canny = background

    high = 0
    low = 0
    left = 0
    right = 0
    flag = 1
    for index, i in enumerate(canny):
        if cv2.countNonZero(i):
            low = index
            if flag:
                high = index
                flag -= 1
    flag = 1
    for index, i in enumerate(canny.T):
        if cv2.countNonZero(i):
            right = index
            if flag:
                left = index
                flag -= 1

    res = background[high:low, left:right]
    # res = cv2.resize(res, (255, 255))

    cv2.imwrite("temp.jpg", res)

def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range
    return image


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)


def image_pretreatment(img):
    lower_green = np.array([50, 43, 46])
    upper_green = np.array([99, 255, 255])
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(img, lower_green, upper_green)
    kernel = np.ones((3, 3), np.uint8)  # 定义卷积核
    binary = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel, iterations=2)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=5)

    return binary

#path为处理完用于识别图片的保存路径 在这里也就是temp.jpg
def test_one_image(path):
    list1 = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]  #对应的输出结果列表
    image_ds = tf.data.Dataset.from_tensors(path).map(load_and_preprocess_image)
    # image_ds = tf.data.Dataset.from_tensor_slices(all_image_paths).map(load_and_preprocess_image)
    # 注意 from_tensor_slices 和 from_tensors 方法的区别
    test_image = np.array(list(image_ds.as_numpy_iterator()))
    #载入模型
    model = keras.models.load_model('./saved_model2')
    results = model.predict(test_image)
    print(np.argmax(results, axis=-1))
    word = list1[np.argmax(results, axis=-1)[0]]
    print("识别结果：" + word)
    return word


'''
for i in range(12):
    print("识别"+str(i)+"照片")
    path="./test/"+str(i)+'.jpg'
    test_one_image(path)
    print("----------")
#time.sleep(1)       # 识别频率
'''

'''测试代码
list1 =['a','b','c','d','e','f','g','h','i','j','k','l','m']
path = './test/'
for i in list1:
    t = i
    for j in range(1,4):
        pathname=path+t+"-"+str(j)+".jpg"
        img = image_pretreatment(pathname)
        cv2.imwrite("./temp.jpg",img)
        test_one_image('./temp.jpg')

'''
#pre_pic('D:\\dataset\\5\\22.jpg')
print(test_one_image('temp.jpg'))
