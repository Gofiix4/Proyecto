from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Cadena aleatoria
import secrets
import string
#
from django.http import HttpResponse
from user_agents import parse
import user_agents 

import datetime
from datetime import datetime as fechaparte
# Create your views here.
from .models import Encuesta_calidad

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import requests
from pprint import pprint

from api.models import *

@method_decorator(login_required, name='dispatch')
class Home(APIView):
    template_name="index.html"
    def get(self,request):
        tareas = Tareas.objects.all()
        return render(request,self.template_name, {"tareas": tareas})
    def post(self,request):
        return render(request,self.template_name)

class Signup(APIView):
    template_name="signup.html"
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, self.template_name,{
                'form' : UserCreationForm
            })
    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            longitud = 10
            caracteres = string.ascii_letters + string.digits
            contra_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud))
            try:
                correo = User.objects.filter(email=request.POST['email'])
                if correo.exists():
                    return render(request, self.template_name, {
                        'form' : UserCreationForm,
                        "mensaje" : 'El email que ingresaste ya es utilizado por otra persona, prueba introduciendo otro'
                    })
                else:
                    # Aqui guarda en la base de datos
                    user = User.objects.create_user(first_name=request.POST['first_name'], email=request.POST['email'], last_name=request.POST['last_name'], username=request.POST['username'], password=contra_aleatoria) # Al final a password se le asigna el valor de contraseña aleatoria
                    # Guardas el usuario
                    user.save()
                    # Defines variables para que posteriormente las mandes por una mamada de link inverso xd a la clase que manda el correo
                    nombre = ' '
                    correo = request.POST['email']
                    apellido = ' '
                    usuario = request.POST['username']
                    asunto = 'Bienvenida'
                    detalles = ' '
                    # Igual aqui a contra le mandas el valor de la cadena generada automaticamente
                    contra = contra_aleatoria
                    # Aqui retorna a la clase de enviar correo
                    return redirect('enviar_correo', nombre=nombre, correo=correo, apellido=apellido, usuario=usuario, contra=contra, asunto=asunto, detalles=detalles)
                # Aqui te regresa al mismo formulario si es que el usuario que ingresaste ya existe
            except IntegrityError:
                return render(request, self.template_name, {
                    'form' : UserCreationForm,
                    "mensaje" : 'El usuario que ingresaste ya es utilizado por otra persona, prueba introduciendo otro'
                })
            except MultiValueDictKeyError:
                return render(request, self.template_name, {
                    'form': AuthenticationForm,
                    'mensaje': 'Alguno de los campos no han sido llenados de manera correcta, intentalo de nuevo'
                })

class Signin(APIView):
    template_name="signin.html"
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, self.template_name, {
                'form': AuthenticationForm
            })
    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            try:
                user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
                if user is None:
                    return render(request, self.template_name, {
                        'form': AuthenticationForm,
                        'error': 'Usuario o contraseña incorrecta'
                    })
                else:
                    login(request, user)
                    return redirect('/')
            except MultiValueDictKeyError:
                return render(request, self.template_name, {
                        'form': AuthenticationForm,
                        'error': 'Alguno de los campos no han sido llenados de manera correcta, intentalo de nuevo'
                    })
            except IntegrityError:
                return render(request, self.template_name, {
                    'form' : UserCreationForm,
                    "mensaje" : 'No se ha podido iniciar sesión de manera coorrecta, intentalo de nuevo'
                })
            
class Signout(APIView):
    def get(self,request):
        logout(request)
        return redirect('signin')

class Task(APIView):
    template_name="task.html"
    def get(self,request):
        status = Status.objects.all()
        prioridad = Prioridad.objects.all()
        return render(request,self.template_name, {'status': status, 'prioridad': prioridad})
    def post(self,request):
        Tstatus = Status.objects.all()
        Tprioridad = Prioridad.objects.all()
        if 'formAdd' in request.POST:
            try:
                titulo = request.POST.get('titulo')
                descripcion = request.POST.get('descripcion')
                fecha_inicio = request.POST.get('fecha_inicio')
                hora_inicio = request.POST.get('hora_inicio')
                fecha_hora_inicio = str(fecha_inicio + ' ' + hora_inicio)
                fecha_termino = request.POST.get('fecha_termino')
                hora_termino = request.POST.get('hora_termino')
                fecha_hora_termino = str(fecha_termino + ' ' + hora_termino)
                status = request.POST.get('status')
                prioridad = request.POST.get('prioridad')
                if request.user.is_authenticated:
                    id_usuario = request.user.id
                    usuario = User.objects.get(pk=id_usuario)
                    fkstatus = Status.objects.get(pk=status)
                    fkprioridad = Prioridad.objects.get(pk=prioridad)
                    registroTarea = Tareas(Titulo=titulo, Descripcion=descripcion, Fecha_inicio=fecha_hora_inicio, Fecha_termino=fecha_hora_termino, fk_Status=fkstatus, fk_Prioridad=fkprioridad, fk_Usuario=usuario)
                    registroTarea.save()
                    return render(request,self.template_name, {'mensaje': 'Tarea creada con exito!', "color" : 'lightgreen', 'status': Tstatus, 'prioridad': Tprioridad})
            except Exception as e:
                return render(request,self.template_name, {'mensaje': 'La tarea no se pudo crear' + str(e), "color" : 'red', 'status': Tstatus, 'prioridad': Tprioridad})

