from django.shortcuts import render
import locale, pyodbc
from datetime import datetime
import pandas as pd
from io import BytesIO
from openpyxl.styles import PatternFill, Font
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

global_result = None

# Définir la locale française
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

server = "172.16.69.1"
database = 'INTERCO'
username = 'reader'
password = 'm1234'
driver = "ODBC Driver 17 for SQL Server"

cnxn = pyodbc.connect(f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
cursor = cnxn.cursor()


    
def grandlivre(request):
    cursor.execute("SELECT DISTINCT SOCIETE AS SOCNAME FROM TABLE_TIERS ORDER BY SOCIETE ASC")
    societes = cursor.fetchall()
    
    context = {
        'societes': societes,
    }
    return render(request, 'grandlivre/grandlivre.html', context)

def grandLivreSociete(request):
    societe = request.POST.get('societe_select', None)
    date_start = request.POST.get('start-date', None)
    date_end = request.POST.get('end-date', None)


    global cursor
    global global_result
    
    if date_start:
        start_obj = datetime.strptime(date_start, '%Y-%m')
        year_start = start_obj.year
        month_start = start_obj.month

    if date_end:
        end_obj = datetime.strptime(date_end, '%Y-%m')
        year_end = end_obj.year
        month_end = end_obj.month



    if societe and month_start and month_end and year_start and year_end:
        query = "(select GRAND_LIVRE.SOCIETE, COMPTE, INTITULE_COMPTE, DATE_COMPTABLE,DATE_SAISIE, JOURNAL, PIECE, FACTURE, LIBELLE, GRAND_LIVRE.TIERS, INTITULE_TIERS, ECHEANCE, LETTRAGE, DEBIT, CREDIT, TYPE_LETTRAGE, SOLDE, INTERCO, ANNEE_MOIS, TYPE_INTERCO,isnull(TABLE_TIERS.TIERS,'') as Tiers_interco from GRAND_LIVRE left outer JOIN TABLE_TIERS ON  GRAND_LIVRE.TIERS= TABLE_TIERS.CODE and TABLE_TIERS.SOCIETE = GRAND_LIVRE.SOCIETE and TABLE_TIERS.CODE is not null where GRAND_LIVRE.SOCIETE = '?' AND month(DATE_COMPTABLE) BETWEEN '?' AND '?' AND year(DATE_COMPTABLE) BETWEEN '?' AND '?' AND GRAND_LIVRE.TIERS IS NOT NULL) union all ( select GRAND_LIVRE.SOCIETE, COMPTE, INTITULE_COMPTE, DATE_COMPTABLE,DATE_SAISIE, JOURNAL, PIECE, FACTURE, LIBELLE, GRAND_LIVRE.TIERS, INTITULE_TIERS, ECHEANCE, LETTRAGE, DEBIT, CREDIT, TYPE_LETTRAGE, SOLDE, INTERCO, ANNEE_MOIS, TYPE_INTERCO,isnull(TABLE_TIERS.TIERS,'') as Tiers_interco from GRAND_LIVRE left outer JOIN TABLE_TIERS ON  GRAND_LIVRE.COMPTE= TABLE_TIERS.COMPTE_GENERAL and TABLE_TIERS.SOCIETE = GRAND_LIVRE.SOCIETE and TABLE_TIERS.CODE is  null where GRAND_LIVRE.SOCIETE = '?' AND  month(DATE_COMPTABLE) BETWEEN '?' AND '?' AND year(DATE_COMPTABLE) BETWEEN '?' AND '?'  AND GRAND_LIVRE.TIERS IS  NULL )  "


        processed_querry = query.replace('?', '{}').format(societe, month_start, month_end, year_start, year_end, societe, month_start, month_end, year_start, year_end)

        try:
            cursor.execute(processed_querry) 
        except pyodbc.Error as e:
            print(f"Erreur 55°° : {str(e)}")

        data = cursor.fetchall()

        result = []
        for row in data:
            result.append({       
                'SOCIETE': row[0], 'COMPTE': row[1], 'INTITULE_COMPTE': row[2], 'DATE_COMPTABLE': row[3].strftime("%d/%m/%Y"), 'DATE_SAISIE': row[4].strftime("%d/%m/%Y"), 'JOURNAL': row[5], 'PIECE': row[6], 'FACTURE': row[7], 'LIBELLE': row[8], 'TIERS': row[9], 'INTITULE_TIERS': row[10], 'ECHEANCE': row[11].strftime("%d/%m/%Y"), 'LETTRAGE': row[12], 'DEBIT': row[13], 'CREDIT': row[14], 'TYPE_LETTRAGE': row[15], 'SOLDE': row[16], 'INTERCO': row[17], 'ANNEE_MOIS': row[18], 'TYPE_INTERCO': row[19], 'TIERS_INTERCO': row[20]
            })
        
        global_result = result

        # Return the result as JSON
        return JsonResponse({'data': result, 'status': 'success'})


def download_grand_livre(request):
    return export_simple_xls()


def export_simple_xls():
    global global_result

    # Create a DataFrame from the global result
    df = pd.DataFrame(global_result)

    # Create an in-memory output
    output = BytesIO()

    # Use pd.ExcelWriter to write the DataFrame to the output
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

        # Get the workbook and the sheet
        sheet = writer.sheets['Data']

        # Define the styles
        blue_fill = PatternFill(start_color="005ec2", end_color="005ec2", fill_type="solid")
        white_font = Font(color="FFFFFF", bold=True)

        # Apply styles to the first row (header)
        for cell in sheet[1]:  # The first row
            cell.fill = blue_fill
            cell.font = white_font

        # Adjust column widths based on the content
        for column in sheet.columns:
            max_length = 0
            for cell in column:  # Iterate over the cells in the column
                try:
                    if cell.value:  # Check if the cell has a value
                        max_length = max(max_length, len(str(cell.value)))  # Update max_length
                except Exception as e:
                    print(f"Error accessing cell value: {e}")
            adjusted_width = max_length + 2  # Add some padding
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width  # Adjust width

    # Create the response object with appropriate content type
    output.seek(0)  # Move the pointer to the start of the stream
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="grand_livre.xlsx"'

    return response