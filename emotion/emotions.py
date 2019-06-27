import cv2
import numpy as np
from keras.models import load_model
from statistics import mode
import matplotlib as mpl
mpl.use('PDF')
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from imutils.video import VideoStream
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import imutils
import time



emotion_model_path = './models/emotion_model.hdf5'
emotion_labels = get_labels('fer2013')

frame_window = 10
emotion_offsets = (20, 40)

face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model_path)

emotion_target_size = emotion_classifier.input_shape[1:3]

emotion_window = []
cap = None
camera =  VideoStream(src=0).start()
#camera.resolution = (640, 480)
#camera.framerate = 25
#rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
while True : 
    bgr = camera.read()


    gray_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    k=0
    for face in faces:
        
        x1, x2, y1, y2 = apply_offsets(face, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)
        k=k+1
        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue
        
        print (emotion_text,k)
        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face, rgb, color)
        draw_text(face, rgb, emotion_mode,
                  color, 0, -45, 1, 1)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
