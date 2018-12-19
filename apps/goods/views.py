from django.shortcuts import render

# Create your views here.
def index(request):
    '''shouye '''
    return render(request,'index.html')