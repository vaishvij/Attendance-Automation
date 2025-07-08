import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2 as cv
import os

cred = credentials.Certificate("Enter path of your private key here")
firebase_admin.initialize_app(cred,{"databaseURL":"Enter path of your realtime Database here","storageBucket":"Enter path of your storage bucket here"})

ref=db.reference("Students")

data={"234890":{"name":"Andrew Ng","course":"B.Tech CSE","start_year":2020,"total_attendance":41,"grade":"A+","year":4,"last_attendance_time":"2024-01-10 00:54:34"},
      "852741":{"name":"Bill Gates","course":"B.Tech IT","start_year":2020,"total_attendance":45,"grade":"B+","year":4,"last_attendance_time":"2024-01-10 00:54:34"},
      "963852":{"name":"Elon Musk","course":"B.Tech Mechanical","start_year":2021,"total_attendance":67,"grade":"C","year":3,"last_attendance_time":"2024-01-10 00:54:34"},
      "2201456":{"name":"Daniel Radcliffe","course":"BBA","start_year":2023,"total_attendance":70,"grade":"B","year":1,"last_attendance_time":"2024-01-10 00:54:34"},
      "22021654":{"name":"Satya Nadela","course":"MBA","start_year":2023,"total_attendance":99,"grade":"A","year":1,"last_attendance_time":"2024-01-10 00:54:34"},
      "2202998":{"name":"Drew Scott","course":"BCA","start_year":2023,"total_attendance":99,"grade":"A","year":1,"last_attendance_time":"2024-01-10 00:54:34"},
      "2202999":{"name":"Jonathan Scott","course":"BCA","start_year":2023,"total_attendance":99,"grade":"A","year":1,"last_attendance_time":"2024-01-10 00:54:34"},
      "22021782":{"name":"Larry Page","course":"B.Tech ECE","start_year":2022,"total_attendance":84,"grade":"A+","year":2,"last_attendance_time":"2024-01-10 00:54:34"},
      "220211769":{"name":"Sundar Pichai","course":"M.B.A","start_year":2021,"total_attendance":67,"grade":"C","year":3,"last_attendance_time":"2024-01-10 00:54:34"},
      "220211775":{"name":"Jim Carrey","course":"B.Tech CSE","start_year":2022,"total_attendance":100,"grade":"A+","year":2,"last_attendance_time":"2024-01-10 00:54:34"},
      "220211774":{"name":"Barack Obama","course":"L.L.B","start_year":2022,"total_attendance":71,"grade":"B+","year":2,"last_attendance_time":"2024-01-10 00:54:34"},
      "2201133567":{"name":"Hideo Kojima","course":"Game Dev","start_year":2023,"total_attendance":155,"grade":"A+","year":1,"last_attendance_time":"2024-01-10 00:54:34"},
      "2202116654":{"name":"Amitabh Bachan","course":"L.L.M","start_year":2023,"total_attendance":81,"grade":"B+","year":1,"last_attendance_time":"2024-01-10 00:54:34"}
    
    }

#Add images to database
imagesPath="Images"
imgPathList=os.listdir(imagesPath)
imgList=[]
studentId=[]

for path in imgPathList:
    file3=f"{imagesPath}/{path}"
    bucket=storage.bucket()
    blob=bucket.blob(file3)
    blob.upload_from_filename(file3)

for key,value in data.items():
    ref.child(key).set(value)       #Sending data to a directory of key and data sended is value 
    