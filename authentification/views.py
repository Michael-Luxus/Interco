from django.shortcuts import render, redirect
from django.contrib import messages
import pyodbc
import json
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.decorators import login_required
from utils.ldap import ldap_login_connection
from .forms import LoginForm
from .models import CustomUser

def displayMain(request):
    soc_name = request.GET.get("societe_get")

    if soc_name:
        with open('societe.json', 'r', encoding='utf-8') as file:
            societes = json.load(file)

        for societe in societes:
            if societe["Nom"] == soc_name:
                connexion = connexionSQlServer(societe["Server"], societe["Base"], societe["Nom"])
                cursor = connexion.cursor()

                query = "SELECT * FROM AGRIEXP.ZVM"
                cursor.execute(query)
                rows = cursor.fetchall()

    return render(request, 'app/main.html')

def connexionSQlServer(server, base, name=None):
    conn = None
    value = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={base};UID=reader;PWD=m1234"
    try:
        conn = pyodbc.connect(value)
    except pyodbc.Error as e:
        print("===============================")
        print(f"Erreur de Connexion pour {server} à la base {name} ")
        print("===============================")
    except Exception as e:
        print("Autre erreur de connexion", str(e))
    return conn

class LoginLDAP(View):
    @staticmethod
    def get(request):
        forms = LoginForm()
        context = {
            'forms': forms,
        }
        # return render(request, 'auths/login.html', context)
        return render(request, 'authentification/login.html', context)

    @staticmethod
    def post(request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            # Authentification LDAP
            user = authenticate_and_get_user(username, password)
            if user:
                try:
                    # Récupération de l'utilisateur avec le nom d'utilisateur
                    user = CustomUser.objects.get(username=username)
                    # Gestion de la connexion
                    auth_login(request, user)
                    # messages.success(request, "Vous êtes maintenant connecté.")
                    return redirect('home:home')
                except CustomUser.DoesNotExist:
                    # Si l'utilisateur n'existe pas
                    messages.error(request, "Utilisateur introuvable dans la base de données. Veuillez contacter l'administrateur.")
                    return redirect('auths:login')
            else:
                # Si la connexion LDAP échoue
                messages.error(request, "Erreur de l'authentification LDAP. Vérifiez vos informations de connexion.")
                return redirect('auths:login')
        else:
            # Si le formulaire est invalide
            messages.error(request, "Le formulaire de connexion est invalide !")
            return redirect('auths:login')

@login_required
def logout_ldap(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    auth_logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('auths:login')

def authenticate_and_get_user(username, password):
    """
    Authentifie l'utilisateur avec LDAP et retourne l'objet utilisateur.
    """
    connexion = ldap_login_connection(username=username, password=password)
    if connexion:
        try:
            # On suppose que `ldap_login_connection` renvoie un utilisateur LDAP valide
            user = CustomUser.objects.get(username=username)
            return user
        except CustomUser.DoesNotExist:
            return None
    return None
