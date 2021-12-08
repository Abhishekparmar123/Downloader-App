from django.shortcuts import render, redirect
from pytube import YouTube
import os


# Create your views here.
def index(request):
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads/"
    print("outside loop")
    if request.method == 'POST':
        link = request.POST.get("youtubeLink")
        downloadAudio = request.POST.get("downloadAudio")
        downloadVideo = request.POST.get("downloadVideo")
        audioQuality = request.POST.get("AudioQuality")
        videoQuality = request.POST.get("VideoQuality")
        print("hello")
        print(audioQuality, videoQuality)
        print(downloadAudio, downloadVideo)
        print("link "+str(link))
        if link:
            yt = YouTube(link)
            title = yt.title
            thumbnail = yt.thumbnail_url

            audio = []
            video = []
            for i in yt.streams.filter(only_audio=True):
                print(i)
                audio.append(i.abr)
            print("video ")

            for j in yt.streams.filter(only_video=True, mime_type="video/mp4"):
                print(j)
                video.append(j.resolution)

            audio.sort()
            video = list(set(video))
            video.sort()
            print(audio, video)
            print(thumbnail)
            return render(request, 'index.html', {
                'thumbnail': thumbnail,
                'title': title,
                'audio': audio,
                'video': video,
                'link': link,
            })
        elif downloadAudio:
            if audioQuality != "Audio Quality" and downloadAudio is not None:
                print("Download")
                yt = YouTube(downloadAudio)
                yt = yt.streams.filter(abr=audioQuality)
                yt.first().download(dirs)
                return render(request, 'index.html', {
                    'message': "Downloaded ..... ",
                })
            else:
                print("select audio quality")
                return render(request, 'index.html', {
                    'error': "Choose Audio Quality",
                })
        elif downloadVideo:
            if videoQuality != "Video Quality" and downloadVideo is not None:
                print("Download")
                yt = YouTube(downloadVideo)
                yt = yt.streams.filter(res=videoQuality, mime_type="video/mp4")
                yt.first().download(dirs)
                print("select video quality")
                return render(request, 'index.html', {
                    'message': "Downloaded ..... ",
                })
            else:
                print("select video quality")
                return render(request, 'index.html', {
                    'error': "Choose Video Quality",
                })
        else:
            return render(request, 'index.html', {
                'error': "Enter a correct URL",
            })
    return render(request, 'index.html')
