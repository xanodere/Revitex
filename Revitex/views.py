import datetime
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import centre, controle_Technique, randez_vous, num_memoire, titre_Proprieté, email_Contact, Appels_offre, quota, slots
from .forms import testform, dudeforrm, testform_tronqué, formContact, SearchForm, Barreform
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date, datetime



def num_commande_inc():
    num_memoiretemp = num_memoire.objects.all()[0]
    num_memoiretemp.num += 1
    num_memoiretemp.save()
    return num_memoiretemp.num


# Create your views here.
def test(request):
    
   
    if len(request.GET) > 0:
        form = testform(request.GET)
        if form.is_valid():
            Date = form.cleaned_data['Date']
            centerr = form.cleaned_data['centre']
            ct_technique = form.cleaned_data['ct_technique']
            tr_propriete = form.cleaned_data['tr_propriete']
            GSM = form.cleaned_data['GSM']
            adresse = form.cleaned_data['email']
            
            
            user = centerr.gestionnaire 
            
            Randez_vous = randez_vous(numero=num_commande_inc(),
            centre = centerr,
            controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),
            TitrePropriété=titre_Proprieté.objects.filter(titre_proprieté=tr_propriete).first(),
            Date=Date,
            gestionnaire=user,
            GSM=GSM,
            email=adresse,)
           
            try :
                slot = slots.objects.get(centre=centerr,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),date= Date.date(),gestionnaire=centerr.gestionnaire)
                if slot.slots_restant > 0:
                    slot.slots_restant -=1
                    slot.save()
                    Randez_vous.save()
                    messages.info(request, 'Randez-vous enregistré avec succés')
                else:
                    messages.warning(request, "Il n'y a plus de place pour ce type de contrôle technique a cette date")
                
            except Exception:
                cotaa = quota.objects.get(centre=centerr,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),gestionnaire=centerr.gestionnaire).cota_par_jour
                if cotaa > 0:
                    slots.objects.create(centre=centerr,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),date=Date.date(),slots_restant=(cotaa-1),gestionnaire=centerr.gestionnaire)
                    Randez_vous.save()
                    messages.info(request, 'Randez-vous enregistré avec succés')    
                else:
                    messages.warning(request, "Il n'y a plus de place pour ce type de contrôle technique a cette date")
                
            
    else :
        form = testform()
   
   
    centres = centre.objects.all()
    dict = {}
    dict_titre = {}
    for center in centres:
        
        ## extraction des Controles_dispo selon le centre

        liste_con_dispo_sale = center.Controles_dispo.all()
        liste_con_dispo_propre = []

        for controle in liste_con_dispo_sale:
            liste_con_dispo_propre.append(controle.controle_techniques)
        

        dict[center.__str__()] = liste_con_dispo_propre

        ## extraction des titre_dispo selon le centre

        liste_titre_dispo_sale = center.Titre_dispo.all()
        liste_titre_dispo_propre = []

        for titre in liste_titre_dispo_sale:
            liste_titre_dispo_propre.append(titre.titre_proprieté)
        

        dict_titre[center.__str__()] = liste_titre_dispo_propre
  

    context = {
        "form" : form,
        "centres": centres,
        "dict_centre_contrDispo" : dict,
        "dict_titre" : dict_titre,

    }


    return render(request,"test.html",context)

def dude(request):

    form = dudeforrm()

    if  len(request.GET) > 0:
        form = dudeforrm(request.GET)
        if form.is_valid():
            print(form.cleaned_data['Data'])

    return render(request,"god.html",context={
        "form":form
     })


class HomeView(ListView):

    model = centre
    template_name = "nosCentres.html"
    context_object_name = "centre"
  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centres'] = centre.objects.all()
        context['form'] = Barreform()
        context['now']= datetime.now().time()
        return context


def tri(request, slug):
   if slug == "Ordre alphabetique" : 
    test = serializers.serialize("json", centre.objects.all().order_by("nom"), fields = ("fields","nom")) 
   if slug == "Ordre anti-alphabetique":
    test = serializers.serialize("json", centre.objects.all().order_by("nom").reverse(), fields = ("fields","nom")) 
   if slug == "Likes":
    test = serializers.serialize("json", centre.objects.all().order_by("likes").reverse(), fields = ("fields","nom")) 
   if slug == "Aléatoire" or slug== "Par défaut":
    test = serializers.serialize("json", centre.objects.all().order_by("?"), fields = ("fields","nom")) 
    if slug == "Par défaut":
        test = serializers.serialize("json", centre.objects.all(), fields = ("fields","nom")) 
   return JsonResponse(test, safe=False)


def like(request, slug):
    
    centre_liké = centre.objects.get(nom=slug)
    centre_liké.likes = centre_liké.likes +1
    centre_liké.save()

    return HttpResponse("like comptabilisé")


