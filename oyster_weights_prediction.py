from tensorflow import keras
import cv2


def Load_model():
	oyster = keras.models.load_model("./oyster.h5")
	return oyster


def prepare(filepath):	#如果輸入為單張相片預測
    IMG_SIZE = 320
    IMAGE_CHANNEL = 3 
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, IMAGE_CHANNEL)

def concat_img(img1,img2):	#如果輸入為兩張相片預測
	IMG_SIZE = 320
	IMAGE_CHANNEL = 3 
	pic1 = cv2.imread(img1)
	pic2 = cv2.imread(img2)
	gray1 = cv2.resize(pic1,(320,160))
	gray2 = cv2.resize(pic2,(320,160))
	new_img = cv2.vconcat([gray1, gray2])
	new_array = cv2.resize(new_img, (IMG_SIZE, IMG_SIZE))
	return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, IMAGE_CHANNEL)