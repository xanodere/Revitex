
from django import forms
from django.contrib.admin import widgets
from django.db.models import fields
from django.db.models.query import QuerySet
from django.forms.widgets import Select, Textarea
from .models import controle_Technique, randez_vous, centre, titre_Proprieté, ville
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.validators import RegexValidator


"""queryset= centre.objects.all()

choices = [0 for i range(len(queryset)) ]

for i in range(len(queryset)):
    choices[i][0] = queryset[i].nom 
    choices[i][1] = queryset[i].__str__()

print(choices)"""


class testform(forms.Form):
    Date = forms.SplitDateTimeField(widget = AdminSplitDateTime())
    centre = forms.ModelChoiceField(queryset= centre.objects.all(), widget=Select(attrs={"onchange":"selectdyn()"}))
    ct_technique = forms.CharField(widget=Select(attrs={"id":"ct_technique"}),label="Contrôle technique")
    tr_propriete = forms.CharField(widget=Select(attrs={"id":"tr_propriete"}), required = False, label="Titre de propriété")
    phoneNumberRegex = RegexValidator(regex = r"^0\d{9,15}$",message="Veuillez utiliser le format: '0XXXXXXXXX'.")
    GSM = forms.CharField(validators = [phoneNumberRegex], max_length = 16)
    email = forms.EmailField()

"""class testform(forms.ModelForm):
    class Meta:
        model = randez_vous
        fields = ("Date","centre" )
        
        widgets = {
              'Date': AdminSplitDateTime,
              "centre" : forms.Select(attrs={"onchange":"selectdyn()"})
        }"""

class testform_tronqué(forms.Form):
    def __init__(self, center, *args, **kwargs):
        super(testform_tronqué, self).__init__(*args, **kwargs)
        self.fields["ct_technique"] = forms.ModelChoiceField(queryset=center.Controles_dispo.all(),widget=Select(attrs={"id":"ct_technique"}),label="Contrôle technique:")
        self.fields["tr_propriete"] = forms.ModelChoiceField(queryset=center.Titre_dispo.all(),widget=Select(attrs={"id":"ct_technique"}), required = False,label="Titre de propriété")

    Date = forms.SplitDateTimeField(widget = AdminSplitDateTime)
    phoneNumberRegex = RegexValidator(regex = r"^0\d{9,15}$",message="Veuillez utiliser le format: '0XXXXXXXXX'.")

    GSM = forms.CharField(validators = [phoneNumberRegex], max_length = 16)
    email = forms.EmailField()
   

class dudeforrm(forms.Form):
    data = forms.SplitDateTimeField()


class formContact(forms.Form):
    nom = forms.CharField(max_length= 30, label="Votre nom")
    email = forms.EmailField(label="Votre email")
    objet = forms.CharField(max_length=300, label="Sujet")
    message = forms.CharField(widget=Textarea,label="Message",required=False)


    
class SearchForm(forms.Form):
    recherche = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={"class": "search-field", "placeholder": "Chercher une appels d'offre",
               }))


class Barreform(forms.Form):
    
    ville = forms.ModelChoiceField(queryset=ville.objects.all(),widget=Select(attrs={"id":"autocomplete-container","placeholder":"Ville","class":"pac-target-input"}))
    Contrôle_technique = forms.ModelChoiceField(queryset=controle_Technique.objects.all(),widget=Select(attrs={"id":"autocomplete-container","placeholder":"Contrôle technique","class":"pac-target-input"}))
    Titre_proprieté = forms.ModelChoiceField(queryset=titre_Proprieté.objects.all(),widget=Select(attrs={"id":"autocomplete-container","placeholder":"Titre de propriété","class":"pac-target-input"}))