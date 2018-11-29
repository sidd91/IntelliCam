import face_recognition 
import pickle
import cv2
import imutils
import argparse
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
import sys
import os


ap = argparse.ArgumentParser()
ap.add_argument("-e","--encodings", required=True)

args = vars(ap.parse_args())

data= pickle.loads(open(args["encodings"],"rb").read())
video_capture=cv2.VideoCapture(1)
process_this_frame= True
flag=False

def send_mail(send_from,send_to,file):
    #assert isinstance(send_to, list)
	msg = MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = send_to
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = "Intrustion Alert"
	img_data= open(file,'rb').read()
	image=MIMEImage(img_data, name=os.path.basename(file))
	msg.attach(image)
	server= smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login("siddharthchawla01@gmail.com", "Ilikeseries91")
	server.sendmail("siddharthchawla01@gmail.com","siddharthchawla01@gmail.com",msg.as_string())
	server.quit()
  
def notify(img):
	send_mail("siddharthchawla01@gmail.com","siddharthchawla01@gmail.com",img)

while True:
	print("Sarv")
	ret, frame=video_capture.read()

	small_frame=cv2.resize(frame,(0,0),fx=1,fy=1)

	rgb_small_frame= small_frame[:, :, ::-1]

	if process_this_frame:
    
		boxes=face_recognition.face_locations(rgb_small_frame,model="cnn")
		encodings=face_recognition.face_encodings(rgb_small_frame,boxes)
		names=[]

		for face_encoding in encodings:
			matches= face_recognition.compare_faces(data["encodings"],face_encoding,0.6)
			name = "Unknown"

			if True in matches:
				first_match_index= matches.index(True)
				name= data["names"][first_match_index]

			names.append(name)

	process_this_frame= not process_this_frame

	for (top, right, bottom, left), name in zip(boxes, names):
        	print("in for")
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
		if(name == "Unknown"):
			flag=True
			cv2.imwrite(os.path.join("/home/nvidia/work/cmpe220/Intruders",'intruder.png'),frame)
			notify("/home/nvidia/work/cmpe220/Intruders/intruder.png")
			print("notified")
                        break          
    			# Display the resulting imag
                print("sid")
                
	print("Siddharth")
	if flag==True:
                text= "Intruder detected"
         	os.system('curl https://notify.run/NAX4kZZjehexVvGh -d "Intruder detected ! Please check email for details" ')
		break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
