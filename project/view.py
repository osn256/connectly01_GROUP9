from getpass import getuser
from django.shortcuts import render

def profileView(request):
    user = getuser()
    return render(request, 'profile.html', {'user': user})