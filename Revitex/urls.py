from django.urls import path
from .views import test, HomeView, tri, like, details, contact, home, appels_doffres, desc_appel, Le_controle_contact, Simu, rech_centres
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path("home/",home,name="home"),
    path("Le_contrôle_technique/",Le_controle_contact, name="Le_controle"),
    path("randez-vous/",test, name="test"),
    path("nos-centres/",HomeView.as_view(), name="dude" ),
    path("tri/<slug>",tri, name="tri" ),
    path("like/<slug>",like, name="like" ),
    path("desc_centre/<slug>",details, name="desc" ),
    path("Contact/",contact, name="contact"),
    path("Appels-d'offres/",appels_doffres, name="appels" ),
    path("desc_appel/<slug>",desc_appel, name="desc_appel"  ),
    path("simulateur/",Simu, name="Simu" ),
    path("rech_centre/",rech_centres, name="rech_centres" )
    

]