def details(request, slug):
    centre_chosit = centre.objects.get(nom=slug)
    
    
    if  len(request.GET) > 0:
        form = testform_tronqué(centre_chosit, request.GET,)
        if form.is_valid():
            Date = form.cleaned_data['Date']
            ct_technique = form.cleaned_data['ct_technique']
            tr_propriete = form.cleaned_data['tr_propriete']
            GSM = form.cleaned_data['GSM']
            adresse = form.cleaned_data['email']
            user = centre_chosit.gestionnaire
            
            Randez_vous = randez_vous(numero=num_commande_inc(),
            centre = centre_chosit,
            controleTechnique=ct_technique,
            TitrePropriété=tr_propriete,
            Date=Date,
            gestionnaire=user,
            GSM=GSM,
            email=adresse,)
            try :
                slot = slots.objects.get(centre=centre_chosit,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),date= Date.date(),gestionnaire=centre_chosit.gestionnaire)
                if slot.slots_restant > 0:
                    slot.slots_restant -=1
                    slot.save()
                    Randez_vous.save()
                    messages.info(request, 'Randez-vous enregistré avec succés')
                else:
                    messages.warning(request, "Il n'y a plus de place pour ce type de contrôle technique a cette date")
                
            except Exception:
                cotaa = quota.objects.get(centre=centre_chosit,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),gestionnaire=centre_chosit.gestionnaire).cota_par_jour
                if cotaa > 0:
                    slots.objects.create(centre=centre_chosit,controleTechnique=controle_Technique.objects.get(controle_techniques=ct_technique),date=Date.date(),slots_restant=(cotaa-1),gestionnaire=centre_chosit.gestionnaire)
                    Randez_vous.save()
                    messages.info(request, 'Randez-vous enregistré avec succés')    
                else:
                    messages.warning(request, "Il n'y a plus de place pour ce type de contrôle technique a cette date")
        else: 
            print(form.errors)
    else:
        form = testform_tronqué(centre_chosit)
    
    return render(request,"description_centre.html",{
        "centre" : centre_chosit,
        "form"   : form
    })



def contact(request):
    

    if  len(request.GET) > 0:
        form = formContact(request.GET)
        if form.is_valid():
            messages.info(request, 'Votre message à bien été envoyé')
            emails_receptions = []
            email_database = email_Contact.objects.all()
            for mail in email_database:
                emails_receptions.append(mail.email)
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            nom = form.cleaned_data["nom"]
            objet = form.cleaned_data['objet']
            objet = "Contact de revitex :" + objet
           
            total = "nom:    " + nom  + '\n' + "Message: \n\n " + message
            send_mail(objet, total, sender, emails_receptions)
    else: 
        form = formContact()
    
    context={
        "form":form
    }

    return render(request,"contact.html",context)


def home(request):
    appels = Appels_offre.objects.all()
    form = Barreform()
    
    return render(request, "home-page.html",{
        "appels" : appels,
        "form":form
    })

def appels_doffres(request):
    appels = Appels_offre.objects.all()
    
    if len(request.GET) > 0 :
        recherche = request.GET.get('recherche', "")
        queries = recherche.split(" ")
        print(queries)
        negatif = []
        for q in queries:
            items = Appels_offre.objects.exclude(
                Q(titre__icontains=q)
            )
            print(items)
            for item in items:
                negatif.append(item)
        print(negatif)
        appels = set(appels) - set(negatif)
    pop_appel = Appels_offre.objects.all().order_by("popularité").reverse()[:3]
    context={
        "appels" : appels,
        "pops" : pop_appel,
        "searchform" : SearchForm(),
    }
    return render(request,"appels-d'offres.html",context)

def desc_appel(request,slug):
    appel = Appels_offre.objects.get(id=slug)
    appel.popularité += 1
    appel.save()
    pop_appel = Appels_offre.objects.all().order_by("popularité").reverse()[:3]

    context = {
        "appel" : appel,
        "pops" : pop_appel,
        "searchform" : SearchForm(),
    }
    return render(request,"description_appel.html",context) 
    
def Le_controle_contact(request):
    pop_appel = Appels_offre.objects.all().order_by("popularité").reverse()[:3]
    context={
        "pops" : pop_appel,
        "searchform" : SearchForm(),
    }
    return render(request,"le_Controle_technique.html",context)

def Simu(request):
    pop_appel = Appels_offre.objects.all().order_by("popularité").reverse()[:3]
    context={
        "pops" : pop_appel,
        "searchform" : SearchForm(),
    }
    return render(request,"simulateur.html",context)


def rech_centres(request):
    centres = centre.objects.all()
   

    if len(request.GET) > 0 :
       
        ville = request.GET.get('ville', "")

        Contrôle_technique = request.GET.get('Contrôle_technique', "")
        
        Titre_proprieté = request.GET.get('Titre_proprieté', "")
        
        
        centres = centre.objects.filter(ville=ville,Controles_dispo=Contrôle_technique,Titre_dispo=Titre_proprieté)
       




    context={
        "centr": centres,
    }
    return render(request,"rech_centre.html",context)
