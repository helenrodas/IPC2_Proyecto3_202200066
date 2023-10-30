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
        data = request.POST.get("data")
        fechainicio = request.POST.get("fechainicio")
        fechafinal = request.POST.get("fechafinal")
        url  = request.POST.get("url")

        if not data:
            return JsonResponse({"message": "No se ha seleccionado rango de fechas."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            # files = {"file": (file.name, file.read())}
            response = requests.post("http://127.0.0.1:5000/hashtags", data={"data": data, "fechainicio": fechainicio,"fechafinal":fechafinal})
            response.raise_for_status()

            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            print(response_data)
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
    return render(request, 'hashtags.html')

def consultaMenciones(request):
    if request.method == 'POST':
        data = request.POST.get("data")
        fechainicio = request.POST.get("fechainicio")
        fechafinal = request.POST.get("fechafinal")
        url  = request.POST.get("url")

        if not data:
            return JsonResponse({"message": "No se ha seleccionado rango de fechas."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            # files = {"file": (file.name, file.read())}
            response = requests.post("http://127.0.0.1:5000/menciones", data={"data": data, "fechainicio": fechainicio,"fechafinal":fechafinal})
            response.raise_for_status()

            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            print(response_data)
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
    return render(request, 'menciones.html')

def consultaSentimientos(request):
    if request.method == 'POST':
        data = request.POST.get("data")
        fechainicio = request.POST.get("fechainicio")
        fechafinal = request.POST.get("fechafinal")
        url  = request.POST.get("url")

        if not data:
            return JsonResponse({"message": "No se ha seleccionado rango de fechas."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            # files = {"file": (file.name, file.read())}
            response = requests.post("http://127.0.0.1:5000/consulta_sentimientos", data={"data": data, "fechainicio": fechainicio,"fechafinal":fechafinal})
            response.raise_for_status()

            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            print(response_data)
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
    return render(request, 'sentimientos.html')

def ayuda(request):
    
    return render(request, 'ayuda.html')
