import os
import re
import nltk
from nltk.corpus import stopwords
import zipfile
import mysql.connector as mysql

# Fonction pour dézipper les fichiers
def unzip_files_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                    print(f"Extracted {file_path}")
                except zipfile.BadZipFile:
                    print(f"Skipped {file_path} as it's not a valid zip file.")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Fonction pour nettoyer le contenu des fichiers SRT
def clean_srt_content(content):
    # Suppression des timestamps
    content = re.sub(timestamp_pattern, '', content)
    # Suppression des étoiles
    content = content.replace('*', '')
    # Suppression des chiffres et de la ponctuation
    content = re.sub(r'[\d\.,:;?!]+', '', content)
    # Suppression des espaces en double
    content = re.sub(r'\s+', ' ', content)
    # Suppression des espaces en début et fin de ligne
    content = content.strip()
    # Division du texte en lignes
    lignes = re.split(r'\n+', content)
    # Suppression des mots vides pour chaque ligne
    for i, ligne in enumerate(lignes):
        mots = ligne.split()
        mots_sans_stopwords = [mot for mot in mots if mot.lower() not in stop_words]
        lignes[i] = ' '.join(mots_sans_stopwords)
    return '\n'.join(lignes)

# Chemin vers le répertoire principal
repertoire_principal = r'C:\Users\Baran\OneDrive\Bureau\SAE5\sous-titres'

# Expression régulière pour les timestamps
timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')

# Parcours de chaque sous-répertoire dans le répertoire principal
for repertoire in os.listdir(repertoire_principal):
    chemin_repertoire = os.path.join(repertoire_principal, repertoire)

    # Dézipper les fichiers dans le sous-répertoire
    unzip_files_in_directory(chemin_repertoire)

    # Parcours de chaque fichier SRT dans le sous-répertoire
    for fichier in os.listdir(chemin_repertoire):
        if fichier.endswith('.srt'):
            chemin_fichier = os.path.join(chemin_repertoire, fichier)

            # Détermination de la langue des sous-titres
            if "VF" in fichier:
                stop_words = set(stopwords.words('french'))
            elif "VO" in fichier:
                stop_words = set(stopwords.words('english'))
            else:
                stop_words = set(stopwords.words('english'))

            # Lecture et nettoyage du contenu du fichier
            with open(chemin_fichier, 'r', encoding='latin-1') as f:
                contenu = f.read()
            contenu_nettoye = clean_srt_content(contenu)

            # Écriture du contenu nettoyé dans le fichier
            with open(chemin_fichier, 'w', encoding='latin-1') as f:
                f.write(contenu_nettoye)
            print(f"Nettoyage du fichier {chemin_fichier} terminé.")
