from tkinter import messagebox

import camera as camera
import cv2
import os
import sys
from IPython.terminal.pt_inputhooks import tk
from imutils.video import VideoStream
import time
import imutils
from imutils import paths
import argparse
import pymysql
from tkinter import *
import pickle
import numpy as np

data_path = "E:/opencv-face-recognition_advanced/opencv-face-recognition_advanced/dataset"
db = pymysql.connect("localhost", "root", "", "facePro")
cursor = db.cursor()


def Embedding():
    os.system(
        'cmd /k "python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7"')


def Train():
    os.system(
        'cmd /k "python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle"')


def Mark():
    os.system(
        'cmd/k "python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle"')


def Empldatabase(eid, ename, employeeregister):
    print(str(eid))
    print(ename)
    # vs = VideoStream(src=0).start()
    # time.sleep(2.0)
    camera = cv2.VideoCapture(0)
    i = 0
    try:
        cursor.execute("INSERT INTO `employeedetails`(`EID`, `name`) VALUES (%s,%s)", (str(eid), str(ename)))
        # Get a list of all records
        print("Data insertion success!!!")
        # Submit to database for execution
        db.commit()
        db.close()
    except Exception as e:
        print(e)
        db.close()
    if not os.path.exists(os.path.join(data_path, str(eid), str(ename))):
        os.makedirs(os.path.join(data_path, str(eid), str(ename)))
        # vs = VideoStream(src=0).start()
        # time.sleep(2.0)
    while i < 10:
        # frame = vs.read()
        input('Press Enter to capture')

        return_value, image = camera.read()
        cv2.imwrite(os.path.join(data_path, str(eid), 'Train' + str(i) + '.png'), image)
        i += 1
        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF
        # cv2.imshow(image)
    del (camera)
    # cv2.destroyAllWindows()
    # vs.stop()

def employeRegister():
    employeeregister = Tk()
    employeeregister.title('Employee Registration')
    employeeregister.config(bg='DarkSlateGray')
    employeeregister.geometry('600x600')
    employeeregister.resizable(0, 0)
    appName1 = Label(employeeregister, text='Employee registration', bg='black', fg='cyan', font=('arial', 25))
    appName1.pack(side=TOP, fill=BOTH)
    usernamelabel = Label(employeeregister, text="Enter Employee ID", font=('impact', 10))
    usernamelabel.place(x=10, y=72)
    Eid = Entry(employeeregister, fg='blue', bd=3, width=40)
    Eid.place(x=170, y=70)
    usernamelabel2 = Label(employeeregister, text="Enter Employee Name", font=('impact', 10))
    usernamelabel2.place(x=10, y=100)
    Ename = Entry(employeeregister, fg='blue', bd=3, width=40)
    Ename.place(x=170, y=100)
    button1 = Button(employeeregister, text='Take Image', bg='green', fg='white', activebackground='blue', width=15,
                     activeforeground='yellow', command=lambda: Empldatabase(Eid.get(), Ename.get(), employeeregister))
    button1.place(x=30, y=200)
    button2 = Button(employeeregister, text='Embedding', bg='green', fg='white', activebackground='blue', width=15,
                     activeforeground='yellow', command=Embedding)
    button2.place(x=180, y=200)
    button2 = Button(employeeregister, text='Train', bg='green', fg='white', activebackground='blue', width=15,
                     activeforeground='yellow', command=Train)
    button2.place(x=340, y=200)
    employeeregister.mainloop()


def OnClick(Adminid, Adminname, root):
    Aid = Adminid
    Ausername = Adminname
    cursor.execute("select * from Admin ")
    # Get a list of all records
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        if (id == Aid and name == Ausername):
            print("LoginSuccess", "You are login succesfully")
            root.destroy()
            employeRegister()
        db.commit()
    else:
        # messagebox.showinfo("error")
        db.close()


def AdminLogin():
    window.destroy()
    root = Tk()
    root.geometry('520x550')
    root.config(bg='DarkSlateGray')
    appName = Label(root, text='Admin Login Page', bg='black', fg='cyan', font=('arial', 25))
    appName.pack(side=TOP, fill=BOTH)
    usernamelabel = Label(root, text="Enter Admin ID", font=('impact', 10))
    usernamelabel.place(x=10, y=72)
    Adminid = Entry(root, fg='blue', bd=3, width=40)
    Adminid.place(x=170, y=70)
    usernamelabel2 = Label(root, text="Enter Admin Name", font=('impact', 10))
    usernamelabel2.place(x=10, y=100)
    Adminname = Entry(root, fg='blue', bd=3, width=40)
    Adminname.place(x=170, y=100)
    runloginbutton = Button(root, text='Login', bg='green', fg='white', activebackground='blue', width=30,
                            activeforeground='yellow', command=lambda: OnClick(Adminid.get(), Adminname.get(), root))
    runloginbutton.place(x=180, y=130)
    root.mainloop()


def Rules():
    window.destroy()
    Rules = Tk()
    Rules.title('Face Recognition System')
    Rules.config(bg='DarkSlateGray')
    Rules.geometry('600x600')
    Rules.resizable(0, 0)
    appName1 = Label(Rules, text='Rules', bg='black', fg='cyan', font=('arial', 25))
    appName1.pack(side=TOP, fill=BOTH)
    usernamelabel = Label(Rules, text="1)Only Admin Can Register Others", font=('impact', 10))
    usernamelabel.place(x=10, y=72)
    usernamelabe2 = Label(Rules, text="2)User Cant stay Dark Places", font=('impact', 10))
    usernamelabe2.place(x=10, y=132)
    usernamelabe3 = Label(Rules, text="3)Admin has to provide employee's username and id before register to the system",
                          font=('impact', 10))
    usernamelabe3.place(x=10, y=182)
    Back = Button(Rules, text='Back', bg='green', fg='white', activebackground='blue', width=20,
                  activeforeground='yellow', command=window)
    Back.place(x=10, y=300)


window = Tk()
window.title('Home')
window.config(bg='DarkSlateGray')
window.geometry('600x600')
window.resizable(0, 0)
appName1 = Label(window, text='Face Recognition Attendance System', bg='black', fg='cyan', font=('arial', 25))
appName1.pack(side=TOP, fill=BOTH)
welcome = Label(window, text="WELCOME TO THE NSBM GREEN UNIVERSITY", font=('Franklin Gothic Medium', 18))
welcome.place(x=70, y=92)
loginbutton = Button(window, text='Register',font=('Franklin Gothic Medium', 20), bg='DarkOliveGreen', fg='white', activebackground='blue', width=20,
                     activeforeground='yellow', command=AdminLogin)
loginbutton.place(x=160, y=200)
loginbutton2 = Button(window, text='Mark Attendance',font=('Franklin Gothic Medium', 20), bg='DarkOliveGreen', fg='white', activebackground='blue', width=20,
                      activeforeground='yellow', command=Mark)
loginbutton2.place(x=160, y=300)
loginbutton3 = Button(window, text='Rules', bg='DarkOliveGreen',font=('Franklin Gothic Medium', 20), fg='white', activebackground='blue', width=20,
                      activeforeground='yellow', command=Rules)
loginbutton3.place(x=160, y=400)
window.mainloop()
