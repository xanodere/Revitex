from django.contrib import admin
from .models import randez_vous, ville, centre, controle_Technique, titre_Proprieté, num_memoire, image_gallerie, service_centre, features_centre, email_Contact, Documents, Appels_offre, quota, slots
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import Permission, User
from django.contrib import messages
from django_admin_listfilter_dropdown.filters import  DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
# Register your models here.


def Dupliquer(modeladmin, request, queryset):
    import copy

    for course in queryset:
    	# multiple could be selected
    	
        course_copy = copy.copy(course) # django copy object
        course_copy.id = None   # set 'id' to None to create new object
        course_copy.nom = "Temp"

        course_copy.save()  # (7) save the copy

        Dupliquer.short_description = "Duplicate Center"


class Randez_vous(GuardedModelAdmin):
    list_display = ["__str__", "date", "etat", "gestionnaire"]
    list_filter = (
        ("état",ChoiceDropdownFilter),
        ("gestionnaire",RelatedDropdownFilter),
        ("centre",RelatedDropdownFilter),
        )
    user_owned_objects_field="gestionnaire"
    user_can_access_owned_objects_only = True

class Service_centre(admin.ModelAdmin):
    list_display = ["titre", "prix"]

class appels_offre(admin.ModelAdmin):
    list_display = ["titre","date"]

class Centre(GuardedModelAdmin):
    
    list_display = ["__str__", "gestionnaire"]
    list_filter = (
        ("gestionnaire",RelatedDropdownFilter),
        )
    user_owned_objects_field="gestionnaire"
    user_can_access_owned_objects_only = True
    readonly_fields = ('likes',)
    actions = [Dupliquer]

    def save_model(self, request, obj, form, change):
        
        gestionnere = obj.gestionnaire
        
        for changed_data in form.changed_data:
            if changed_data == "Controles_dispo":
              try:
                ancien_controle =  obj.Controles_dispo.all()
              except Exception:
                ancien_controle =[]    
              nouveau_dispo = form.cleaned_data['Controles_dispo']
              super().save_model(request, obj, form, change)
              a_ajouter = set(nouveau_dispo)-set(ancien_controle)  
              a_supprimer = set(ancien_controle)-set(nouveau_dispo)
              print(a_ajouter)
              print(a_supprimer)
              for j in a_supprimer:
                  quota.objects.filter(centre=obj,controleTechnique=j).delete()
              for i in a_ajouter:
                quota.objects.create(centre=obj,controleTechnique=i,gestionnaire=gestionnere)
              self.message_user(request,"N'oubliez pas de definir le quota pour les nouveaux types de contrôle technique",messages.INFO)

            if changed_data == "gestionnaire": 
                permission = Permission.objects.get(name="Can change centre")
                permission2 = Permission.objects.get(name="Can change randez_vous")
                permission3 = Permission.objects.get(name="Can change quota")
                permission4 = Permission.objects.get(name="Can view slots")
        
                gestionnere.user_permissions.add(permission, permission2, permission3,permission4)
                randez_vouss = randez_vous.objects.filter(centre = obj)
                quotas=quota.objects.filter(centre= obj)
                slotss = slots.objects.filter(centre= obj)
                for Randez_vous in randez_vouss:
                    Randez_vous.gestionnaire = gestionnere 
                    Randez_vous.save()
                for quotaa in quotas:
                    quotaa.gestionnaire = gestionnere 
                    quotaa.save()
                for slot in slotss:
                    slot.gestionnaire = gestionnere 
                    slot.save()    
        super().save_model(request, obj, form, change)

class quotadmin(GuardedModelAdmin):
    user_owned_objects_field="gestionnaire"
    user_can_access_owned_objects_only = True
    list_display = ["centre","controleTechnique","gestionnaire"]
    list_filter = (
        ("gestionnaire",RelatedDropdownFilter),
        ("centre",RelatedDropdownFilter),
        ("controleTechnique",RelatedDropdownFilter),
        )

class slotsAdmin(GuardedModelAdmin):
    user_owned_objects_field="gestionnaire"
    user_can_access_owned_objects_only = True
    list_display = ["centre","controleTechnique","date","gestionnaire"]
    list_filter = (
        ("gestionnaire",RelatedDropdownFilter),
        ("centre",RelatedDropdownFilter),
        ("controleTechnique",RelatedDropdownFilter),
        ("date", DateRangeFilter)
        )

admin.site.register(service_centre, Service_centre)
admin.site.register(features_centre)
admin.site.register(controle_Technique)
admin.site.register(titre_Proprieté)
admin.site.register(ville)
admin.site.register(centre, Centre)
admin.site.register(randez_vous, Randez_vous)
admin.site.register(image_gallerie)
admin.site.register(email_Contact)
admin.site.register(Documents)
admin.site.register(Appels_offre,appels_offre)
admin.site.register(quota,quotadmin)
admin.site.register(slots,slotsAdmin)
