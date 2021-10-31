from django.db import models
from django.db.models.aggregates import Min
from location_field.models.plain import PlainLocationField
from django.core.validators import  MinValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime
from pytz import timezone
# Create your models here.

controleTechnique_choice = [
    ("C1","Véhicules léger"),
    ("C2","Poid lourd -15"),
    ("C3","Poid lourd +15"),
]

TitrePropriété_choice = [
    ("T1","Cyclomoteur"),
 
]

etat_randez_vous = [
    ("E","En attente"),
    ("V","Validé"),
    ("A","Annulé"),
]

class controle_Technique(models.Model):
    controle_techniques = models.CharField(default="Véhicules léger", max_length=30)
    
    def __str__(self):
            return self.controle_techniques


class titre_Proprieté(models.Model):
    titre_proprieté = models.CharField(default="Véhicules léger", max_length=30)

    def __str__(self):
        return self.titre_proprieté

class ville(models.Model):
    nom = models.CharField(max_length=30, default="", blank=True)

    def __str__(self):
        return self.nom

class image_gallerie(models.Model):
    nom = models.CharField(max_length=30)
    image = models.ImageField()

    def __str__(self):
        return self.nom       

class features_centre(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class service_centre(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.titre

    def prix(self):
        return str(self.price) + " MAD" 

    

class centre(models.Model):
    nom = models.CharField(max_length=30, default="", unique=True)
    description = models.TextField(default="Pas de description disponible")
    image_pres = models.ImageField()
    ville = models.ForeignKey(ville,on_delete=models.CASCADE)
    
    Controles_dispo = models.ManyToManyField(controle_Technique)

    latitude = models.DecimalField(max_digits=9, decimal_places=7, )
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    Titre_dispo = models.ManyToManyField(titre_Proprieté,blank=True)
    adresse = models.CharField(max_length = 100, default="pas d'adresse")
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    img_gallerie = models.ManyToManyField(image_gallerie)

    services = models.ManyToManyField(service_centre)
    features = models.ManyToManyField(features_centre)
    heure_ouverture = models.TimeField(default="9:00")
    heure_fermeture = models.TimeField(default="17:00")

    gestionnaire = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (
            ('gerer_centre', 'Gérer son centre'),
        )

    def __str__(self):
        return "Centre " + self.nom + " - "+ self.ville.nom  
    
    def get__titre(self):
        return "Centre " + self.nom + " - "+ self.ville.nom  


class randez_vous(models.Model):
    
    class Meta:
        verbose_name_plural = "Randez-vous"

    numero = models.IntegerField(default = 0,unique=True)
    centre = models.ForeignKey(centre,on_delete=models.CASCADE,null=True, blank=True)

    controleTechnique = models.ForeignKey(controle_Technique,on_delete=models.CASCADE)
    TitrePropriété = models.ForeignKey(titre_Proprieté,on_delete=models.CASCADE,blank=True,null=True)
    
    Date = models.DateTimeField (null=True, blank=True)
    état = models.CharField(choices=etat_randez_vous, default="E", max_length = 30)
    gestionnaire = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

   
    phoneNumberRegex = RegexValidator(regex = r"^0\d{9,15}$",message="Veuillez utiliser le format: '0XXXXXXXXX'.")
    GSM = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return str(self.numero)

    def etat(self):
        return self.état

    def date(self):
        return self.Date

##faudrait qd meme le refaire dans le form


class num_memoire(models.Model):
    num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.num)



class email_Contact(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
class Documents(models.Model):

    class Meta:
        verbose_name_plural = "Documents"
    
    titre = models.CharField(max_length=30)
    document = models.FileField()
    
    def __str__(self):
        return self.titre


class Appels_offre(models.Model):
    titre = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(default="Pas de description disponible")
    image = models.ImageField()
    villes = models.ManyToManyField(ville)
    document = models.ManyToManyField(Documents)
    popularité = models.IntegerField(default=0, validators=[MinValueValidator(0)])




class quota(models.Model):
    
    centre = models.ForeignKey(centre,on_delete=models.CASCADE,null=True)
    controleTechnique =models.ForeignKey(controle_Technique,on_delete=models.CASCADE,null=True)
    gestionnaire = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
   
    
    cota_par_jour = models.IntegerField(validators=[MinValueValidator(0)], default=10)
    

class slots(models.Model):

    class Meta:
        verbose_name_plural = "Slots"
     
    centre = models.ForeignKey(centre,on_delete=models.CASCADE,null=True)
    controleTechnique =models.ForeignKey(controle_Technique,on_delete=models.CASCADE,null=True)
    gestionnaire = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    slots_restant = models.IntegerField()
    



