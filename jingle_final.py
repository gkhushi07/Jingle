#importing packages
from dotenv import load_dotenv
import os
import smtplib
import speech_recognition as sr
import pyttsx3 
from email.message import EmailMessage
from tkinter import *
from tkinter import ttk
from datetime import datetime
import mysql.connector as msl

#global variables
s=''
name=''
reciever=''
subject=''
ms_tm=''

#creating objects of diff modules
TTS=pyttsx3.init() #for text to speech conversion
STT=sr.Recognizer() #for speech recognition
win= Tk() #for GUI


#function where bot speaks given text
def botSpeaks(Audio):
    TTS.setProperty("rate",200)
    TTS.say(Audio)
    TTS.runAndWait()

#fucntion to recognize user's voice 
def userSpeaks():
    try:
        with sr.Microphone() as source:
            print("Listening")
            s="Listening"
            STT.pause_threshold=1
            STT.energy_threshold=1500
            hear=STT.listen(source)
            info=STT.recognize_google(hear)
            print(info)
            return info
    except Exception as e:
            print(e)
            print("Try Again...Not Recognisable")
            #m1=Label(win,text="Try Again...Not Recognisable",font='terminal',fg='gold',bg='black').grid(row=3,column=2,padx=10,pady=10)
            return "None"

#function to create and add data in database
def db_get(name,reciever,subject,ms_tm):
    nm=name
    eid=reciever
    sub=subject
    mess_timing=ms_tm

    obj=msl.connect(host='localhost',password='123456789',user='root',database='jingle')
    
    cursor=obj.cursor()
    cursor.execute('create table if not exists tableX(name varchar(30),e_id varchar(30),subject varchar (100),time datetime)')
    cursor.execute('insert into tableX values(%s,%s,%s,%s)',(nm,eid,sub,mess_timing))
    obj.commit()
    cursor.execute('select * from tableX')
    print("inserted")
    for i in cursor:
        print(i)

#function that sends mail to recipient acc to info given
def sendMail(name,reciever,subject,message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    myemail='spare.ac.2702@gmail.com'
    password= os.getenv("HOST_EMAIL_PASSWORD")
    server.login(user=myemail,password=password)
    mail=EmailMessage()
    mail['From']='spare.ac.2702@gmail.com'
    mail['To']= reciever
    mail['Subject']=subject
    mail.set_content(message)
    server.send_message(mail)
    now=datetime.now()
    ms_tm=now.strftime('%y-%m-%d %H:%M:%S')
    print("Message sent at:",ms_tm)
    m3=Label(win,text="Message Sent!",font='terminal',fg='gold',bg='black').grid(row=5,column=2,padx=10,pady=10)
    db_get(name,reciever,subject,ms_tm)

#dictionary acting as contact list
nicknames={'Khushi': 'gkhushiask6@gmail.com',
        'Shivangi': 'shivangiyadav20bca051@gmail.com',
            'Shristi': 'shrishtipal20bca052@gmail.com',
            'Garima': 'GARIMASHUKHLA457@GMAIL.COM'
            }

#final bot method which ask for info from the user and send message to the desired recipient
def getInfo():
    botSpeaks('Speak the name or email address whom you want to send email')
    name=userSpeaks()
    if name in nicknames:
        reciever=nicknames[name]
        print(reciever)           
    else:
        reciever=input()

    botSpeaks("Speak the subject of your mail")
    subject=userSpeaks()

    botSpeaks('Speak the body of your mail')
    message=userSpeaks()

    sendMail(name,reciever,subject,message)
    
    botSpeaks("is there anything else I can do")
    reply=userSpeaks()
    if 'yes' in reply:
        getInfo()
    else:
        print('Thank You!')
        m2=Label(win,text="Thank You!",font='terminal',fg='gold',bg='black').grid(row=6,column=2,padx=10,pady=10)

#function creating database display window
def db():

    win=Tk()
    win.title('JINGLE DATA')
    win.geometry('1110x500')

    obj=msl.connect(host='localhost',password='123456789',user='root',database='jingle')
    print('connection established')

    cursor=obj.cursor()
    cursor.execute('SELECT * from tableX')

    tree=ttk.Treeview(win)
    tree['show']='headings'
    tree['columns']=('1','2','3','4')

    tree.column('1',width=100,minwidth=50,anchor=CENTER)
    tree.column('2',width=300,minwidth=50,anchor=CENTER)
    tree.column('3',width=500,minwidth=50,anchor=CENTER)
    tree.column('4',width=200,minwidth=50,anchor=CENTER)

    tree.heading("1",text="NAME",anchor=CENTER)
    tree.heading("2",text="EMAIL ID",anchor=CENTER)
    tree.heading("3",text="SUBJECT",anchor=CENTER)
    tree.heading("4",text="DATE",anchor=CENTER)

    i=0
    for row in cursor:
        tree.insert('',i,values=(row[0],row[1],row[2],row[3]))
        i=i+1
    tree.place(x=0,y=0)

    win.mainloop()

#GUI 
p=PhotoImage(file=r'assets\sym.png')
win.iconphoto(False,p)
win.title("JINGLE")

h=Label(win,text="Hi there! Click to begin :)",font='terminal',fg = 'gold', bg='black').grid(row=1,column=2,padx=10,pady=10)
b=Button(win,text='Click',font='terminal',fg='black',bg='gold',command=getInfo).grid(row=2,column=2,padx=10,pady=10)
pb=Button(win,text='Preview',font='terminal',fg='black',bg='gold',command=db).grid(row=3,column=2,padx=10,pady=10)

                    
win.configure(background='black')
win.geometry('350x320+900+350')

win.mainloop()

