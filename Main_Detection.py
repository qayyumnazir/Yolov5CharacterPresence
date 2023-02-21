import streamlit as st
import torch
from detect import detect
from io import *
import os
import wget
import time
import moviepy.editor as moviepy
import requests
from detect import detect
import pandas as pd
import streamlit_authenticator as stauth
from moviepy.editor import *
import pytube
import database as db
from pytube import YouTube
import hydralit_components as hc
global usernamez
newdata=[]
#skvideo.setFFmpegPath('C:\ProgramData\Anaconda3\Lib\site-packages\skvideo\io')

## CFG
cfg_model_path = "data\yvn500medhyp.pt" 

cfg_enable_url_download = False
if cfg_enable_url_download:
    url = "https://archive.org/download/yoloTrained/yoloTrained.pt" #Configure this if you set cfg_enable_url_download to True
    cfg_model_path = f"models/{url.split('/')[-1:]}" #config model path from url name



def playvideo(source):
    video_file = open(source, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

def playvideo2(source):
    clip = moviepy.VideoFileClip(source)
    clip.write_videofile("data/video_output/result.mp4", codec="libx264")
    st_video = open("data/video_output/result.mp4", 'rb')
    video_bytes = st_video.read()
    st.video(video_bytes)
    #st.write("Model Prediction")
    return clip

def getvideo(source):
    clip = moviepy.VideoFileClip(source)
    return clip
def print_res(result,test_keys):
    test_keys=test_keys
    res={}
    temp_array = []
    for names_index in range(len(test_keys)):
        for arrays in result:
            #print(arrays[names_index])
            temp_array.append(int(float(arrays[names_index])))
    
        res[test_keys[names_index]] = temp_array
        temp_array=[]
    
    x1=['Q1','Q2','Q3','Q4']
    df = pd.DataFrame(res) 
    df.index = ["Quartile 1 Percentage","Quartile 2 Percentage","Quartile 3 Percentage","Quartile 4 Percentage"]
    #st.write(df)
    #df = df.rename(columns={'date':'index'}).set_index('index')

    st.table(df)
    st.line_chart(df)
    #st.bar_chart(df, y=df.keys,x=df.values)
    #print(res)


    pass
def CreateLineData(dataz):
    # opening the file in read mode
    my_file = open(dataz, "r")
  
    # reading the file
    data = my_file.read()  
    # replacing end splitting the text 
    # when newline ('\n') is seen.
    data_into_list = data.split("\n")
    data_into_list.pop()
    my_file.close()
    return data_into_list

def getN(filename):
    with open(filename) as f:
        for line in f:
            pass
        last_line = line
    return len(line[7:].split(" , "))

    

def getCharData():
    return CreateLineData("name.txt")
def getQuarData():
    return newdata

def toTextFile(textfile,data):
    with open(textfile, "w") as txt_file:
        for line in data:
            txt_file.write(" ".join(line) + "\n") # works with any number of elements in a line

def savefile(value):
    pass

def LinkHelper(link):
    yt = pytube.YouTube(link) 
    try: 
        # object creation using YouTube
        # which was imported in the beginning 
            yt = pytube.YouTube(link) 
    except: 
            st.error("Connection Error")
        
    mp4files = yt.filter('mp4')
    yt.set_filename('utubetemp')
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)

    try:
            d_video.download( os.path.join('data/uploads',yt.filename))
        
    except:
            print("Extract Error!")
        
    st.write('Task Completed!')


def LinkToVid(fps,device):
                    imgpath = 'data/uploads/tempUtube.mp4'
                    outputpath = os.path.join('data/video_output/temp2.mp4')
                    st.write("Uploaded Video")
                    playvideo(imgpath)
                    dur= getvideo(imgpath).duration
                    st.write("Please choose you prefered cut for the video")
                                
                    start = st.number_input('Please enter starting time :',min_value=0,max_value=int(dur))
                    end = st.number_input("Please enter ending time :",min_value=0,max_value=int(dur))
                    if st.button("Confirm"):

                        with hc.HyLoader('Processing Video',hc.Loaders.standard_loaders):
                            clip = VideoFileClip(imgpath)
                            clip= clip.subclip(start,end)
                            duration = clip.duration
                            clip = clip.set_fps(int(fps))
                            q1_dur= clip.subclip(0,duration*(1/4))
                            q2_dur= clip.subclip(duration*(1/4),duration*(2/4))
                            q3_dur= clip.subclip(duration*(2/4),duration*(3/4))
                            q4_dur= clip.subclip(duration*(3/4),duration)
                            bruh = [q1_dur,q2_dur,q3_dur,q4_dur]
                            newdata=[]
                            temp_count=1
                        with hc.HyLoader('Running Detection',hc.Loaders.standard_loaders):
                            for breh in bruh:
                                breh.write_videofile("temp2.mp4")
                                N=getN("data//data.yaml")
                                detect(weights=cfg_model_path, source='temp2.mp4', device=0, data= "data/data.yaml",max_det=N) if device == 'cuda' else detect(weights=cfg_model_path, source='temp2.mp4', device='cpu',max_det=N)
                                st.write("Quartile ",str(temp_count))
                                playvideo2(outputpath)
                                newdata.append(CreateLineData("receipt.txt"))
                                temp_count=temp_count+1
                                
                        print(newdata)
                        print(print_res(newdata,getCharData()))
                        toTextFile("datatemp.txt",newdata)

