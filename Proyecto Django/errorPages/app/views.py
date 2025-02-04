from django.shortcuts import render

from django.http import HttpResponse

from .utils import google_search

from django.http import JsonResponse
from .models import ErrorLog

# def index(request):
#    return HttpResponse("Hola Mundo")

def index(request):
    return render(request, 'index.html', status=200)

def show_error_404(request):
    return render(request,'404.html', status=404)

def show_error_500(request):
    return render(request,'500.html', status=500)

def generar_error(request):
    return 7/0

def onepage(request):
    return  render(request, 'onepage.html', status=200)

def buscar(request):
    query = request.GET.get('q','')
    results = []
    if query: # Si query tiene valor
        data = google_search(query)
        results = data.get("items", [])
    return render(
        request,
        'search.html',
        {'results': results, 'query': query}
    )

def error_logs(request):
    return render(request, 'error_logs.html')

def get_error_logs(request):
    errors = ErrorLog.objects.values('id', 'codigo', 'mensaje', 'fecha')
    return JsonResponse({'data': list(errors)})