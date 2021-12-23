from django.shortcuts import render, redirect
from pytube import YouTube
import os
from django.http import FileResponse


# Create your views here.
def index(request):
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads/"

    if request.method == 'POST':
        link = request.POST.get("youtubeLink")
        downloadAudio = request.POST.get("downloadAudio")
        downloadVideo = request.POST.get("downloadVideo")
        audioQuality = request.POST.get("AudioQuality")
        videoQuality = request.POST.get("VideoQuality")

        if link:
            yt = YouTube(link)
            title = yt.title
            thumbnail = yt.thumbnail_url

            audio = []
            audio_size = []
            video = []
            video_size = []
            for i in yt.streams.filter(only_audio=True):
                print(i)
                audio.append(i.abr)
                size = i.filesize / (1024 * 1024)
                size = round(size, 2)
                audio_size.append(size)
            for j in yt.streams.filter(only_video=True, mime_type="video/mp4"):
                video.append(j.resolution)
                size = j.filesize / (1024 * 1024)
                size = round(size, 2)
                video_size.append(size)
            audio.sort()
            video = list(set(video))
            video.sort()
            return render(request, 'index.html', {
                'thumbnail': thumbnail,
                'title': title,
                'audio': zip(audio, audio_size),
                'video': zip(video, video_size),
                'link': link,
            })
        elif downloadAudio:
            if audioQuality != "Audio Quality" and downloadAudio is not None:
                yt = YouTube(downloadAudio)
                yt = yt.streams.filter(abr=audioQuality)
                return FileResponse(open(yt.first().download(), 'rb'))
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
                return FileResponse(open(yt.first().download(), 'rb'))
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