def LinkInput(device, src, fps =30):
    link = st.text_input("Please enter the link",key="Enter Link")
       
    if link:
        try: yt = YouTube(link) 
        except: 
            st.error("The link causes error, make sure the added link is correct.")
       
    try:
        with hc.HyLoader('Downloading Video',hc.Loaders.standard_loaders):
            yt.streams.filter(progressive = True, 
            file_extension = "mp4").first().download(output_path = "data\\uploads",
            filename = "tempUtube.mp4")
        LinkToVid(fps,device)
            

    except:

        st.warning("Please Enter The Proper YouTube Link")


            
            



def videoInput(device, src , fps=30):

    uploaded_video = st.file_uploader("Upload Video", type=['mp4', 'mov', 'png', 'jpg'])
    if uploaded_video != None:
        
        if uploaded_video.name[len(uploaded_video.name)-3:] != 'png' and uploaded_video.name[len(uploaded_video.name)-3:] != 'jpg':

            imgpath = os.path.join('data/uploads',uploaded_video.name)
            outputpath = os.path.join('data/video_output/temp2.mp4')
            with open(imgpath, mode='wb') as f:
                f.write(uploaded_video.read())  # save video to disk
            st.write("Uploaded Video")
            playvideo(imgpath)
            dur= getvideo(imgpath).duration
            st.write("Please choose you prefered cut for the video")

            start = st.number_input('Please enter starting time :',min_value=0,max_value=int(dur))
            end = st.number_input("Please enter ending time :",min_value=0,max_value=int(dur))
            if st.button("Confirm"):

                with hc.HyLoader('Processing Video',hc.Loaders.standard_loaders):
                    clip = VideoFileClip(imgpath)
                    clip= clip.subclip(start,end)
                    duration = clip.duration
                    clip = clip.set_fps(int(fps))
                    q1_dur= clip.subclip(0,duration*(1/4))
                    q2_dur= clip.subclip(duration*(1/4),duration*(2/4))
                    q3_dur= clip.subclip(duration*(2/4),duration*(3/4))
                    q4_dur= clip.subclip(duration*(3/4),duration)
                    bruh = [q1_dur,q2_dur,q3_dur,q4_dur]
                    newdata=[]
                    temp_count=1
                with hc.HyLoader('Running Detection',hc.Loaders.standard_loaders):
                    for breh in bruh:
                        breh.write_videofile("temp2.mp4")
                        N=getN("data//data.yaml")
                        detect(weights=cfg_model_path, source='temp2.mp4', device=0, data= "data/data.yaml",max_det=N) if device == 'cuda' else detect(weights=cfg_model_path, source='temp2.mp4', device='cpu',max_det=N)
                        st.write("Quartile ",str(temp_count))
                        playvideo2(outputpath)
                        newdata.append(CreateLineData("receipt.txt"))
                        temp_count=temp_count+1
                
                print(newdata)
                print(print_res(newdata,getCharData()))
                toTextFile("datatemp.txt",newdata)
                
                #os.remove(imgpath)

                


            
        else:
           imgpath = os.path.join('data/uploads',uploaded_video.name)
           with open(imgpath, mode='wb') as f:
                f.write(uploaded_video.read())
           outputpath = os.path.join('data/video_output',uploaded_video.name)
           detect(weights=cfg_model_path, source=imgpath, device=0, data= "data/data.yaml",max_det=3) if device == 'cuda' else detect(weights=cfg_model_path, source=imgpath, device='cpu',max_det=3)
           st.image(outputpath)
           #os.remove(imgpath)


        
    
#def imgInput(device, src):



def main():


    # -- Sidebar
    st.sidebar.title('⚙️Options')
    datasrc = st.sidebar.radio("Select input source.", ['Upload your own data.', 'From Youtube links.'])
    efpees = st.sidebar.radio("Select preferred FPS.", ['30','15','5','1'])
    
    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = True, index=0)
    # -- End of Sidebar

    st.header('Cartoon Character Object Detections')
    st.subheader('👈🏽 Select options left-haned menu bar.')
    st.sidebar.markdown("-")
    if datasrc == "From Youtube links.":    
        LinkInput(deviceoption, datasrc)
    elif datasrc == "Upload your own data.": 
        videoInput(deviceoption, datasrc, efpees)



    

if __name__ == '__main__':
     users = db.fetch_all_users()

     usernames = [user["key"] for user in users]
     names = [user["name"] for user in users]
     hashed_passwords = [user["password"] for user in users]
     authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=30)
     name, authentication_status, username = authenticator.login("Login", "main")
     print(usernames,name,hashed_passwords)
    


     if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar')
        usernamez=username
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Didi And Friends Detections')
        main()
     elif st.session_state["authentication_status"] == False:
         st.error('Username/password is incorrect')
     elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')

  
    

# Downlaod Model from url.    
@st.cache
def loadModel():
    start_dl = time.time()
    model_file = wget.download(url, out="models/")
    finished_dl = time.time()
    print(f"Model Downloaded, ETA:{finished_dl-start_dl}")
    if cfg_enable_url_download:
        loadModel()