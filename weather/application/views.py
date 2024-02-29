from django.shortcuts import render, HttpResponse
def application(request):
   return render(request, "home.html")