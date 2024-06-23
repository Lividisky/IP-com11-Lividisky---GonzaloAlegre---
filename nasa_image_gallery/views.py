# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render, get_object_or_404
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from .models import Favourite
from  nasa_image_gallery.layers.generic import mapper
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #Importamos para paginación.
from django.http import Http404 
# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request.user) #devuelve la lista de url de los favoritos.


    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    per_page = request.GET.get('per_page', 5)  # Valor por defecto: 5 elementos por página
    try:
        per_page = int(per_page) # Convertir per_page a un entero para asegurar que sea un número válido
    except ValueError:
        per_page = 5
    images, favourite_list = getAllImagesAndFavouriteList(request)
    pagina= request.GET.get('page', 1) #Obtiene el número de la página o asigna el 1 si no tiene.
    try:
        paginator=Paginator(images, per_page) #Dice cuantas imagenes mostrar por página.
        images= paginator.page(pagina)
    except:
        raise Http404    #En caso de no encontrar página, da error.
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list, 'paginator': paginator, 'per_page':per_page}) 
     
    

# función utilizada en el buscador.
def search(request):
    search_msg = request.GET.get('query', '')
    per_page = request.GET.get('per_page', 5)

    if not search_msg:
        return redirect("home")
    else:
        filtro = services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
        paginator = Paginator(filtro, per_page)
        page_number = request.GET.get('page')

        try:
            filtro = paginator.page(page_number)
        except PageNotAnInteger:
            filtro = paginator.page(1)
        except EmptyPage:
            filtro = paginator.page(paginator.num_pages)

        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request.user)
        is_search_page=True
    return render(request, 'home.html', {'images': filtro, 'favourite_list': favourite_list, 'paginator': paginator, 'per_page':per_page, 'query':search_msg, 'is_search_page':is_search_page})
 # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.



# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos y eliminarlos.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.repositories.getAllFavouritesByUser(request.user)
    return render(request, 'favourites.html', {'favourite_list': favourite_list}) #Trae los favoritos del usuario y los renderiza a favoritos.html

    


@login_required
def saveFavourite(request, image_url):
    fav= mapper.fromTemplateIntoNASACard(request) #Transforma al request en NasaCard.
    fav.image_url= image_url
    fav_user= request.user
    if Favourite.objects.filter(image_url=image_url, user=request.user).exists(): #Verifica si el favorito ya existe
        print(f"El favorito para la imagen {image_url} ya existe.")
        return redirect(request.META.get('HTTP_REFERER')) #Si ya existe vuelve a la página anterior.
    else: #Si no existe. 
        image_data = {
        'title': fav.title,
        'description': fav.description, #Prepara los datos.
        'image_url': fav.image_url,
        'date': fav.date,
        'user': fav_user  # Asegúrate de pasar el objeto de usuario, no solo el ID
    }

    # Guardar el favorito utilizando la función del repositorio
        saved_favourite = services_nasa_image_gallery.repositories.saveFavourite(image_data) #Guarda el favorito.
        return redirect('home')
    
        


    


@login_required
def deleteFavourite(request, image_url):
    favorito= get_object_or_404(Favourite, image_url=image_url, user=request.user) #Obtiene la imagen a quitar, en base a su url.
    favorito.delete()  #elimina la imágen.
    return redirect(request.META.get('HTTP_REFERER')) #Redireccion a la misma página donde se añadió la imágen. 


    