def enviar_correo(request, nombre, correo, apellido, usuario, contra, asunto, detalles):
    subject = asunto
    from_email = 'carlos.eht.09@gmail.com'
    recipient_list = [correo]
    # Se utiliza una variable para guardar la informacion del dispositivo que se esta usando
    

    # Renderiza la plantilla HTML con el contexto
    contexto = {'nombre': nombre,
                'correo': correo,
                'apellido': apellido,
                'usuario': usuario,
                'contra': contra,
                'asunto': asunto,
                'detalles': detalles}
    contenido_correo = render_to_string('email.html', contexto)

    # Envía el correo
    send_mail(subject, '', from_email, recipient_list, html_message=contenido_correo)
    # Redirige al inicio de sesion
    return redirect('/')

class forgotPwd(APIView):
    template_name="forgot_password.html"
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, self.template_name,{
                'form' : UserCreationForm
            })
    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            longitud = 10  # Longitud de la contraseña
            caracteres = string.ascii_letters + string.digits  # Caracteres permitidos
            contra_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud))
            try:
                user = User.objects.filter(email=request.POST['email'])
                if user.exists():
                    user = user[0]
                    nombre = user.first_name
                    usuario = user.username
                    user.set_password(contra_aleatoria)
                    user.save()
                    # Defines variables para que posteriormente las mandes por una mamada de link inverso xd a la clase que manda el correo
                    nombre = nombre
                    correo = request.POST['email']
                    apellido = " "
                    usuario = usuario
                    asunto = "Reestablecer contraseña"
                    detalles = 'Hemos recibido tu solicitud para restablecer tu contraseña en Task Master Pro. Tu seguridad es nuestra prioridad, y estamos aquí para ayudarte a recuperar el acceso a tu cuenta, es por eso que te hemos asignado una nueva contraseña para que puedas tener acceso nuevamente.'
                    # Igual aqui a contra le mandas el valor de la cadena generada automaticamente
                    contra = contra_aleatoria
                    # Aqui retorna a la clase de enviar correo
                    return redirect('enviar_correo', nombre=nombre, correo=correo, apellido=apellido, usuario=usuario, contra=contra, asunto=asunto, detalles=detalles)
                else:
                    return render(request, self.template_name,{
                        'form' : UserCreationForm,
                        "mensaje" : 'No hemos podido localizar tu cuenta, asegurate de que tu correo sea correcto'
                    })
            except IntegrityError:
                return render(request, self.template_name,{
                    'form' : UserCreationForm,
                    "mensaje" : 'No hemos podido localizar tu cuenta, asegurate de que tu correo sea correcto'
                })

def page_not_found(request, exception):
    return render(request, 'error-404.html', status=404)

def weather(request):
    if request.method == 'GET':
        return render(request, 'clima.html')
    if request.method == 'POST':
        city = request.POST['city']
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=707388566f992a643aa9bceea9e1e312".format(city)

        res = requests.get(url)

        try:
            temp = res.json()["main"]["temp"]
            vel_viento = res.json()["wind"]["speed"]
            latitud = res.json()["coord"]["lat"]
            longitud = res.json()["coord"]["lon"]
            descripcion = res.json()["weather"][0]["description"]
            
            tempo = round(temp - 273.15, 1)

            context = {
                'temp': "Temperatura:"+ str(tempo)+"°C",
                'vel_viento': "Velocidad del viento:"+ str(vel_viento)+"m/s",
                'latitud': "Latitud:"+ str(latitud),
                'longitud': "Longitud:"+ str(longitud),
                'descripcion': "Descripción:"+ str(descripcion),
            }

            return render(request, 'clima.html', context)

        except KeyError as e:
            error_message = "Error: Clave no encontrada - {}".format(e)
            return render(request, 'clima.html', {'error_message': error_message})

    return render(request, 'clima.html')