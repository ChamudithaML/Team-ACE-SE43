# Importing required python libraries
import numpy as np    # numpy for arrays
from tensorflow.keras.preprocessing import image   
from tensorflow.keras.models import load_model    # importing keras load_model to import model

# names of classes. use to assign names to prediction
classes = ['Apple Red 1', 'Apple Red 2', 'Apple Red 3', 'Apple Red Delicious', 'Avocado',
 'Banana', 'Carambula', 'Cauliflower', 'Eggplant', 'Grape Blue', 
'Guava', 'Onion Red', 'Onion Red Peeled', 'Orange', 'Pepper Green', 'Pitahaya Red', 'Watermelon']

# model using function. taking file name as parameter
def prediction_func2(filename):
    new_model = load_model('fruityeye/models/model1.h5')   # loading the trained model
    test_image = image.load_img('fruityeye/images\\' + filename, target_size=(100, 100))   # loading images using file name and resizing to feed the model.
    test_image = image.img_to_array(test_image)   # adding image to numpy array
    test_image = np.expand_dims(test_image, axis=0)   # expanding a dimention to feed the model
    result = new_model.predict(test_image)   # feeding the model

    # accessing the prediction result
    result1 = result[0]  

    # variable to hold array index
    k=0 

    # this loop to assign class name according to output
    for i in range(17):
        if result1[i] == 1.:
            k=i
            break

    # taking class name using index and stroring it in variable
    prediction = classes[k]

    # returning class name
    return prediction,k