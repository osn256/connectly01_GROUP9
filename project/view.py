from getpass import getuser
from django.shortcuts import render

def profileView(request):
    users = getuser()
    return render(request, 'profile.html', {'user': users})