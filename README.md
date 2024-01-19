![Static Badge](/static/badges/Build-with-Python.svg) ![Static Badge](/static/badges/Build-with-Django.svg) ![Static Badge](/static/badges/Build-with-MySQL.svg)   
![Static Badge](/static/badges/Use-Pytest.svg)   
![Static Badge](/static/badges/Use-Sentry.svg)   
![Static Badge](/static/badges/Use-Postman.svg) ➔ [Documentation Postman du projet Epic Events](https://documenter.getpostman.com/view/26427645/2s9Ykkg3Lu)   

![Static Badge](/static/badges/tests-badge.svg)   
![Static Badge](/static/badges/coverage-badge.svg)   
![Static Badge](/static/badges/flake8-badge.svg)   

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/26427645-f52af692-f8f7-4e4e-8efc-53d8d0c53e5b?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26427645-f52af692-f8f7-4e4e-8efc-53d8d0c53e5b%26entityType%3Dcollection%26workspaceId%3D6431c2eb-5581-47a5-91d7-1cd5511f9a44)

<div id="top"></div>

## Menu   
1. **[Informations générales](#informations-générales)**   
2. **[Fonctionnalitées](#fonctionnalitées)**   
3. **[Liste pré-requis](#liste-pre-requis)**   
4. **[Création environnement](#creation-environnement)**   
5. **[Activation environnement](#activation-environnement)**   
6. **[Installation des librairies](#installation-librairies)**   
7. **[Installation de la base de données MySQL](#installation-bdd)**   
8. **[Connecter l'application à la base de données MySQL](#connexion-bdd)**   
9. **[Installation des variables d'environnement](#installation-environnement)**   
10. **[Administration opérations CRUD et gestionnaires de commmandes](#administration-bdd)**   
11. **[Exécution de l'application](#execution-application)**   
12. **[Tests avec Pyest](#tests-pytest)**      
13. **[Tests de couverture de code avec Coverage](#tests-coverage)**
14. **[Rapport avec flake8](#rapport-flake8)**   
15. **[Informations importantes sur les différents fichiers et dossiers](#informations-importantes)**   
16. **[Auteur et contact](#auteur-contact)**   


<div id="informations-générales"></div>

<div style="display: flex; align-items: center;">
    <h3>Projet Epic Events</h3>
    <img src="/static/img/logo_light.png" alt="Logo Epic Events" width="150">
</div>

- Application conçu pour faciliter une collaboration efficace entre les équipes chez **Epic Events** de la gestion de la relation client **CRM** (Customer Relationship Management).   
- L'objectif principal est de mettre en place une base de données qui permette de stocker et de manipuler de manière sécurisée les informations des clients, ainsi que les contrats et les événements.   
- Application **Python**, incluant la journalisation avec **Sentry**.   

>_Note : Plusieurs besoins de l'application **Epic Events** ont été mis en place._   
   
#### Besoins généraux   
- Chaque collaborateur doit avoir ses identifiants pour utiliser la plateforme.   
- Chaque collaborateur est associé à un rôle (suivant son département).   
- La plateforme doit permettre de stocker et de mettre à jour les informations sur les clients, les contrats et les événements.   
- Tous les collaborateurs doivent pouvoir accéder à tous les clients, contrats et événements en lecture seule.   

#### Besoins individuels   

##### Équipe de gestion :   
- ``Créer``, ``mettre à jour`` et`` supprimer`` des collaborateurs dans le système **CRM**.   
- ``Créer`` et ``modifier`` tous les contrats.   
- Filtrer l’affichage des événements : afficher tous les événements qui n’ont pas de « support » associé.   
- ``Modifier`` des événements (pour associer un collaborateur support à l’événement).   

#### Besoins individuels   

##### Équipe commerciale :   
- ``Créer`` des clients (le client leur sera automatiquement associé).   
- ``Mettre à jour`` les clients dont ils sont responsables.   
- ``Modifier`` et ``mettre à jour`` les contrats des clients dont ils sont responsables.   
- Filtrer l’affichage des contrats : afficher tous les contrats qui ne sont pas encore signés, ou qui ne sont pas encore entièrement payés.   
- ``Créer`` un événement pour un de leurs clients qui a signé un contrat.   

#### Besoins individuels   

##### Équipe support :   
- Filtrer l’affichage des événements : afficher uniquement les événements qui leur sont attribués.   
- ``Mettre à jour`` les événements dont ils sont responsables.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="fonctionnalitées"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Fonctionnalitées   

- Opérations d'administration et de gestion des utilisateurs, des clients, des contrats et des événements.   
- Visualisation des informations et données des utilisateurs, des clients, des contrats et événements.   

>_Note : Testé sous **Windows 10** Professionnel - **Python** 3.12.0_   

--------------------------------------------------------------------------------------------------------------------------------

<div id="liste-pre-requis"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Liste pré-requis   

- Un compte **Sentry** ➔ https://sentry.io/welcome/   
- Un compte **Postman** ➔ https://www.postman.com/   

Application conçue avec les technologies suivantes :   
- **Python** v3.12.0 choisissez la version adaptée à votre ordinateur et système. **Python** est disponible à l'adresse suivante ➔ https://www.python.org/downloads/   
- **Django** version 4.2.7 ➔ [Documentation Django](https://docs.djangoproject.com/en/5.0/)    
- **MySQL** version 8.0 ➔ [Documentation MySQL](https://dev.mysql.com/doc/)    
- **Windows 10** Professionnel   

- Les scripts **Python** s'exécutent depuis un terminal.   
- Pour ouvrir un terminal sur Windows, pressez la touche ``windows + r`` et entrez ``cmd``.   
- Sur **Mac**, pressez la touche ``command + espace`` et entrez ``terminal``.   
- Sur **Linux**, vous pouvez ouviri un terminal en pressant les touches ``Ctrl + Alt + T``.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="creation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Création de l'environnement virtuel   

- Installer une version de **Python** compatible pour votre ordinateur.   
- Une fois installer ouvrer le cmd (terminal) placer vous dans le dossier principal (dossier racine).   

Taper dans votre terminal :    

```bash   
$ python -m venv env
```   
Un répertoire appelé ``env`` doit être créé.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="activation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Activation de l'environnement virtuel   

- Placez-vous avec le terminal dans le dossier principale (dossier racine).   
  Pour activer l'environnement virtuel créé, il vous suffit de taper dans votre terminal :   

```bash
$ env\Scripts\activate.bat
```
- Ce qui ajoutera à chaque début de ligne de commande de votre terminal ``(env)`` :   
>*Note : Pour désactiver l'environnement virtuel, il suffit de taper dans votre terminal :*   

```bash
$ deactivate
```
--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-librairies"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Installation des librairies   

- Le programme utilise plusieurs librairies externes et modules de **Python**, qui sont répertoriés dans le fichier ``requirements.txt``.   
- Placez-vous dans le dossier où se trouve le fichier ``requirements.txt`` `à la racine du projet, l'environnement virtuel doit être activé.   
- Pour faire fonctionner l'application, il vous faudra installer les librairies requises.   
- À l'aide du fichiers ``requirements.txt`` mis à disposition.   

Taper dans votre terminal la commande :   

```bash
$ pip install -r requirements.txt
```
--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-bdd"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Installation du SGBD MySQL   

- Pour le projet **Epic Events** la gestion des données utilise le SGBD **MySQL**.   
- Installer **MySQL** qui est disponible à l'adresse suivante ➔ https://dev.mysql.com/downloads/installer/   

- Une fois le programme téléchargé, lancez-le en double-cliquant dessus, autorisez le programme à s'installer.   
>_Note : Je vous conseille de choisir la version **Serveur only** lors de l'installation._   

- Il y a plusieurs manières d'utiliser **MySQL** soit par ``MySQL 8.0 Command Line Client`` une fois **MySQL** installé.   
- Soit par le terminal CMD de Windows, pour cela il faut créer une variable d'environnement pour ouvrir **MySQL** d'un terminal CMD.   
>_Note : Je vous conseille de créer une variable d'environnement dans le **PATH**._   

Allez dans ``Paramères avancés du système`` ➔ ``Variables d'environnement`` ➔ ``Variable système`` ➔ ``Path``   

*Cliquez sur ``modifier`` ajoutez les variables suivantes :*   

```bash   
C:\Program Files\MySQL\MySQL Server 8.0\bin
C:\Program Files\MySQL\MySQL Server 8.0\lib
```   

Après ces modifications vous pourrez utiliser **MySQL** depuis le terminal CMD.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-bdd"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Installation et chargement de la base de données MySQL   

>_Note : Ces commandes sont fonctionnelles si vous avez installer les variables d'environnement dans le **PATH**._   

- Pour lancer et vous connectez à **MySQL**   
  Lancer un terminal CMD, puis taper la commande :   

```bash   
$ mysql -u root -p
```   

- Une fois identifié et connecté créer la base de données avec la commande :   

```js   
$ mysql> CREATE DATABASE epicevents;
```   

- Pour afficher la base de données **MySQL**.   
Ensuite taper la commande :   

```js   
$ SHOW DATABASES;
```   

- Pour utiliser la base de données.   
  On utilise la commande :   

```js   
$ USE epicevents;
```  

- Charger les tables de la base de données grâce au fichier ``EpicEvents.sql`` disponible dans le dossier principal du projet.   
  On utilise la commande :   

```bash
$ source C:\path\to\directory\Epic Events\EpicEvents.sql
```   

- Quittez **MySQL**.   
  Avec la commande :   

```bash   
$ exit;
```  

<div id="connexion-bdd"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

--------------------------------------------------------------------------------------------------------------------------------

### Connecter l'application à la base de données MySQL   

Dans le cadre de **Django** et de l'utilisation de **MySQL**, la configuration de Django pour travailler avec une base de données **MySQL** implique d'établir une connexion à cette dernière.   
Après avoir installé **MySQL** et chargé les tables depuis le fichier EpicEvents.sql, la configuration de l'application **Django** nécessite la mise en place de cette connexion.   

- Ouvrez un terminal CMD activer l'environnement virtuel.   
  Exécutez la commande :   

```bash   
$ python manage.py makemigrations
```   

- Ensuite taper la commande :   
```bash   
$ python manage.py migrate
```   

- L'exécution des commandes ``makemigrations`` et ``migrate`` génère les tables, y compris celles de jonction (d'associations), dans la base de données.   
- Ces tables de jonction sont automatiquement créées en fonction de la structure des modèles **Django**.   

À présent, la base de données est chargée et fonctionnelle, prête à être utilisée avec l'application **Epic Events**.   
Vous pouvez vérifier ceci en vous connectant à **MySQL**.   

- Dans un terminal CMD, connectez-vous avec la commande suivante :   

```bash   
$ mysql -u root -p
```   

- Affichez et utilisez la base de données avec les commandes suivantes :   

```js   
$ SHOW DATABASES;
$ USE epicevents;
```   

- Pour vérifier la création et les structures des tables, utilisez les commandes :   

```js   
$ SHOW tables;
$ SHOW COLUMNS FROM NomDeLaTable;
```   

- Pour vérifier les données présentes dans une table, utilisez les commandes :   

```bash   
$ SELECT * FROM NomDeLaTable;

#Cette requête est utilisée pour afficher la déclaration SQL complète nécessaire pour recréer une table existante, y compris tous ses indices, contraintes et autres propriétés.
#Cette requête retourne un ensemble de résultats avec une colonne appelée "Create Table" qui contient la déclaration SQL complète de la table spécifiée.
$ SHOW CREATE TABLE NomDeLaTable;
```   

#### ERD Epic Events   

- ERD (Entity-Relationship Diagram) de la base de données **Epic Events**   

![ERD bdd](/static/img/ERD_Epic_Events.png)    

--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Installation des variables d'environnement   

- Pour utiliser l'application, il faut configurer l'environnement de l'application **Epic Events** et générer une clé secrète aléatoire pour la configuration de **Django**.   
- De plus, il est nécessaire d'inclure des noms de variables d'environnement préconfigurées tels que :   

##### Configuration de l'environnement :   
Il est essentiel de configurer l'environnement de l'application.
- Générez une clé secrète aléatoire pour la configuration de **Django** et incluez des noms de variables d'environnement préconfigurées.   
Utilisez le fichier ``.env``, voici un exemple d'un fichier ``.env`` une fois configuré avec les paramètres :   

```bash   
DJANGO_SECRET_KEY=%x7xmakyvew_am2-0_n*0inmjkdncucg!^_!i3&==k@d2j+4vo
DB_NAME=epicevents
DB_USER=root
DB_PASSWORD=************
DB_HOST=127.0.0.1
DB_PORT=3306
SENTRY_DSN=https://4e0c26cb1f6e2b2e0cfa9eb9ab598f9a@o4505744249623232.ingest.sentry.io/4506530972696576
```   

##### Création du fichier ``.env`` :   

À la racine du dossier principal d'**Epic Events**, exécutez le fichier ``create_env.bat`` ➔ ([create_env.bat](create_env.bat)).   
Double-cliquez dessus pour enregistrer le fichier ``.env`` à la racine du dossier principal.   

##### Configuration du fichier ``.env`` :   

Une fois le fichier ``.env`` créé, ouvrez-le avec un éditeur de texte.   
Remplissez les champs avec les valeurs appropriées pour chaque variable d'environnement.   
Ces étapes garantissent une configuration correcte de l'environnement nécessaire au bon fonctionnement de l'application **Epic Events**.   

> _Note : La clé **SENTRY_DSN** doit être récupérée dans les paramètres de votre compte **Sentry**._   

> _Note : Le fichier .env généré doit être configuré avec des valeurs appropriées pour chaque variable d'environnement avant utilisation._   

--------------------------------------------------------------------------------------------------------------------------------

<div id="administration-bdd"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Administration opérations CRUD et gestionnaire de commmandes   

La gestion des opérations CRUD peut se faire de plusieurs manières :   

- En utilisant des requêtes sous forme de commandes dans **MySQL**   
- En utilisant des commandes dans Le shell **Django**   
- En utilisant le site d'administration de **Django** à l'adresse suivante ➔ http://127.0.0.1:8000/admin/   

>_Note : Le site d'administration de **Django** est accessible seulement aux administrateurs et aux utilisateurs de l'équipe gestion._   

- Dans ce projet, la mise en place d'un gestionnaire de commandes a été réalisée avec les bibliothèques ``Click`` et ``Rich``, ainsi qu'avec ``BaseCommand`` de **Django**.   
- Ce gestionnaire de commandes fonctionne avec les privilèges administrateur et ne reflète donc pas les permissions et besoins individuels de chaque département.   

> _Note : Les permissions de chaque département sont fonctionnelles et activées, ceci peut être vérifié en utilisant **Postman**._   

**Postman** ➔ [Documentation Postman du projet Epic Events](https://documenter.getpostman.com/view/26427645/2s9Ykkg3Lu)   

- Import et exécute la collection dans votre propre espace de travail **Postman** ➔ [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="vertical-align: middle; width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/26427645-f52af692-f8f7-4e4e-8efc-53d8d0c53e5b?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26427645-f52af692-f8f7-4e4e-8efc-53d8d0c53e5b%26entityType%3Dcollection%26workspaceId%3D6431c2eb-5581-47a5-91d7-1cd5511f9a44)

--------------------------------------------------------------------------------------------------------------------------------

#### Ouvrez un terminal CMD et activez l'environnement virtuel.   

Les commandes d'administration et de gestion pour utiliser le gestionnaire de commandes.   
##### - Afficher tous les utilisateurs :   

* Exemple de sortie dans le terminal :   
![Display users](/static/img/screen_display_users.png)   

```bash   
$ python manage.py management_user --display_users
```   

##### - Création d'un utilisateur ou d'un administrateur :   

```bash   
$ python manage.py management_user --create_user
$ python manage.py management_user --create_superuser
$ python manage.py management_user --update_user [id_user]
$ python manage.py management_user --delete_user [id_user]
```   

##### - Afficher tous les clients :   

* Exemple de sortie dans le terminal :   
![Display clients](/static/img/screen_display_clients.png)   


```bash   
$ python manage.py management_client --display_clients
```   

##### - Création d'un client :   

```bash   
$ python manage.py management_client --create_client
$ python manage.py management_client --update_client [id_client]
$ python manage.py management_client --delete_client [id_client]
```   

##### - Afficher tous les contrats :   

* Exemple de sortie dans le terminal :   
![Display contracts](/static/img/screen_display_contracts.png)   


```bash   
$ python manage.py management_contract --display_contracts
```   

- Création d'un contrat :   
```bash   
$ python manage.py management_contract --create_contract
$ python manage.py management_contract --update_contract [id_contract]
$ python manage.py management_contract --delete_contract [id_contract]
```   

##### - Afficher tous les événements :   

* Exemple de sortie dans le terminal :   
![Display events](/static/img/screen_display_events.png)   


```bash   
$ python manage.py management_event --display_events
```   

##### - Création d'un événement :   

```bash   
$ python manage.py management_event --create_event
$ python manage.py management_event --update_event [id_event]
$ python manage.py management_event --delete_event [id_event]
```   
--------------------------------------------------------------------------------------------------------------------------------

<div id="execution-application"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Exécution de l'application   

##### Utilisation   

Lancement du serveur **Django**.   
- Placez-vous avec le terminal CMD dans le dossier principal.   
- Activer l'environnement virtuel et ensuite lancer le serveur **Django**. Taper dans votre terminal la commande :   

```bash   
$ python manage.py runserver
```   

- Démarrer le serveur vous permet d'accéder au site d'administration de **Django** à l'adresse suivante ➔ http://127.0.0.1:8000/admin/   
- D'utiliser les requêtes ``GET``, ``POST``, ``PUT``, ``DEL`` lors de l'utilisation de **Postman**.   

>_Note : Le site d'administration de **Django** est accessible seulement aux administrateurs et aux utilisateurs de l'équipe gestion._   

>*Note navigateur : Les tests ont était fait sur **Firefox** et **Google Chrome**.*   

--------------------------------------------------------------------------------------------------------------------------------

<div id="tests-pytest"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Tests avec Pytest   

- Nous effectuons des tests unitaires et d'intégrations de plusieurs manières pour garantir la qualité du code.   

>*Note : Pour exécuter les tests il est nécessaire d'avoir activer l'environnement virtuel, mais il n'est pas nécessaire de lancer le serveur **Django**.*    

##### Exécution de Pytest   

- Utilisation de **Pytest** pour effectuer les tests. ➔ [Documentation Pytest](https://docs.pytest.org/)   
- Pour exécuter les tests à l'aide de **Pytest**, utilisez la commande suivante :   

```bash   
$ pytest
```   

```js   
(env) C:\Epic Events>pytest
=========================================== test session starts ===========================================
platform win32 -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0 -- C:\Epic Events\env\Scripts\python.exe
cachedir: .pytest_cache
django: version: 4.2.7, settings: EpicEvents.settings (from ini)  
rootdir: C:\Epic Events
configfile: setup.cfg
plugins: cov-4.1.0, django-4.7.0, time-machine-2.13.0
collected 67 items

contracts/tests.py::TestContractsApp::test_contract_print_details PASSED                             [  1%]
contracts/tests.py::TestContractsApp::test_contract_str_representation PASSED                        [  2%]
contracts/tests.py::TestContractsApp::test_save_method PASSED                                        [  4%]
contracts/tests.py::TestContractViewSet::test_all_contracts_details PASSED                           [  5%]
contracts/tests.py::TestContractViewSet::test_contract_details PASSED                                [  7%]
contracts/tests.py::TestContractViewSet::test_contract_details_unauthorized_user PASSED              [  8%]
contracts/tests.py::TestContractViewSet::test_contracts_list PASSED                                  [ 10%]
contracts/tests.py::TestContractViewSet::test_create_contract PASSED                                 [ 11%]
contracts/tests.py::TestContractViewSet::test_create_contract_unauthorized_user PASSED               [ 13%]
contracts/tests.py::TestContractViewSet::test_destroy_contract PASSED                                [ 14%]
contracts/tests.py::TestContractViewSet::test_destroy_contract_unauthorized_user PASSED              [ 16%]
contracts/tests.py::TestContractViewSet::test_filtered_contracts PASSED                              [ 17%]
contracts/tests.py::TestContractViewSet::test_update_contract PASSED                                 [ 19%]
contracts/tests.py::TestContractViewSet::test_update_contract_unauthorized_user PASSED               [ 20%]
events/tests.py::TestEventsApp::test_event_print_details PASSED                                      [ 22%]
events/tests.py::TestEventsApp::test_event_str_representation PASSED                                 [ 23%]
events/tests.py::TestEventsApp::test_save_method PASSED                                              [ 25%]
events/tests.py::TestEventViewSet::test_all_events_details PASSED                                    [ 26%]
events/tests.py::TestEventViewSet::test_create_event PASSED                                          [ 28%]
events/tests.py::TestEventViewSet::test_create_event_already_exists PASSED                           [ 29%]
events/tests.py::TestEventViewSet::test_create_event_contract_not_signed PASSED                      [ 31%]
events/tests.py::TestEventViewSet::test_create_event_unauthorized_user PASSED                        [ 32%]
events/tests.py::TestEventViewSet::test_destroy_event PASSED                                         [ 34%]
events/tests.py::TestEventViewSet::test_destroy_event_unauthorized_user PASSED                       [ 35%]
events/tests.py::TestEventViewSet::test_event_details PASSED                                         [ 37%]
events/tests.py::TestEventViewSet::test_event_details_unauthorized_user PASSED                       [ 38%]
events/tests.py::TestEventViewSet::test_events_list PASSED                                           [ 40%]
events/tests.py::TestEventViewSet::test_events_without_support PASSED                                [ 41%]
events/tests.py::TestEventViewSet::test_update_event PASSED                                          [ 43%]
events/tests.py::TestEventViewSet::test_update_event_unauthorized_user PASSED                        [ 44%]
profiles/tests.py::TestProfilesApp::test_add_client_to_group PASSED                                  [ 46%]
profiles/tests.py::TestProfilesApp::test_assign_sales_contact PASSED                                 [ 47%]
profiles/tests.py::TestProfilesApp::test_create_client1 PASSED                                       [ 49%]
profiles/tests.py::TestProfilesApp::test_create_client2 PASSED                                       [ 50%]
profiles/tests.py::TestProfilesApp::test_create_superuser PASSED                                     [ 52%]
profiles/tests.py::TestProfilesApp::test_create_superuser_invalid_attributes PASSED                  [ 53%]
profiles/tests.py::TestProfilesApp::test_create_user_management PASSED                               [ 55%]
profiles/tests.py::TestProfilesApp::test_create_user_sales PASSED                                    [ 56%]
profiles/tests.py::TestProfilesApp::test_create_user_support PASSED                                  [ 58%]
profiles/tests.py::TestProfilesApp::test_create_user_with_empty_email PASSED                         [ 59%]
profiles/tests.py::TestProfilesApp::test_has_module_perms PASSED                                     [ 61%]
profiles/tests.py::TestProfilesApp::test_has_perm PASSED                                             [ 62%]
profiles/tests.py::TestProfilesApp::test_obtain_jwt_token_url PASSED                                 [ 64%]
profiles/tests.py::TestProfilesApp::test_refresh_jwt_token_url PASSED                                [ 65%]
profiles/tests.py::TestProfilesApp::test_str_method_with_sales_contact PASSED                        [ 67%]
profiles/tests.py::TestLoginViewSet::test_user_login_inactive_account PASSED                         [ 68%]
profiles/tests.py::TestLoginViewSet::test_user_login_invalid_credentials PASSED                      [ 70%]
profiles/tests.py::TestLoginViewSet::test_user_login_successful PASSED                               [ 71%]
profiles/tests.py::TestClientViewSet::test_all_clients_details PASSED                                [ 73%]
profiles/tests.py::TestClientViewSet::test_client_details PASSED                                     [ 74%]
profiles/tests.py::TestClientViewSet::test_client_details_unauthorized_user PASSED                   [ 76%]
profiles/tests.py::TestClientViewSet::test_clients_list PASSED                                       [ 77%]
profiles/tests.py::TestClientViewSet::test_create_client PASSED                                      [ 79%]
profiles/tests.py::TestClientViewSet::test_create_clients_unauthorized_user PASSED                   [ 80%]
profiles/tests.py::TestClientViewSet::test_destroy_client PASSED                                     [ 82%]
profiles/tests.py::TestClientViewSet::test_destroy_client_unauthorized_user PASSED                   [ 83%]
profiles/tests.py::TestClientViewSet::test_update_client PASSED                                      [ 85%]
profiles/tests.py::TestClientViewSet::test_update_client_unauthorized_user PASSED                    [ 86%]
profiles/tests.py::TestUserViewSet::test_all_users_details PASSED                                    [ 88%]
profiles/tests.py::TestUserViewSet::test_create_user PASSED                                          [ 89%]
profiles/tests.py::TestUserViewSet::test_create_user_unauthorized_user PASSED                        [ 91%]
profiles/tests.py::TestUserViewSet::test_destroy_user PASSED                                         [ 92%]
profiles/tests.py::TestUserViewSet::test_destroy_user_unauthorized_user PASSED                       [ 94%]
profiles/tests.py::TestUserViewSet::test_update_user PASSED                                          [ 95%]
profiles/tests.py::TestUserViewSet::test_update_user_unauthorized_user PASSED                        [ 97%]
profiles/tests.py::TestUserViewSet::test_user_details PASSED                                         [ 98%]
profiles/tests.py::TestUserViewSet::test_users_list PASSED                                           [100%]

===================================== 67 passed in 277.36s (0:04:37) ======================================
```   
- Pour afficher plus d'informations sur les tests lors de leurs exécutions vous pouvez utiliser la commande :   

```bash   
$ pytest -v -s
``` 

--------------------------------------------------------------------------------------------------------------------------------

<div id="tests-coverage"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

#### Tests de couverture de code avec Coverage   

- Utilisation de **Coverage** pour mesurer la couverture de code. ➔ [Documentation Coverage](https://coverage.readthedocs.io/en/7.3.2/)   

- Cette commande exécute les tests en utilisant **Coverage** pour collecter les informations de couverture.   

```bash   
$ pytest --cov=.
```   

```bash   
---------- coverage: platform win32, python 3.12.0-final-0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
contracts\models.py      30      1    97%
contracts\views.py       79      5    94%
events\models.py         30      0   100%
events\views.py          88      5    94%
profiles\models.py      130     10    92%
profiles\views.py       146     18    88%
-----------------------------------------
TOTAL                   503     39    92%


===================================== 67 passed in 284.05s (0:04:44) ======================================
```   

Renvoie : **92%** de couverture de code.   

- Pour afficher un rapport de couverture avec plus de détails.   

```bash   
$ pytest --cov=. --cov-report html
```

- Cela générera un dossier ``htmlcov`` dans lequel vous pouvez ouvrir le fichier ``index.html`` pour visualiser un rapport interactif de la couverture de code dans votre navigateur.   

**Rapport Coverage**   

![Rapport Coverage](/static/img/coverage_screen.png)   

--------------------------------------------------------------------------------------------------------------------------------

<div id="rapport-flake8"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Rapport avec flake8   

Tapez dans votre terminal la commande :   

```bash   
$ flake8
```   
- Ne renvoie aucune erreur.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="informations-importantes"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Informations importantes sur les différents fichiers et dossiers   

##### Les dossiers contract, events, profiles   

  - Chacun contient un fichier ``tests.py`` contenant les configurations pour les tests.   
    - ``contracts`` ➔ ([tests.py](contracts/tests.py))   
    - ``events`` ➔ ([tests.py](events/tests.py))   
    - ``profiles`` ➔ ([tests.py](profiles/tests.py))   

##### Les dossiers management/commmands   

  - Chacun contient un fichier contenant les configurations pour le gestionnaire de commandes.   
    - ``contracts`` ➔ ([management_contract.py](/contracts/management/commands/management_contract.py))   
    - ``events`` ➔ ([management_event.py](/events/management/commands/management_event.py))   
    - ``profiles`` ➔ ([management_user.py](/profiles/management/commands/management_user.py))   
    - ``profiles`` ➔ ([management_client.py](/profiles/management/commands/management_client.py))   

##### Le dossier utils   

  - Le dossier contient le fichier ``creating_environment_variables.py`` qui génère le fichier ``.env`` pour les variables d'environnement ([creating_environment_variables.py](utils/creating_environment_variables.py))   

##### Le dossier static   

  - Dossier qui contient qui contient les images et les badges nécessaire à l'application.   
    - ``static`` ➔ ([badges](static/badges))   
    - ``static`` ➔ ([img](static/img))   

##### Le fichier EpicEvents.sql   

  - Le fichier ``EpicEvents.sql`` contient la configuration des tables pour la base de données ➔ ([EpicEvents.sql](EpicEvents.sql))   

##### Le fichier .coveragerc   

  - Le fichier contient la configuration de ``Coverage`` ([.coveragerc](.coveragerc))   

##### Le fichier .flake8   

  - Le fichier contient la configuration de ``Flake8`` ([.flake8](.flake8))   

--------------------------------------------------------------------------------------------------------------------------------

<div id="auteur-contact"></div>
<a href="#top" style="float: right;">Retour en haut ↑</a>

### Auteur et contact   

Pour toute information supplémentaire, vous pouvez me contacter.   
**Bubhux :** bubhuxpaindepice@gmail.com   
