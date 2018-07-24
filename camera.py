import cv2
import numpy as np
import os
import time
from threading import Timer
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def stable(percentage):
    while (percentage>5):
        _,frame=cam.read()
        white_position=move.apply(frame)
        movement=np.array(white_position)
        white_pixel=np.count_nonzero(movement)
        percentage=(white_pixel*100)/np.size(movement)
        print(percentage)
        time.sleep(2)
    return 0


def SendMail(initial_id,final_id):
    
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Alert!!!'
    msg['From'] = ''      #enter the e-mail of sender
    msg['To'] = ''        #enter the e-mail of reciver
    text = MIMEText("Check this ")
    msg.attach(text)
    
    for i in range (initial_id,final_id):
        ImgFileName='proof/'+str(i)+'.jpg'
        img_data = open(ImgFileName, 'rb').read()
        image = MIMEImage(img_data, ImgFileName)
        msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(' ', '') #enter e-mail of sender and password
    s.sendmail(msg['From'],msg['To'], msg.as_string())
    s.quit()
    return final_id


final_id=0
initial_id=1
thresold=10       

cam=cv2.VideoCapture(0)
move=cv2.createBackgroundSubtractorMOG2()

if not os.path.exists('proof'):
    os.makedirs('proof')

for the_file in os.listdir('proof'):
    file_path = os.path.join('proof', the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
    
while True:
    _,frame=cam.read()
    white_position=move.apply(frame)
    movement=np.array(white_position)
    white_pixel=np.count_nonzero(movement)
    percentage=(white_pixel*100)/np.size(movement)
    
    if final_id==0:
       percentage=stable(percentage)
       final_id+=1
       print('Security is on')
       
    if(percentage>thresold):
        print("pic taken")
        cv2.imwrite('proof/'+str(final_id)+'.jpg',frame)
        final_id+=1
        
    
    if(cv2.waitKey(1)==ord('q')):
        break;

cam.release()
cv2.destroyAllWindows()


    

