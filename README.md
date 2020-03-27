# OSINT - Sensibilisation

## Description du projet
Ce projet d'OSINT - Sensibilisation permet de récolter des informations en sources ouvertes à propos d'une entreprise. Ces informations serviront à créer un questionnaire de sensibilisation, personnalisé par rapport à l'entreprise cible, mais pourront également servir à créer une campagne de phishing.

## Installation et dépendances

### Dépendances
* Linux
* Python 3
* Firefox
* Geckodriver
* Whois

### Installation
#### Installation de Geckodriver
* Rendez-vous sur le site (https://github.com/mozilla/geckodriver/releases) et téléchargez Geckodriver.
* Placez l'archive dans le répertoire /opt/.
* Décompressez l'archive : `tar -xzvf archive`.
* Rendez-le exécutable : `chmod u+x geckodriver`.
* Modifiez le PATH : `export PATH=$PATH:/opt/`.

#### Installation de Whois
* Lancer la commande suivante : `sudo apt-get install whois`.

#### Installation du projet
* Téléchargez le projet depuis Github : `git clone https://github.com/PiaMardaye/osint`.
* Rendez-vous dans le dossier du projet : `cd osint`.
* Lancer l'installation : `python3 setup.py`.

## Utilisation
* Lancer le projet comme suit : `python3 scan.py -n nom_de_l'entreprise -d nom_de_domaine_de_l'entreprise`.

*Si le nom de l'entreprise contient plusieurs mots, écrivez le entre guillemets.*


## Améliorations à faire et fonctionnalités à ajouter
* Pouvoir entrer un nom d'entreprise composé de plusieurs mots.
* Faire une recherche [SHODAN](https://shodan.io) pour chacune des adresses IP trouvées.
* Vérifier les emails récoltés sur [Mailtester](https://mailtester.com).
* Récolter des informations sur les employés : nom, fonction, email, âge, hobbies, etc.

**Tous les résultats sont pour l'instant à placer dans un dictionnaire Python : un pour les résultats SHODAN, un pour les emails, et un pour les informations du personnel.**

## Collaboratrices
* Pia MARDAYE
* Assiya EL HARCHI

