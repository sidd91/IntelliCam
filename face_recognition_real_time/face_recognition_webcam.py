import face_recognition 
import pickle
import cv2
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-e","--encodings", required=True)

args = vars(ap.parse_args())

data= pickle.loads(open(args["encodings"],"rb").read())
video_capture=cv2.VideoCapture(1)
process_this_frame= True

while True:
    ret, frame=video_capture.read()
    
    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    
    rgb_small_frame= small_frame[:, :, ::-1]

    if process_this_frame:
        
        boxes=face_recognition.face_locations(rgb_small_frame,model="cnn")
        encodings=face_recognition.face_encodings(rgb_small_frame,boxes)
        names=[]

        for face_encoding in encodings:
            matches= face_recognition.compare_faces(data["encodings"],face_encoding,0.4)
            name = "Unknown"
  
            if True in matches:
                first_match_index= matches.index(True)
                name= data["names"][first_match_index]



            names.append(name)
 
    process_this_frame= not process_this_frame

    for (top, right, bottom, left), name in zip(boxes, names):
             # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

          # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
vidieo_capture.release()
cv2.destroyAllWindows()
