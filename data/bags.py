
from pytube import YouTube

link = "https://www.youtube.com/watch?v=w9TcErzdoTg"

yt = YouTube(link)  

try:
    yt.streams.filter(progressive = True, 
file_extension = "mp4").first().download(output_path = "C:\\Users\\qayyu\\Desktop\\Fzzy",
filename = "Kontol.mp4")
except:
    print("The Link is unavailable")
print('Task Completed!')