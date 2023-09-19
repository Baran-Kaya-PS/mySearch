import os
import re
import nltk
from nltk.corpus import stopwords
import zipfile
#import mysql.connector as mysql
from langdetect import detect
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import FrenchStemmer

#nltk.download('wordnet')

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

def clean_srt_content(content, lemmatizer):
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
    # Suppression des mots vides pour chaque ligne et lemmatisation
    for i, ligne in enumerate(lignes):
        mots = ligne.split()
        mots_sans_stopwords = []
        for mot in mots:
            mot_nettoye = mot.lower()
            if mot_nettoye not in stop_words:
                if lemmatizer:
                    mot_lemmatise = lemmatizer.lemmatize(mot_nettoye)
                else:
                    mot_lemmatise = mot_nettoye
                mots_sans_stopwords.append(mot_lemmatise)
        lignes[i] = ' '.join(mots_sans_stopwords)
    return '\n'.join(lignes)

# Chemin vers le répertoire principal
repertoire_principal = r'C:\Users\tetex\Documents\BUT3 S5\SAE\sous-titres'

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

            # Détection de la langue
            try:
                langue = detect(contenu)
            except:
                langue = "unknown"  # En cas d'échec de la détection
            
            # Détermination des mots vides en fonction de la langue
            if langue == "fr":
                stop_words = set(stopwords.words('french'))
                lemmatizer = WordNetLemmatizer() # Utilisez un lemmatiseur français de votre choix si nécessaire
            elif langue == "en":
                stop_words = set(stopwords.words('english'))
                lemmatizer = None  # Lemmatiseur NLTK pour l'anglais
            else:
                stop_words = set(stopwords.words('english'))
                lemmatizer = None  # Par défaut, utilisez l'anglais

            # Nettoyage du contenu du fichier
            contenu_nettoye = clean_srt_content(contenu, lemmatizer)
            
            # Écriture du contenu nettoyé dans le fichier
            with open(chemin_fichier, 'w', encoding='latin-1') as f:
                f.write(contenu_nettoye)
            print(f"Nettoyage du fichier {chemin_fichier} terminé.")
