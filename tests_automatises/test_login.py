from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import time
import os

# 🔧 Configuration
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/resident/login/"
LOG_FILE = "resultat.txt"
PDF_FILE = "resultat.pdf"

# Liste pour stocker les lignes du rapport
rapport_lignes = []

def add_line(message):
    rapport_lignes.append(message)
    print(message)

# 🛠 Configurer le service ChromeDriver
try:
    service = Service(executable_path=r"C:\Windows\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
except Exception as e:
    add_line(f"❌ Échec du démarrage de ChromeDriver : {str(e)}")
    exit(1)

try:
    add_line("➡️ Ouverture de la page de login...")
    driver.get(LOGIN_URL)
    time.sleep(2)

    # 🔍 Saisie du username
    add_line("➡️ Saisie du nom d'utilisateur...")
    username_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys("jamila")

    # 🔑 Saisie du mot de passe
    add_line("➡️ Saisie du mot de passe...")
    password_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys("jamila")

    # 🔘 Clic sur le bouton Login
    add_line("➡️ Clic sur le bouton Login...")
    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    time.sleep(2)

    # ✅ Vérification de la page d'accueil
    add_line("➡️ Vérification de la page d'accueil...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        page_title = driver.find_element(By.TAG_NAME, "h1").text
        add_line(f"✅ Connecté avec succès ! Page d'accueil : {page_title}")

        if any(keyword in page_title.lower() for keyword in ["dashboard", "bienvenue", "accueil", "tableau de bord"]):
            add_line("✅ Page d'accueil valide")
        else:
            add_line("⚠️ Page d'accueil chargée, mais titre inattendu")

    except Exception:
        add_line("❌ Échec de la connexion : page d'accueil non chargée")
        driver.save_screenshot("erreur_login.png")
        add_line("📸 Capture d'écran enregistrée : erreur_login.png")
        raise

    # ✅ Vérifier le logout
    add_line("➡️ Vérification du bouton Logout...")
    try:
        # Essayer de trouver le bouton/lien "Déconnexion"
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Déconnexion']"))
        )
        try:
            logout_link.click()
        except:
            driver.execute_script("arguments[0].click();", logout_link)
        add_line("✅ Déconnexion effectuée via bouton.")
    except Exception:
        # Fallback direct via URL
       
        driver.get(f"{BASE_URL}/resident/logout/")
        add_line("✅ Déconnexion effectuée via URL directe.")

    # Attendre que l'utilisateur soit de retour sur la page login
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        add_line("✅ Déconnexion réussie : retour à la page de login.")
    except Exception as e:
        add_line(f"⚠️ Impossible de vérifier le retour à la page de login : {str(e)}")
        driver.save_screenshot("erreur_logout.png")
        add_line("📸 Capture d'écran enregistrée : erreur_logout.png")

except Exception as e:
    add_line(f"❌ Erreur critique : {str(e)}")
    driver.save_screenshot("erreur_execution.png")
    add_line("📸 Capture d'écran enregistrée : erreur_execution.png")

finally:
    add_line("➡️ Fermeture du navigateur...")
    time.sleep(1)
    driver.quit()

# 📄 Générer le rapport texte
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(rapport_lignes))
add_line(f"📄 Rapport texte généré : {os.path.abspath(LOG_FILE)}")

# 📄 Générer le rapport PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)
for ligne in rapport_lignes:
    ligne_clean = ligne.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 10, txt=ligne_clean, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.output(PDF_FILE)
add_line(f"📄 Rapport PDF généré : {os.path.abspath(PDF_FILE)}")
