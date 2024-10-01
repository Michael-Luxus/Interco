from django.contrib import admin
from .models import Societe, Type, Tier, AssociationSociete, Indentite, IntercoHistorique, \
    Tableau, ListInterco, Global
from main.redirec import user_editor
from authentification.models import CustomUser
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group


class AssociationSocieteInline(admin.TabularInline):
    model = AssociationSociete
    fk_name = 'societe1'
    extra = 1


@admin.register(Societe)
class SocieteModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'user', 'server', 'password', 'types', 'value']
    list_filter = ['active']
    list_editable = ['active', 'types', 'server', 'value']
    search_fields = ['societe1']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'user', 'server', 'password', 'active', 'types', 'value')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AssociationSocieteInline]

    def has_module_permission(self, request):
        return not get(request) 

@admin.register(Type)
class TypeModelAdmin(admin.ModelAdmin):
    list_display = ['intitule']

    def has_module_permission(self, request):
        return not get(request) 

@admin.register(Global)
class GlobalDataAdmin(admin.ModelAdmin):
    list_display = ('societe', 'codetiers', 'intitule', 'tier', 'comptegeneral')

    def has_module_permission(self, request):
        return get(request) 


@admin.register(Tier)
class TiersDataAdmin(admin.ModelAdmin):
    list_display = ('societe',)

    def has_module_permission(self, request):
        return get(request) 
    

@admin.register(AssociationSociete)
class AssociationSocieteModelAdmin(admin.ModelAdmin):
    list_display = ['societe1', 'societe2', 'type', 'tier']
    list_filter = ['type', 'tier']
    search_fields = ['societe1', 'societe2']

    def has_module_permission(self, request):
        return not get(request) 

      
@admin.register(Indentite)
class IdentiteModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'correspondance']

    def has_module_permission(self, request):
        return not get(request) 


@admin.register(ListInterco)
class ListIntercoModelAdmin(admin.ModelAdmin):
    list_display = ['interco']

    def has_module_permission(self, request):
        return not get(request) 


@admin.register(Tableau)
class TableauAdmin(admin.ModelAdmin):
    list_display = ('base', 'ecPiece', 'ecRefPiece', 'ecNo')
    ordering = ('base',)
    search_fields = ('base', 'ecRefPiece')
    list_per_page = 10
    list_filter = ('base',)

    def has_module_permission(self, request):
        return not get(request) 


@admin.register(IntercoHistorique)
class IntercoHistoriqueAdmin(admin.ModelAdmin):
    list_display = ('interco', 'tableau1', 'tableau2')
    ordering = ('interco',)

    def has_module_permission(self, request):
        return not get(request) 





admin.site.unregister(CustomUser)
admin.site.unregister(Group)
    
class CustomUserAdmin(UserAdmin):
    def has_module_permission(self, request):
        return not get(request) 
    
class CustomGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        return not get(request) 
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

def get(request):
    # return request.user.username in user_editor
    return False

