from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from pytube import YouTube
import requests

# Create your views here.
def homePage(request):
    return render(request,'app/html/index.html')

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def detailsFunction(request):
    if request.is_ajax:
        url = request.POST.get('url')
        request = requests.get(url)
        if 'youtube.com' in url or 'youtu.be' in url:
            if request.status_code == 200:
                if "Video unavailable" not in request.text:      
                    yt = YouTube(url)
                    print("Title :", yt.title)
                    # To get number of views
                    print("Views :", yt.views)
                    # To get the length of video
                    print("Duration :", yt.length)
                    # To get description
                    print("Description :", yt.description)
                    # To get ratings
                    print("Ratings :", yt.rating)
                    url_code=''
                    if '=' in url:
                        url_code = url.split('=')[1]
                    else:
                        url_code = url.split('/')[3]
                    data = {
                        'status':200,
                        'title': yt.title,
                        'views': yt.views,
                        'duration':convert(yt.length),
                        'desc':yt.description,
                        'rating':yt.rating,
                        'url_code':url_code,
                        'url':url
                    }
        #             # stream = yt.streams.get_highest_resolution()
        #             # stream.download()
        #             # print("Download completed!!")
        #             # print(url)
                    return JsonResponse(data)
                else:
                    return JsonResponse({'status':201,'value':'Video not available'})
            else:
                return JsonResponse({'status':201,'value':'Video not available'})
        else:
            return JsonResponse({'status':201,'value':'Pest Correct Youtube URL'})

def downloadFunction(request):
    if request.is_ajax:
        url = request.GET['url']
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        return JsonResponse({'status':'Download completed!!'})
    else:
        return JsonResponse({'status':'Download Failed'})