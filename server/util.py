import joblib
import json
import numpy as np
import cv2
import base64
from wavelet import w2d

__model=None
def classify_image(image_base64_data,file_path=None):
    
    imgs=get_cropped_img_if_2_eyes(file_path, image_base64_data)
    result=[]
    for img in imgs:
        raw_scale_img=cv2.resize(img,(32,32))
        g_img=w2d(img,'db1',5)
        raw_gscale_img=cv2.resize(g_img,(32,32))
        combined_img=np.vstack((raw_scale_img.reshape(32*32*3,1),raw_gscale_img.reshape(32*32,1)))
        
        len_image_array=32*32*3+32*32
        
        final=combined_img.reshape(1,len_image_array).astype(float)
        
        result.append({
            'class':class_number_name(__model.predict(final)[0]),
            'class_probability':np.round(__model.predict_proba(final)*100,2).tolist()[0],
            'class_dictionary':__class_name_to_number}
                      )
        
        
    return result
 
def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name
    
    with open("./artifacts/class_dictionary.json","r") as f:
        __class_name_to_number=json.load(f)
        __class_number_to_name={v:k for k,v in __class_name_to_number.items()}
        
        
    global __model
    if __model is None:
        with open("./artifacts/saved_model.pk1.txt","rb") as f:
            __model=joblib.load(f)
    print("loading saved artifacts...done")        
    
          
        

def get_cv2_image_from_base64_string(b64str):
    encoded_data=b64str.split(',')[1]
    nparr=np.frombuffer(base64.b64decode(encoded_data),np.uint8)
    img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    return img
def class_number_name(class_num):
    return  __class_number_to_name[class_num]
      
    
    
def get_cropped_img_if_2_eyes(img_path,img_base64_data):
    face_cascade=cv2.CascadeClassifier("C:/Users/Sai charan/Downloads/opencvcascades/haarcascade_frontalface_default.xml")
    eye_cascade=cv2.CascadeClassifier("C:/Users/Sai charan/Downloads/opencvcascades/haarcascade_eye.xml")
    
    if img_path:
        img=cv2.imread(img_path)
    else:
        img=get_cv2_image_from_base64_string(img_base64_data)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    eyes=()
    cropped_faces=[]
    for (x,y,w,h) in faces:
        face_img=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=img[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(roi_gray)
    if eyes is not None and len(eyes)>=2:
        cropped_faces.append(roi_color)
    return cropped_faces

def get_b64_test_img_for_virat():
    with open("b64.txt")as f:
        return f.read()


if __name__=="__main__":
    load_saved_artifacts()
   # print(classify_image(get_b64_test_img_for_virat(),None))
    print(classify_image(None,"C:/Users/Sai charan/Downloads/SportsPersonClassify/server/test_img/virat1.jpg"))