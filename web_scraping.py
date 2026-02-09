import requests
from bs4 import BeautifulSoup

# TÜİK eğitim verileri sayfasının URL'si
url = "https://data.tuik.gov.tr/Kategori/GetKategori?p=Egitim,-Kultur,-Spor-ve-Turizm-105"

# Sayfaya GET isteği gönderiyoruz
response = requests.get(url)

# İstek başarılı mı kontrol ediyoruz
if response.status_code == 200:
    # Sayfa içeriğini çekip BeautifulSoup ile parse ediyoruz
    soup = BeautifulSoup(response.content, "html.parser")
    print("TÜİK Eğitim Verileri Sayfası başarıyla çekildi ve parse edildi.")

    # Sayfanın başlığını yazdırıyoruz
    print("Sayfa Başlığı:", soup.title.string)

    # "Veri Tabanları" bağlantısını bulma
    veri_tabanlari_url = None
    for link in soup.find_all('a'):
        if "Veri Tabanları" in link.text:
            veri_tabanlari_url = link['href']
            print("Veri Tabanları bağlantısı bulundu:", veri_tabanlari_url)
            # Eğer bağlantı tam bir URL değilse, ana URL ile birleştirelim
            if not veri_tabanlari_url.startswith("http"):
                veri_tabanlari_url = "https://data.tuik.gov.tr" + veri_tabanlari_url
            break

    if veri_tabanlari_url:
        # Veri Tabanları sayfasına GET isteği gönderiyoruz
        veri_tabanlari_response = requests.get(veri_tabanlari_url)

        # İstek başarılı mı kontrol ediyoruz
        if veri_tabanlari_response.status_code == 200:
            veri_tabanlari_soup = BeautifulSoup(veri_tabanlari_response.content, "html.parser")
            print("Veri Tabanları sayfası başarıyla çekildi.")

            # "Ulusal Eğitim İstatistikleri Veritabanı (M)" bağlantısını bulma
            ulusal_egitim_url = None
            for sub_link in veri_tabanlari_soup.find_all('a'):
                if "Ulusal Eğitim İstatistikleri Veritabanı (M)" in sub_link.text:
                    ulusal_egitim_url = sub_link['href']
                    print("Ulusal Eğitim İstatistikleri Veritabanı (M) bağlantısı bulundu:", ulusal_egitim_url)

                    # Eğer bağlantı tam bir URL değilse, ana URL ile birleştirelim
                    if not ulusal_egitim_url.startswith("http"):
                        ulusal_egitim_url = "https://data.tuik.gov.tr" + ulusal_egitim_url
                    break

            if ulusal_egitim_url:
                # Ulusal Eğitim İstatistikleri Veritabanı sayfasına GET isteği gönderiyoruz
                ulusal_egitim_response = requests.get(ulusal_egitim_url)

                # İstek başarılı mı kontrol ediyoruz
                if ulusal_egitim_response.status_code == 200:
                    ulusal_egitim_soup = BeautifulSoup(ulusal_egitim_response.content, "html.parser")
                    print("Ulusal Eğitim İstatistikleri Veritabanı (M) sayfası başarıyla çekildi.")
                    # Örnek olarak sayfanın başlığını yazdırıyoruz
                    print("Sayfa Başlığı:", ulusal_egitim_soup.title.string)
                else:
                    print("Ulusal Eğitim İstatistikleri Veritabanı (M) sayfasına erişim sağlanamadı. Status kodu:",
                          ulusal_egitim_response.status_code)
            else:
                print("Ulusal Eğitim İstatistikleri Veritabanı (M) bağlantısı bulunamadı.")
        else:
            print("Veri Tabanları sayfasına erişim sağlanamadı. Status kodu:", veri_tabanlari_response.status_code)
    else:
        print("Veri Tabanları bağlantısı bulunamadı.")
else:
    print("TÜİK Eğitim Verileri sayfasına erişim sağlanamadı. Status kodu:", response.status_code)
