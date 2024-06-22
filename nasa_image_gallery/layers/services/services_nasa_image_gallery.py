# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
from nasa_image_gallery.models import Favourite

def getAllImages(input=None):
    # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
    # ¡OJO! el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.
    json_collection = transport.getAllImages(input)

    images = []
    for i in json_collection:
        imagen = mapper.fromRequestIntoNASACard(i)
        images.append(imagen)
    # recorre el listado de objetos JSON, lo transforma en una NASACard y lo agrega en el listado de images. Ayuda: ver mapper.py.

    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request): #Transforma al requeste del template en una nasa card.
    title = request.POST.get('title')
    description = request.POST.get('description')
    image_url = request.POST.get('image_url')
    date = request.POST.get('date')

    fav =  Favourite(
        title=title,
        description=description,
        image_url=image_url,
        date=date,
        user=request.user
        )

    return repositories.saveFavourite(fav) #Lo guarda como favorito.
 
def getAllFavouritesByUser(user):
        favourite_list = Favourite.objects.filter(user=user).values_list('image_url', flat=True) #Devuelve una lista de urls.
        return list(favourite_list)
        
        


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.