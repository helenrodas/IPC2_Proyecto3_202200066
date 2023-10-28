import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



def cargarArchivos(request):
    if request.method == 'POST':
        data = request.POST.get("data")
        file = request.FILES.get("file")
        url  = request.POST.get("url")

        if not file:
            return JsonResponse({"message": "No se ha seleccionado un archivo."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            files = {"file": (file.name, file.read())}
            response = requests.post(url, data={"data": data}, files=files)
            response.raise_for_status()

            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'pagina.html')

def consultaHashtags(request):
    if request.method == 'POST':
        pass
    return render(request, 'hashtags.html')

def consultaMenciones(request):
    if request.method == 'POST':
        pass
    return render(request, 'menciones.html')

def consultaSentimientos(request):
    if request.method == 'POST':
        pass
    return render(request, 'sentimientos.html')

def ayuda(request):
    if request.method == 'POST':
        pass
    return render(request, 'ayuda.html')

# def get_response_from_flask(request):
#     try:
#         response = requests.get('http://127.0.0.1:5000/hashtags')
#         response.raise_for_status()
#         response_data = response.json()
#         return JsonResponse(response_data)
#     except requests.exceptions.RequestException as e:
#         return HttpResponse(str(e), status=500)
