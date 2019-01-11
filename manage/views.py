from django.shortcuts import render

def manage(request):
    return(render(request, 'manage.html', locals()))