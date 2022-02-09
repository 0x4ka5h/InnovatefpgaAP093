import cv2
import os
import numpy as np

trustedPersons = os.listdir('apiCenter/vehicleSide/validateface/trustedPersons/')
declinedPersons = os.listdir('apiCenter/vehicleSide/validateface/declinedPersons/')

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
                continue;
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)

            faces.append(image)
            labels.append(label)   
    return faces, labels

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







