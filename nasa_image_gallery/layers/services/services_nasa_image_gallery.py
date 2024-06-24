# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from nasa_image_gallery.models import Favourite
from django.contrib.auth.decorators import login_required
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



def getAllFavouritesByUser(user):
        if not isinstance(user, User) or not user.is_authenticated:
            return[]
        favourite_list = Favourite.objects.filter(user=user).values_list('image_url', flat=True) #Devuelve una lista de urls.
        return list(favourite_list) 
        
        

