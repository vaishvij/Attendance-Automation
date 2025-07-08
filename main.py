import cv2 as cv
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("Enter path of your private key here")
firebase_admin.initialize_app(cred,{"databaseURL":"Enter path of your realtime Database here","storageBucket":"Enter path of your storage bucket here"})

bucket=storage.bucket()

cap=cv.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
#Sets the webcam on the basis of stock image
#Used to show attendance portal

#Load the background image
backImage=cv.imread("Resources/Attendance Portal.png")

modePath="Resources/Modes"
modePathList=os.listdir(modePath)

modeList=[]

for path in modePathList:
    modeList.append(cv.imread(os.path.join(modePath,path)))
    #os.path.join(ModePath, path) constructs the full path to the image by joining the directory path (ModePath) with the filename (path).

print("!! Beginning of loading of file !!")
#Getting the encoding file
file2=open("EncodeFile.p","rb")
encodeListWithId=pickle.load(file2)
file2.close()

#Separate encoding and student id
encodeList,studentId=encodeListWithId
print("!! File Loaded !!")

modeCounter=0
counter=0
id=-1
studentImage=[]

while True:
    success, img=cap.read()
    
    #Resizing image to match the region of background
    img=cv.resize(img,(640,480))
    
    imgSmall=cv.resize(img,(0,0),None,0.25,0.25)
    imgSmall=cv.cvtColor(imgSmall,cv.COLOR_BGR2RGB)
    
    # Comparison of encodings of faces in current frame with existing ones
    curFaceFrame=face_recognition.face_locations(imgSmall)
    encodingOfCurrentFrame=face_recognition.face_encodings(imgSmall,curFaceFrame)
    
    #Overlaying
    backImage[162:162+480,55:55+640]=img
    backImage[44:44+633,808:808+414]=modeList[modeCounter]
    
    if curFaceFrame:
        for encodeFace,faceLoc in zip(encodingOfCurrentFrame,curFaceFrame):
            match=face_recognition.compare_faces(encodeList,encodeFace)
            faceDistance=face_recognition.face_distance(encodeList,encodeFace)
        
            matchIndex=np.argmin(faceDistance)
            
            if match[matchIndex]:
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox=55+x1,162+y1,x2-x1,y2-y1
                backImage=cvzone.cornerRect(backImage,bbox,rt=0)
                #ID of student whose match is found
                id=studentId[matchIndex]
                if counter==0:
                    cvzone.putTextRect(backImage,"Loading",(275,400))
                    cv.imshow("Attendance Portal",backImage)
                    cv.waitKey(1)
                    counter=1
                    modeCounter=2
                    
        if counter!=0:
            
            #We are downloading only in the first frame .
            if counter==1:
                studentInfo=db.reference(f"Students/{id}").get()
                print(studentInfo)
                #Getting profile images of student
                blob=bucket.get_blob(f"Images/{id}.png")
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                studentImage=cv.imdecode(array,cv.COLOR_BGRA2BGR)
                #Update attendance
                datetimeObject=datetime.strptime(studentInfo["last_attendance_time"],"%Y-%m-%d %H:%M:%S")
                elaspedSeconds=(datetime.now()-datetimeObject).total_seconds()
                if elaspedSeconds>30:
                    ref=db.reference(f"Students/{id}")
                    studentInfo["total_attendance"]+=1
                    ref.child("total_attendance").set(studentInfo["total_attendance"])
                    ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeCounter=1
                    counter=0
                    backImage[44:44+633,808:808+414]=modeList[modeCounter]
            # Only displays details if student is not already marked
            if modeCounter!=1:
                if 10<counter<20:
                    modeCounter=3
                    
                backImage[44:44+633,808:808+414]=modeList[modeCounter]
                if counter<=10:    
                    cv.putText(backImage,str(studentInfo["total_attendance"]),(861,125),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255))
                        
                    cv.putText(backImage,str(studentInfo["course"]),(1006,550),cv.FONT_HERSHEY_COMPLEX_SMALL,0.7,(255,255,255))    
                    cv.putText(backImage,str(id),(1006,493),cv.FONT_HERSHEY_COMPLEX_SMALL,0.7,(255,255,255))
                    cv.putText(backImage,str(studentInfo["grade"]),(910,625),cv.FONT_HERSHEY_COMPLEX,0.6,(100,100,100))
                    cv.putText(backImage,str(studentInfo["year"]),(1025,625),cv.FONT_HERSHEY_COMPLEX,0.6,(100,100,100))
                    cv.putText(backImage,str(studentInfo["start_year"]),(1125,625),cv.FONT_HERSHEY_COMPLEX,0.6,(100,100,100.6))
                    (w,h),_=cv.getTextSize(studentInfo["name"],cv.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv.putText(backImage,str(studentInfo["name"]),(808+offset,445),cv.FONT_HERSHEY_COMPLEX,1,(50,50,50))    
                    backImage[175:175+216,909:909+216]=studentImage
                counter+=1
            
            #If above one wrong frame (extra frame)
                if counter>=20:
                    counter=0
                    modeCounter=0
                    studentInfo=[]
                    studentImage=[]
                    backImage[44:44+633,808:808+414]=modeList[modeCounter]

    #If no face in frame show active
    else:
        modeCounter=0
        counter=0               
        
    
    cv.imshow("Attendance Portal",backImage)
    cv.waitKey(1)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
