from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

#path to trained keras model
MODEL_PATH = "aircraft_detection.model"

#height and width of images when training
dimensions = 28

#load trained model
print("Loading model")
model = load_model(MODEL_PATH)

#Loading video feed
print("Starting video stream")
vs = VideoStream(2)
vs.start()
time.sleep(2.0)

while True:
    #read and resize each frame
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    #prepare image to be classified
    image = cv2.resize(frame, (dimensions, dimensions))
    image = image.astype("float")/255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    #classify image
    (A_UH8, B_L6R, C_G7C, D_S1P, E_JW3, F_A2X) = model.predict(image)[0]
    probability = max([A_UH8, B_L6R, C_G7C, D_S1P, E_JW3, F_A2X])

    if probability == A_UH8:
    	label = "A_UH8"
    if probability == B_L6R:
    	label = "B_L6R"
    if probability == C_G7C:
    	label = "C_G7C"
    if probability == D_S1P:
    	label = "D_S1P"
    if probability == E_JW3:
    	label = "E_JW3"
    if probability == F_A2X:
    	label = "F_A2X"

    label = "{}: {:.2f}%".format(label, probability * 100)
    frame = cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 0), 2)

    #output frame
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

print("Closing")
vs.stop()
cv2.destroyAllWindows()
