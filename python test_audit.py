import time
import random
import os
from faker import Faker  # Import de la bibliothèque de génération
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialisation de Faker en français
fake = Faker('fr_FR')

# --- CONFIGURATION ---
URL_INSCRIPTION = "https://propulso.great-site.net/inscription.html"
FICHIER_LOGS = "comptes_propulso.txt"
NB_COMPTES_TOTAL = 100

def sauvegarder_compte(nom, email, password):
    """Enregistre les identifiants dans un fichier texte."""
    with open(FICHIER_LOGS, "a", encoding="utf-8") as f:
        f.write(f"Nom: {nom} | Email: {email} | Pass: {password} | Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def executer_inscription(id_client):
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    try:
        print(f"\n[*] Tentative pour le Client n°{id_client}...")
        driver.get(URL_INSCRIPTION)
        
        # 1. Attente du "Challenge" InfinityFree
        time.sleep(10) 

        # 2. GÉNÉRATION DE DONNÉES RÉELLES
        nom_reel = fake.name() # Génère un nom et prénom (ex: 'Marcelle Lefebvre')
        email = fake.free_email() # Génère un email réaliste (gmail, hotmail, etc.)
        password = f"Elite{random.randint(100, 999)}!{random.choice(['Az', 'Er', 'Ty'])}"

        # 3. Remplissage du Nom Complet
        nom_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Marc Koffi')]")))
        nom_field.send_keys(nom_reel)

        # 4. Remplissage de l'Email
        email_field = driver.find_element(By.XPATH, "//input[@type='email']")
        email_field.send_keys(email)

        # 5. Remplissage du Mot de Passe
        pass_field = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_field.send_keys(password)

        # 6. Clic sur le bouton "Rejoindre le Réseau"
        btn_rejoindre = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-auth")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_rejoindre)
        time.sleep(1)
        btn_rejoindre.click()

        # 7. Attente validation
        time.sleep(5)
        
        # Sauvegarde locale avec le vrai nom
        sauvegarder_compte(nom_reel, email, password)
        print(f"[✓] Succès : Compte créé pour {nom_reel} ({email})")

    except Exception as e:
        print(f"[X] Échec pour le Client {id_client} : Erreur technique.")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("====================================================")
    print("   DÉMARRAGE AUTOMATISATION : NOMS RÉALISTES")
    print("====================================================")
    
    for i in range(1, NB_COMPTES_TOTAL + 1):
        executer_inscription(i)
        
        # Pause pour éviter d'être détecté
        pause = random.randint(20, 50)
        print(f"[*] Pause de {pause} secondes...")
        time.sleep(pause)

    print("\n[!] TRAVAIL TERMINÉ.")