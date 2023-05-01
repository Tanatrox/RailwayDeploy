from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import *
from .models import *
import datetime
from django.contrib.auth import views as auth_views

# Create your views here.

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("myapp:index")
		messages.error(request, "Registro sin éxito. Datos proporcionados no válidos.")
	form = NewUserForm()
	return render (request=request, template_name="myapp/register.html", context={"form":form})


def login_request(request):
	if request.method == "POST":
		form = IniciarSesionForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("myapp:index")
			else:
				messages.info(request,"Nombre de usuario o contraseña incorrectos.")
		else:
			messages.info(request,"Nombre de usuario o contraseña incorrectos.")
	form = IniciarSesionForm()
	return render(request=request, template_name="myapp/login.html", context={"form":form})

class EditarPerfil(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'myapp:login'
    form_class=EditarPerfilForm
    template_name='myapp/EditarPerfil.html'
    success_url= reverse_lazy('myapp:perfil')

    def get_object(self):
        return self.request.user

# @login_required(login_url='myapp:home')
def logout_request(request):
    logout(request)
    return redirect('myapp:login')


def home(request):
    if request.user.is_authenticated:
        return redirect('myapp:index')
    else:
        return render(request, 'myapp/home.html')


@login_required(login_url='myapp:login')
def index(request):
    contenido = Contenido.objects.all()
    context = {'contenido': contenido}
    return render(request, 'myapp/index.html', context)

@login_required(login_url='myapp:home')
def peliculas(request):
    contenido = Contenido.objects.filter(tipo='Pelicula')
    context = {'contenido': contenido}
    return render(request, 'myapp/peliculas.html', context)

@login_required(login_url='myapp:home')
def series(request):
    contenido = Contenido.objects.filter(tipo='Serie')
    context = {'contenido': contenido}
    return render(request, 'myapp/series.html', context)

@login_required(login_url='myapp:home')
def categorias(request):
    return render(request, 'myapp/categorias.html')

@login_required(login_url='myapp:home')
def recientes(request):
    d = datetime.date(2022, 9, 1)
    contenido = Contenido.objects.all()
    context = {
        'contenido': contenido,
        'fecha': d
    }
    return render(request, 'myapp/recientes.html', context)

@login_required(login_url='myapp:home')
def accion(request):
    contenido = Contenido.objects.filter(genero='Acción')
    context = {'contenido': contenido}
    return render(request, 'myapp/accion.html', context)

@login_required(login_url='myapp:home')
def animacion(request):
    contenido = Contenido.objects.filter(genero="Animación")
    context = {'contenido': contenido}
    return render(request, 'myapp/animacion.html', context)

@login_required(login_url='myapp:home')
def aventura(request):
    contenido = Contenido.objects.filter(genero="Aventura")
    context = {'contenido': contenido}
    return render(request, 'myapp/aventura.html', context)

@login_required(login_url='myapp:home')
def terror(request):
    contenido = Contenido.objects.filter(genero="Terror")
    context = {'contenido': contenido}
    return render(request, 'myapp/terror.html', context)

@login_required(login_url='myapp:home')
def ciencia_ficcion(request):
    contenido = Contenido.objects.filter(genero="Ciencia Ficción")
    context = {'contenido': contenido}
    return render(request, 'myapp/ciencia_ficcion.html', context)

@login_required(login_url='myapp:home')
def comedia(request):
    contenido = Contenido.objects.filter(genero="Comedia")
    context = {'contenido': contenido}
    return render(request, 'myapp/comedia.html', context)

@login_required(login_url='myapp:home')
def drama(request):
    contenido = Contenido.objects.filter(genero="Drama")
    context = {'contenido': contenido}
    return render(request, 'myapp/drama.html', context)

@login_required(login_url='myapp:home')
def familiar(request):
    contenido = Contenido.objects.filter(genero="Familiar")
    context = {'contenido': contenido}
    return render(request, 'myapp/familiar.html', context)

@login_required(login_url='myapp:home')
def fantasia(request):
    contenido = Contenido.objects.filter(genero="Fantasía")
    context = {'contenido': contenido}
    return render(request, 'myapp/fantasia.html', context)

@login_required(login_url='myapp:home')
def misterio(request):
    contenido = Contenido.objects.filter(genero="Misterio")
    context = {'contenido': contenido}
    return render(request, 'myapp/misterio.html', context)

@login_required(login_url='myapp:home')
def musicales(request):
    contenido = Contenido.objects.filter(genero="Musicales")
    context = {'contenido': contenido}
    return render(request, 'myapp/musicales.html', context)

@login_required(login_url='myapp:home')
def perfil(request):
    return render(request, 'myapp/perfil.html')

@login_required(login_url='myapp:home')
def Reproduccion(request, id):
    contenido = Contenido.objects.get(id=id)
    me_gusta = False
    fav = False

    if contenido.meGusta.filter(id=request.user.id).exists():
        me_gusta = False
    else:
        me_gusta = True

    if contenido.favoritos.filter(id=request.user.id).exists():
        fav = False
    else:
        fav = True

    context = {
        'contenido':contenido,
        'me_gusta':me_gusta,
        'fav':fav,
        }
    return render(request, 'myapp/reproductor.html', context)

@login_required(login_url='myapp:home')
def Me_gusta(request, id):
    contenido = get_object_or_404(Contenido, id=request.POST.get('contenido_id'))
    if contenido.meGusta.filter(id=request.user.id).exists():
        contenido.meGusta.remove(request.user)
    else:
        contenido.meGusta.add(request.user)
    return HttpResponseRedirect(reverse('myapp:reproducir', args=[str(id)]))

@login_required(login_url='myapp:home')
def Favoritos(request, id):
    contenido = get_object_or_404(Contenido, id=request.POST.get('contenido_id'))
    if contenido.favoritos.filter(id=request.user.id).exists():
        contenido.favoritos.remove(request.user)
    else:
        contenido.favoritos.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(reverse('myapp:reproducir', args=[str(id)]))

@login_required(login_url='myapp:home')
def Favoritos_lista(request):
    user = request.user
    contenido = user.favoritos.all()
    context = {'contenido': contenido}
    return render(request, 'myapp/favoritas.html', context)

@login_required(login_url='myapp:home')
def Busqueda(request):
    if request.method == 'POST':
        buscar = request.POST['buscar']
        contenido = Contenido.objects.filter(nombre__icontains=buscar)
        return render(request, 'myapp/busqueda.html', {'buscar':buscar, 'contenido':contenido})
    else:
        return render(request, 'myapp/busqueda.html', {'buscar':buscar, 'contenido':contenido})