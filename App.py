# from Models.All_Classes import *

# Application()

# l = "['ISM2023/DK062001-0206', 'ISM2023/DK062001-0206', 'ISM2023/DK062001-0206']"
# def listeAppend(liste: str, element) -> str:
#     i = f"{element}" if f"{element}".isdigit() else f"\'{element}\'"
#     return liste[:-1] +','+ i +']'
import json
data =  [
    {
      "Ann\u00e9e-Scolaire": "2022-2023",
      "niveau": "L2",
      "fili\u00e8re": "GLRS",
      "Classe": "L2-GLRS",
      "P\u00e9riode": {
        "Session 3": {
          "2": [20, 20],
          "3": [14, None],
          "4": [None, None],
          "5": [None, None],
          "6": [None, None],
          "7": [None, None],
          "8": [None, None],
          "9": [None, None],
          "10": [None, None],
          "11": [None, None],
          "12": [12, None],
          "13": [None, None]
        },
        "Session 4": {
          "14": [None, None],
          "15": [None, None],
          "16": [None, None],
          "17": [None, None],
          "18": [None, None],
          "19": [None, None],
          "20": [None, None],
          "26": [None, None]
        }
      },
      "Commentaire": [
        {
          "Date": "02-06-2023",
          "Heure": "02:46",
          "Auteur": "ISM2023/DK280241-0602",
          "Commentaire": "Bonjour Madame comme allez vous ?"
        },
        {
          "Date": "02-06-2023",
          "Heure": "03:25",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Je vais bien merci et toi ?"
        },
        {
          "Date": "03-06-2023",
          "Heure": "02:48",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Bonjour Moustapha, pour l'examen de Algo Avanc\u00e9e & Structures de Donn\u00e9es, tu as eu 14."
        },
        {
          "Date": "03-06-2023",
          "Heure": "02:57",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Bonjour Moustapha, pour l'examen de Programmation Web 1:, PhP, tu as eu 12."
        },
        {
          "Date": "03-06-2023",
          "Heure": "02:59",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Bonjour Moustapha, pour l'examen de Administration Syst\u00e8me Windows de la session Session 3, tu as eu 15."
        },
        {
          "Date": "03-06-2023",
          "Heure": "03:01",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Bonjour Moustapha, pour l'examen de Administration Syst\u00e8me Windows de la session Session 3, tu as eu 20."
        },
        {
          "Date": "03-06-2023",
          "Heure": "03:01",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "Bonjour Moustapha, pour l'\u00e9valuation de Administration Syst\u00e8me Windows de la session Session 3, tu as eu 20."
        },
        {
          "Date": "03-06-2023",
          "Heure": "03:05",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "hello"
        },
        {
          "Date": "03-06-2023",
          "Heure": "03:05",
          "Auteur": "ISM2023/staff1-0601",
          "Commentaire": "m"
        }
      ]
    }
  ]
with open("ISM2023_DK240225_0602.json", 'w', encoding= 'utf-8') as f:
    json.dump(data, f, indent=4)
    