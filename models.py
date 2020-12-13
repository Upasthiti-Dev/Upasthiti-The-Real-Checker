from keras.models import load_model

# load model
model = load_model('face_model.h5')

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array


def load_image(filename):
    # load the image
    img = load_img(filename, target_size=(224, 224))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 224, 224, 3)
    # center pixel data
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img


# load an image and predict the class
def run_example():
    # load the image
    img = load_image('New.jpg')
    # predict the class
    result = model.predict(img)
    print(result)
    if (result[0] > 0.5):
        print('Apoorve attendance marked')
    else:
        print('Maaz attendance marked')