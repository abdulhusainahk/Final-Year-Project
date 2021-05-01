from django.shortcuts import render


def home(request):
    if request.method == "POST":
        print(request.POST)
        return render(request, "home.html")
    else:
        return render(request, "home.html")
    return
