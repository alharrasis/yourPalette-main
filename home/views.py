from django.shortcuts import render
from .script.main import skinUnderTone, fileNameExtract
from django.http import HttpResponse, JsonResponse

# Create your views here.
def detailView(request):
    context = {

    }
    return render(request, "you.html", context=context)
def homeView(request):

    context = {

    }
    
    return render(request, "home.html", context=context)


def uploadView(request):
    if request.method == 'POST':
        print("POSTED")
        # print(request.POST)
        filename = 'home/static/uploaded.jpg' 
        try:
            data = request.POST["file"]
            import base64
            data = data[len("data:image/png;base64"):]
            imgdata = base64.b64decode(data) 
            filename = 'home/static/uploaded.jpg' 
            with open(filename, 'wb') as f:
                f.write(imgdata)
                print("file saved")
        except:
            passedFiles = request.FILES.get('file')
            print(request)
            print(passedFiles)
            filePath = f'home/static/uploaded.jpg'
            with open(filePath, 'wb+') as destination:
                for chunk in passedFiles.chunks():
                    destination.write(chunk)
        
        result, faceFount = skinUnderTone(filename, 'home/static/debug.jpg')
        print(result, faceFount)
        if faceFount: 
            displayImg = "home/static/userview.jpg"
        else:
            displayImg = "home/static/userview.jpg"

        # code:
        # -1, no skin detected
        # 0, cool tone
        # 1, neutral tone
        # 2, warm tone
        hasSkin = True
        foundation = None
        if result == 0:
            foundation = "Cool"
            foundation = "Cool"
            plts = [
                "#FFC5DE",
                "#F8A2AA",
                "#E3237B",
                "#A92D7B",
                "#89112C",
                "#6B0F34",
            ]
        elif result == 1:
            foundation = "Neutral"
            plts = [
                "#FFC5DE",
                "#F8A2AA",
                "#E3237B",
                "#A92D7B",
                "#89112C",
                "#6B0F34",
                "#FECBC8",
                "#FCA590",
                "#DE4C30",
                "#D62C1D",
                "#A10314",
                "#8E131D",
            ]
        elif result == 2:
            foundation = "Warm"
            plts = [
                "#FECBC8",
                "#FCA590",
                "#DE4C30",
                "#D62C1D",
                "#A10314",
                "#8E131D",
            ]
        else:
            hasSkin = False
            foundation = "No Skin Detected"
            plts =[]


    context = {
        "displayImg": displayImg,
        "foundation": foundation,
        "hasSkin": hasSkin,
        "result": result,
        "fileName": fileNameExtract(displayImg),
        "color": "#F0A1FB",
        "plts": plts,
        
    }
    
    response = HttpResponse()
    response['displayImg'] = displayImg
    response['foundation'] = foundation
    response['hasSkin'] = hasSkin
    return JsonResponse(context)