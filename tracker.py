import cv2
import mediapipe as mp
import numpy as np
import socket
import threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),2183))



def handle_client(client_socket):
   base_options = mp.tasks.BaseOptions(model_asset_path='gesture_recognizer.task')
   options = mp.tasks.vision.GestureRecognizerOptions(base_options=base_options
                                                   ,running_mode= mp.tasks.vision.RunningMode.IMAGE)
   cap = cv2.VideoCapture(0) 
   with mp.tasks.vision.GestureRecognizer.create_from_options(options) as recognizer:
     while True:
      # Read video frame by frame 
        success, img = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        result = recognizer.recognize(mp_image)
        if(len(result.gestures) > 0):
         if(result.gestures[0][0].category_name == 'Open_Palm'):
             result = 1
         else:
             result = 0
         client_socket.send(bytes(str(result),'utf-8'))      
        else:
         client_socket.send(bytes('0','utf-8'))      




            
s.listen(1)
while True:
  client_socket, client_address = s.accept()
  print(f"Accepted connection from {client_address}") 
  client_handler = threading.Thread(target=handle_client, args=(client_socket,))
  client_handler.start()