'''noms_series = []

for root,dirs,files in os.walk(path,topdown=True):
    for name in dirs:
        noms_series.append(name)
        print(name)

for nom in noms_series:
    query = "INSERT INTO series (series_name) VALUES ('{}')".format(nom.replace("'", "\\'"))
    cursor.execute(query)
    conn.commit()
    print("insertion de la serie " + nom)
conn.close()'''
import os
import nltk
from nltk.corpus import stopwords
import os
import zipfile
import mysql.connector as mysql
import re

def unzip_files_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)  # Extraire dans le même répertoire que le fichier zip
                    print(f"Extracted {file_path}")
                except zipfile.BadZipFile:
                    print(f"Skipped {file_path} as it's not a valid zip file.")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


# Chemin du répertoire contenant les fichiers .zip
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"
unzip_files_in_directory(path)






# Chemin du répertoire contenant les fichiers .srt
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"


# Chemin du répertoire contenant les fichiers .zip
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"
unzip_files_in_directory(path)


def clean_srt_content(content):
    cleaned_lines = []
    for line in content.splitlines():
        # Sauter les chiffres
        if line.isdigit():
            continue
        # Ignorer les liens
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
            continue
        # Supprimer les balises HTML
        line = re.sub(r'<.*?>', '', line)
        # Sauter les lignes vides
        if not line.strip():
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def remove_stopwords_from_content(content, language):
    # Charger les stopwords pour la langue spécifiée
    if language == 'VO':
        stop_words = set(stopwords.words('english'))
    elif language == 'VF':
        stop_words = set(stopwords.words('french'))
    elif language == 'EN':
        stop_words = set(stopwords.words('english'))
    else:
        return content

    # Tokeniser le contenu et supprimer les stopwords
    words = nltk.word_tokenize(content)
    cleaned_words = [word for word in words if word.lower() not in stop_words]

    return ' '.join(cleaned_words)

def clean_srt_content(content):
    cleaned_lines = []
    for line in content.splitlines():
        # Sauter les chiffres (numéros de ligne)
        if line.isdigit():
            continue
        # Supprimer les horodatages
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def clean_srt_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    cleaned_content = clean_srt_content(content)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

# Chemin du répertoire contenant les fichiers .srt
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"

for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.srt'):
            clean_srt_file(os.path.join(root, name))
            print('Nettoyage du fichier {}'.format(name))

def clean_srt_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    cleaned_content = clean_srt_content(content)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

# Chemin du répertoire contenant les fichiers .srt
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"

for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.srt'):
            clean_srt_file(os.path.join(root, name))
            print('Nettoyage du fichier {}'.format(name))
            
def clean_srt_file(filepath):
    # Déterminer la langue du fichier en fonction de son nom
    if 'VO' in filepath:
        language = 'VO'
    elif 'VF' in filepath:
        language = 'VF'
    elif 'EN' in filepath:
        language = 'EN'
    else:
        return

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    cleaned_content = remove_stopwords_from_content(content, language)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)



conn = mysql.connect(host="localhost",user="root",password="",database="films")
cursor = conn.cursor()
path = "C:\\Users\\Baran\\OneDrive\\Bureau\\SAE5\\sous-titres"



nltk.download('punkt')





