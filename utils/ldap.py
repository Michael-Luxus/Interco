import ldap3
import logging
from django.conf import settings
from ldap3.core.exceptions import LDAPException
from ldap3 import Server, Connection

from utils.logs import write_log


# Définition de la fonction pour rechercher les attributs LDAP d'un utilisateur
def ldap_search_attributes(conn, username):
    # Spécification de la base de recherche LDAP et du filtre de recherche
    search_base = settings.DN_LDAP
    # search_filter = f"(&(sAMAccountName={username}))"
    search_filter = f"(&(sAMAccountName={username}))"
    try:
        # Recherche des attributs spécifiés pour l'utilisateur donné
        conn.search(search_base, search_filter, attributes=['mail', 'sn', 'givenName'])

        # Vérification si des résultats ont été trouvés
        if len(conn.entries) > 0:
            entry = conn.entries[0]
            write_log(f"Utilisateur Trouver : {entry}", level=logging.INFO)

            # Extraction des attributs si présents dans l'entrée LDAP
            email = entry.mail[0] if 'mail' in entry and len(entry.mail) > 0 else None
            lastname = entry.sn[0] if 'sn' in entry else None
            firstname = entry.givenname[0] if 'givenName' in entry else None

            # Retourne un dictionnaire avec les attributs trouvés
            return {
                'email': email,
                'lastname': lastname,
                'firstname': firstname
            }
    except LDAPException as e:
        # Utilisation d'un système de journalisation pour enregistrer les erreurs
        write_log(f"Erreur de recherche LDAP : {str(e)}")
        return False


# Définition de la fonction pour la connexion LDAP
def ldap_login_connection(username, password):
    # Construction du DN de l'utilisateur
    user = f"SMTP-GROUP\\{username}".strip()
    write_log(f"DN: {user}", level=logging.INFO)
    try:
        # Création de l'objet de serveur LDAP
        server = Server(settings.SERVER_LDAP, get_info=ldap3.ALL)

        # Connexion au serveur LDAP avec l'utilisateur et le mot de passe fournis
        with Connection(
                server=server,
                user=user,
                password=password,
                authentication=ldap3.SIMPLE,
                client_strategy=ldap3.SYNC) as conn:

            # Vérification de la liaison réussie (authentification)
            if not conn.bind():
                write_log("Bind Error !", level=logging.ERROR)
                return False
            write_log("Bind Successfully !", level=logging.INFO)
            # Appel de la fonction de recherche d'attributs LDAP pour l'utilisateur
            return ldap_search_attributes(conn, username)

    except LDAPException as e:
        # Utilisation d'un système de journalisation pour enregistrer les erreurs
        write_log(f"Erreur de connexion LDAP : {str(e)}")
        return False

def ldap_logout_connection(ldap_connection):
    try:
        ldap_connection.unbind_s()
        print("Déconnexion LDAP réussie.")
    except ldap.LDAPError as e:
        print(f"Erreur lors de la déconnexion LDAP: {e}")

# Exemple d'utilisation
ldap_conn = ldap_login_connection('your_username', 'your_password')
if ldap_conn:
    ldap_logout_connection(ldap_conn)