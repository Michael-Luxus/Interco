from django.shortcuts import render
import pyodbc
from django.contrib.auth.decorators import login_required


server = "172.16.69.1"
database = 'INTERCO'
username = 'reader'
password = 'm1234'
driver = "ODBC Driver 17 for SQL Server"



cnxn = pyodbc.connect(f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
cursor = cnxn.cursor()



def gap(request):
    # Récupération des dates de début et de fin
    date_debut = request.GET.get("start-date")
    date_fin = request.GET.get("end-date") 

    # Récupérer la liste des sociétés depuis la base de données
    cursor.execute("SELECT DISTINCT SOCIETE AS SOCNAME FROM TABLE_TIERS ORDER BY SOCIETE ASC")
    societes = cursor.fetchall()

    # Obtenir les sociétés sélectionnées à partir des champs du formulaire
    societe_select_1 = request.POST.get('societe_select_1', '')  # Valeur vide par défaut si non sélectionnée
    societe_select_2 = request.POST.get('societe_select_2', '')

    # Ajoutez les données sélectionnées dans le contexte
    context = {
        'societes': societes,
        'societe_select_1': societe_select_1,
        'societe_select_2': societe_select_2,
        "date_debut": date_debut,
        "date_fin": date_fin
    }
    
    return render(request, 'gap/gap.html', context)


