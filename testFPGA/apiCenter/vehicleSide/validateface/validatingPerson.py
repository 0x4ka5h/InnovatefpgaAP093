from re import L
import cv2
import os
import numpy as np
from PIL import Image
import face_recognition as face_rec

trustedPersons =  os.listdir('apiCenter/vehicleSide/validateface/trustedPersons/')
declinedPersons = os.listdir('apiCenter/vehicleSide/validateface/declinedPersons/')
faceCasc = cv2.CascadeClassifier("apiCenter/vehicleSide/validateface/haarcascade_frontalface_default.xml")

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    
    for dir_name in dirs:

        if data_folder_path=="apiCenter/vehicleSide/validateface/trustedPersons/":
            if not dir_name.startswith("t"):
                continue;
            label = int(dir_name.replace("tp", ""))
        else:
            if not dir_name.startswith("d"):
                continue;
            label = int(dir_name.replace("dp", ""))
        

        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            PIL_img=Image.open(image_path).convert('L')
            image=np.array(PIL_img, 'uint8')
            #image = cv2.imread(image_path,2)
            
            faces_ = faceCasc.detectMultiScale(image)
            if len(faces_) == 0 :
                continue

            
            (x, y, w, h) = faces_[0]
            faces.append(image[y:y+h, x:x+w])
            labels.append(label)   
    return faces, labels

def resize(img, size) :
    width = int(img.shape[1]*size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation= cv2.INTER_AREA)


path = 'apiCenter/vehicleSide/validateface/trustedPersons/'
studentImg = []
studentName = []
myList = os.listdir(path)
for cl in myList :
    curimg = cv2.imread(f'{path}/{cl}')
    studentImg.append(curimg)
    studentName.append(os.path.splitext(cl)[0])

def findEncoding(images) :
    imgEncodings = []
    for img in images :
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings

EncodeList = findEncoding(studentImg)


def predictTrustedPerson(face):
    cv2.imwrite("apiCenter/vehicleSide/validateface/test/un.jpg",face)
    
    for i in os.listdir("apiCenter/vehicleSide/validateface/trustedPersons/"):
        known_image = face_rec.load_image_file("apiCenter/vehicleSide/validateface/trustedPersons/"+i)
        unknown_image = face_rec.load_image_file("apiCenter/vehicleSide/validateface/test/un.jpg")
        me = face_rec.face_encodings(known_image)[0]
        you = face_rec.face_encodings(unknown_image)[0]
        results = face_rec.compare_faces([me], you)
        if results[0]==True:
            return 1
    return
def predictDeclinedPerson(face):
    cv2.imwrite("apiCenter/vehicleSide/validateface/test/un.jpg",face)
    for i in os.listdir("apiCenter/vehicleSide/validateface/declinedPersons/"):
        known_image = face_rec.load_image_file("apiCenter/vehicleSide/validateface/declinedPersons/"+i)
        unknown_image = face_rec.load_image_file("apiCenter/vehicleSide/validateface/test/un.jpg")
        me = face_rec.face_encodings(known_image)[0]
        you = face_rec.face_encodings(unknown_image)[0]
        results = face_rec.compare_faces([me], you)
        if results[0]==True:
            return 1
    return

def trainTrustedPersons():
    faces, labels = prepare_training_data("apiCenter/vehicleSide/validateface/trustedPersons/")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save("apiCenter/vehicleSide/validateface/trustedPersons.yml")

def trainDeclinedPersons():
    faces, labels = prepare_training_data("apiCenter/vehicleSide/validateface/declinedPersons/")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save("apiCenter/vehicleSide/validateface/declinedPersons.yml")

'''
def predictTrustedPerson(face):

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read("apiCenter/vehicleSide/validateface/trustedPersons.yml")
    label, confidence = face_recognizer.predict(face)
    #get name of respective label returned by face recognizer
    #label_text = trustedPersons[label]
    
    return confidence

def predictDeclinedPerson(face):

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read("apiCenter/vehicleSide/validateface/declinedPersons.yml")
    label, confidence = face_recognizer.predict(face)
    #label_text = declinedPersons[label]
    return confidence
'''






