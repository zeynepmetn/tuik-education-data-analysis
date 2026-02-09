from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

# ChromeDriver'ın yolu
service = Service(r"c:\Users\zeynep metin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

url = "https://data.tuik.gov.tr/"
driver.get(url)

try:
    # İlk linki bul ve tıkla
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.popCategory[href*='Egitim,-Kultur,-Spor-ve-Turizm-105']"))
    )
    link.click()
    time.sleep(2)
    
    veritabani_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-db-tab"))
    )
    veritabani_link.click()
    time.sleep(2)
   
    egitim_istatistikleri_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bulletin-name"))
    )
    egitim_istatistikleri_link.click()
    time.sleep(3)
    
    # yeni sekmeye gec
    current_tab = driver.current_window_handle
    all_tabs = driver.window_handles
    for tab in all_tabs:
        if tab != current_tab:
            driver.switch_to.window(tab)
            break

    # Yeni sekmedeki elementi bul ve tıkla
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.z-listcell-content"))
    )
    element.click()
    time.sleep(3)
    
    checkboxes = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.z-listitem-checkbox"))
    )
    checkboxes[-1].click() 
    time.sleep(3)

    # Elementin XPath'ini kullan
    xpath_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'okmark.png') and @class='btn-image']"))
    )

    # Görünür hale getir ve tıkla
    driver.execute_script("arguments[0].scrollIntoView();", xpath_button)
    driver.execute_script("arguments[0].click();", xpath_button)
    time.sleep(2)

      # Dinamik id yerine class adı ile butona tıklama
    hepsi_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Hepsi')]"))
    )
    hepsi_button.click() # "Hepsi" butonuna tıklama
    time.sleep(3)
   
    erkek_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'z-label') and text()='Erkek']"))
    )
    erkek_button.click()  # "Erkek" butonuna tıklama
    time.sleep(3)  # Bekleme süresi
    kadın_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'z-label') and text()='Kadın']"))
    )
    kadın_button.click()  # "Kadın" butonuna tıklama
    time.sleep(3) 
    
    yas_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'z-label') and text()='15+ Yaş']"))
    )
    yas_button.click()
    time.sleep(3)

    gosterge_ekle_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Göstergeleri Ekle')]"))
    )
    gosterge_ekle_button.click()
    time.sleep(3)

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//img[contains(@src, 'ileri.png')]]"))
    )
    next_button.click()
    time.sleep(3)

    yil_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'z-listcell-content') and contains(text(), '2023')]//span[contains(@class, 'z-listitem-checkable')]"))
    )
    yil_button.click()
    time.sleep(3)

    ileri_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(., 'İleri')]"))
    )
    
    for button in ileri_buttons:
        if button.is_displayed() and 'İleri' in button.text:
            button.click()
            break
    time.sleep(3)

    turkiye_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//option[text()='İlçe Düzeyi']"))
    )
    turkiye_option.click()  
    time.sleep(2)

    # "HEPSİ" seçeneğini tıklama
    hepsi_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//option[text()='HEPSİ']"))
    )
    hepsi_option.click()  
    time.sleep(2)

    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Düzey')]/span[contains(@class, 'z-listheader-checkable')]"))
    )

    driver.execute_script("arguments[0].click();", checkbox)    
    checkbox.click()
    time.sleep(3)
   
    ileri_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(., 'Rapor Oluştur')]"))
    )
    
    # Butonlardan tıklanabilir olanını seç
    for button in ileri_buttons:
        if button.is_displayed() and 'Rapor Oluştur' in button.text:
            button.click()
            break
    time.sleep(6)
    
    csv_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[contains(@src, 'csv.png')]"))
    )
    csv_button.click()
    time.sleep(3)

except Exception as e:
    print(f"Hata oluştu: {e}")
    traceback.print_exc() 
finally:
    driver.quit()