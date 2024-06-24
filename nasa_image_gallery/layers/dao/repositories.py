# capa DAO de acceso/persistencia de datos.
from django.contrib.auth.decorators import login_required
from nasa_image_gallery.models import Favourite
from django.contrib.auth.models import User

def saveFavourite(image):
    try:
        fav = Favourite.objects.create(
            title=image['title'],
            description=image['description'],
            image_url=image['image_url'],
            date=image['date'],
            user=image['user']
        ) #Crea el favorito a partir de la clase "Favourite"
        fav.save()
        return fav
    except Exception as e:
        
        return None      


def getAllFavouritesByUser(user):
    if not user.is_authenticated:
        return []
    
    favouriteList = Favourite.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date')
    return list(favouriteList)
