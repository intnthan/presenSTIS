import cv2 
import numpy as np
import os 
import pickle

from ultralytics import YOLO 
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input

from sklearn.metrics.pairwise import cosine_similarity

class faceRecognition: 
    def __init__(self):
        self.detector = self.load_detector()
        self.target_size = (224,224)
        self.model = self.load_model_faceRecognition()
        self.threshold = 0.8
        
    # load model face detection
    def load_detector(self):
        model = YOLO('app/face_recognition/yolov8n-face.pt')
        return model
    
    def load_model_faceRecognition(self):
        model = load_model('app/face_recognition/vgg16_model.h5')
        return model 
    
    def load_embedding(self):
        embedding = pickle.load(open('app/embeddings/222011537.pickle', 'rb'))
        return embedding
    
    # build model face detector
    def face_detection(self):
        camera = cv2.VideoCapture(0)
               
        while True: 
            success,frame = camera.read()
            if success:
                results = self.detector(frame, stream=True, max_det=1)
                for r in results: 
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)  
                        
                        # mendapatkan wajah yang terdeteksi 
                        face = frame[y1:y2, x1:x2]
                        face = cv2.resize(face, self.target_size)
                        matched = self.face_recognition(face)
                        if (matched[0]): 
                            print(matched)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  
                        else:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)  
                            
                        
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else: 
                break 
        camera.release()
    
    def face_recognition(self, face):
        face = self.preprocess_image(face)
        
        # get embedding from database dan embedding from frame
        embedding = self.load_embedding()
        new_embedding = self.model.predict(face)[0,:]
        
        # verify face with cosine similarity
        similarity = cosine_similarity(embedding.reshape(1,-1), new_embedding.reshape(1,-1))[0][0]
        if(similarity > self.threshold):
            return True, similarity
        else:
            return False, similarity
    
    def preprocess_image(self, face):
        image = cv2.resize(face, self.target_size)
        image = np.expand_dims(face, axis=0)
        image = preprocess_input(image)
        return image