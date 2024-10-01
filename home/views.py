from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .models import Societe
import pyodbc, os

server = "172.16.69.1"
database = 'INTERCO'
username = 'reader'
password = 'm1234'
driver = "ODBC Driver 17 for SQL Server"

cnxn = pyodbc.connect(f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
cursor = cnxn.cursor()

def write_log(message):
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    with open(log_dir, "a") as f:
       f.write(f"{message}\n")

@login_required
def home(request):
    # Liste des sociétés disponibles
    societes = Societe.objects.all().order_by('name')
    
    # Récupérer les paramètres GET
    company1_name = request.GET.get('societe_1_name', '')
    company2_name = request.GET.get('societe_2_name', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Initialiser les données des tableaux
    table1_data = []
    table2_data = []
    
    if cnxn:
        try:
            cursor.execute("""
                SELECT JO_num, ec_piece, cg_,num, ct_num, ec_sens,
                    CASE
                        WHEN ec_sens = 0 THEN -ec_montant
                        WHEN ec_sens = 1 THEN ec_montant
                        ELSE 0
                    END AS ec_montant, societe
                FROM INTERCO.DB.GL
                WHERE societe IN (?, ?)
                AND date BETWEEN ? AND ?
            """, (company1_name, company2_name, date_debut, date_fin))

            rows = cursor.fetchall()

            # Séparer les transactions par société
            table1_data = [row for row in rows if row.societe == company1_name]
            table2_data = [row for row in rows if row.societe == company2_name]

        except pyodbc.Error as e:
            write_log(f"Erreur lors de l'exécution de la requête : {str(e)}")

    context = {
        'date_debut': date_debut,
        'date_fin': date_fin,
        'company1_name': company1_name,
        'company2_name': company2_name,
        'societes': societes,
        'table1_data': table1_data,
        'table2_data': table2_data,
        'access': True,
    }

    return render(request, 'home/home.html', context)

def inter_value(value):
    ct_num = []
    cg_num = []
    for ass in value:
        if ass.type.intitule == 'CT':
            ct_num.append(ass.tier.value) 
        else:
            cg_num.append(ass.tier.value) 
    result = [tuple(ct_num), tuple(cg_num)]
    return result

def format_tuple(t):
    if len(t) == 1:
        return "('{}')".format(t[0])
    return "({})".format(', '.join("'{}'".format(value) for value in t))