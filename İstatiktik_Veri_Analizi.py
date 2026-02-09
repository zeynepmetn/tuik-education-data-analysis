import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# CSV dosyasını oku, sadece ilk satırı atla ('Satırlar' satırını)
data = pd.read_csv(r"c:\Users\zeynep metin\Downloads\pivot.csv", sep="|", skiprows=[0]) 

# Başlıkları gözden geçirelim ve yalnızca ilçelere ait olanları seçelim
valid_columns = [col for col in data.columns if "Unnamed" not in col and col != "Satırlar"]

# Geçerli sütunları seç ve veri çerçevesini yeniden oluştur
data = data[valid_columns]

# İlk iki satırı ve son satırı atla
data = data.iloc[2:-1]

# Şimdi, ilçeler ve özellikler ile ilişkili verileri daha düzgün bir formata getireceğiz.

# "melt" işlemi ile veriyi uzun formata getirelim
melted_data = data.melt(id_vars=[], var_name='İlçe', value_name='Değer')

# Özelliklerin listesine göre uygun şekilde 'Özellik' sütununu ekleyelim
melted_data['Özellik'] = ["Erkek ve 15+ Yaş ve Bilinmeyen", 
                           "Erkek ve 15+ Yaş ve Okuma Yazma Bilen", 
                           "Erkek ve 15+ Yaş ve Okuma Yazma Bilmeyen", 
                           "Kadın ve 15+ Yaş ve Bilinmeyen", 
                           "Kadın ve 15+ Yaş ve Okuma Yazma Bilen", 
                           "Kadın ve 15+ Yaş ve Okuma Yazma Bilmeyen"] * (len(melted_data) // 6)

# İlçe ve Özellikler sütunlarını düzenli olarak sıralayalım
melted_data = melted_data[['İlçe', 'Özellik', 'Değer']]

# Veriyi yazdıralım
print("Veri Düzenlenmiş Halde:")
print(melted_data.head(6))

## TEMEL İSTATİSTİKLER 

# Veriyi sayısal değerlere dönüştürelim
melted_data['Değer'] = pd.to_numeric(melted_data['Değer'], errors='coerce')

# 1. Temel İstatistiksel Ölçütler
temel_istatistikler = melted_data.groupby('Özellik')['Değer'].agg(['mean', 'median', 'std', 'var', 'min', 'max', 'count']).reset_index()

# Temel istatistikleri yazdıralım
print("\nTemel İstatistikler:")
print(temel_istatistikler)

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Korelasyon Analizi
# "melted_data" tablosundan geniş formata dönüştürerek korelasyon analizi için hazırlayalım
wide_data = melted_data.pivot_table(index="İlçe", columns="Özellik", values="Değer")

# Korelasyon matrisi hesapla
correlation_matrix = wide_data.corr()

# Korelasyon matrisini yazdır
print("Korelasyon Matrisi:")
print(correlation_matrix)

# Korelasyon matrisini heatmap ile görselleştirelim
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Değişkenler Arasındaki Korelasyon Matrisi", fontsize=16)
plt.show()

#-----------------------------------------------------------------------------------------------------------------------------------------------
## GRAFİKLER 
# Erkeklerin Okuma Yazma Oranının İllere Göre Dağılımı (Çubuk Grafik)
melted_data['İl'] = melted_data['İlçe'].str.split('(').str[0]

# Erkek ve 15+ Yaş ve Okuma Yazma Bilen verilerini filtreleme
filtered_data = melted_data[melted_data['Özellik'] == "Erkek ve 15+ Yaş ve Okuma Yazma Bilen"]

# İllere göre toplam değer
grouped_data = filtered_data.groupby("İl")["Değer"].sum()


plt.figure(figsize=(12, 6))
grouped_data.plot(kind="bar", color="darkorange")

# Grafiği özelleştirme
plt.title("Erkeklerin Okuma Yazma Oranının İllere Göre Dağılımı (Çubuk Grafik)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilen Sayısı (Milyon Kişi)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği gösterme
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------
#Kadınların Okuma Yazma Oranının İllere Göre Dağılımı (Çubuk Grafik)

# Kadın ve 15+ Yaş ve Okuma Yazma Bilen verilerini filtreleme
filtered_data_women = melted_data[melted_data['Özellik'] == "Kadın ve 15+ Yaş ve Okuma Yazma Bilen"]

# İllere göre toplam değeri hesaplama
grouped_data_women = filtered_data_women.groupby("İl")["Değer"].sum()

# Bar grafiği oluşturma
plt.figure(figsize=(12, 6))
grouped_data_women.plot(kind="bar", color="pink")

# Grafiği özelleştirme
plt.title("Kadınların Okuma Yazma Oranının İllere Göre Dağılımı (Çubuk Grafik)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilen Sayısı (Milyon Kişi)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği gösterme
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------

## Kadın ve Erkek Okuma Yazma Durumu (Pasta Grafiği)

# Kadın ve Erkek - Okuma Yazma Bilen, Bilmeyen ve Bilinmeyen kategorilerini filtreleyelim
categories = [
    "Kadın ve 15+ Yaş ve Okuma Yazma Bilen",
    "Kadın ve 15+ Yaş ve Okuma Yazma Bilmeyen",
    "Kadın ve 15+ Yaş ve Bilinmeyen",
    "Erkek ve 15+ Yaş ve Okuma Yazma Bilen",
    "Erkek ve 15+ Yaş ve Okuma Yazma Bilmeyen",
    "Erkek ve 15+ Yaş ve Bilinmeyen"
]

# Verileri filtreleyelim
filtered_data = melted_data[melted_data['Özellik'].isin(categories)]

# Kategorilere göre toplamları hesaplayalım
grouped_data = filtered_data.groupby('Özellik')['Değer'].sum()

# Renkler her kategoriye uygun olacak şekilde manuel atanır
colors = ['#FFB6C1',  # Pembe 
          '#ADD8E6',  # Mavi
          '#90EE90',  # Yeşil 
          '#FFDAB9',  # Turuncu 
          '#E6E6FA',  # Mor
          '#FFFACD']  # Sarı 

# Toplam değeri hesaplayalım ve yüzdeleri çıkaralım
total_value = grouped_data.sum()
percentages = (grouped_data / total_value) * 100

# Pasta grafik oluşturma
plt.figure(figsize=(10, 7))

wedges, _ = plt.pie(
    grouped_data, 
    labels=None,  # Grafik üzerindeki yazıları tamamen kaldır
    startangle=140, 
    colors=colors,  
    wedgeprops={'edgecolor': 'black'},  # Dilim kenarlarına renk ekleyelim
    autopct=None  # Otomatik yüzdelik eklemeyi devre dışı bırakıyoruz
)

# Yazıları grafik dışında (sağda) göstermek için `legend` ekleyelim
plt.legend(
    labels=[f"{cat}: {value:,.0f} ({percent:.1f}%)" for cat, value, percent in zip(categories, grouped_data, percentages)],
    loc="upper left",  # Sol üst tarafa hizala
    fontsize=10,
    frameon=False,  # Çerçevesiz bir görünüm
    bbox_to_anchor=(-0.6, 1),  # Daha sola kaydırma

)

# Başlık ekleyelim
plt.title("Kadın ve Erkek Okuma Yazma Durumu (Pasta Grafiği)", fontsize=14, fontweight='bold')

# Düzeni ayarla ve göster
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------

# Erkeklerin Okuma Yazma Oranlarının İlçelere Göre Dağılımı (Nokta Grafiği)

# Dotplot için veriyi gruplama
plt.figure(figsize=(14, 8))

# Erkekler için okuma yazma oranlarını dotplot ile gösterme
sns.stripplot(data=filtered_data, x='İl', y='Değer', jitter=True, color='blue', alpha=0.7, size=8)

# Grafiği özelleştirme
plt.title("Erkeklerin Okuma Yazma Oranlarının İlçelere Göre Dağılımı (Nokta Grafiği)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilen Sayısı (Milyon Kişi)", fontsize=12)
plt.xticks(rotation=90)  # X eksenindeki etiketleri döndür
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği göster
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------

# Kadınların Okuma Yazma Oranlarının İlçelere Göre Dağılımı (Nokta Grafiği)

# Dotplot için veriyi gruplama
plt.figure(figsize=(14, 8))

# Kadınlar için okuma yazma oranlarını dotplot ile gösterme
filtered_data_women = melted_data[melted_data['Özellik'] == "Kadın ve 15+ Yaş ve Okuma Yazma Bilen"]
sns.stripplot(data=filtered_data_women, x='İl', y='Değer', jitter=True, color='pink', alpha=0.7, size=8)

# Grafiği özelleştirme
plt.title("Kadınların Okuma Yazma Oranlarının İlçelere Göre Dağılımı (Nokta Grafiği)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilen Sayısı (Milyon Kişi)", fontsize=12)
plt.xticks(rotation=90)  # X eksenindeki etiketleri döndür
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği göster
plt.tight_layout()
plt.show()

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Kadın ve Erkeklerin Okuma Yazma Durumu Bilinmeyen Sayısı (Yığılmış Bar Grafiği)

# Yığılmış bar grafiği oluşturma (Okuma Yazma Durumu Bilinmeyen)
unknown_data = melted_data[melted_data['Özellik'].isin([
    "Kadın ve 15+ Yaş ve Bilinmeyen",
    "Erkek ve 15+ Yaş ve Bilinmeyen"
])]

# Veriyi cinsiyete göre gruplama ve toplam değerleri hesaplama
unknown_grouped = unknown_data.groupby(['İl', 'Özellik'])['Değer'].sum().unstack()

# Grafiği oluşturma
unknown_grouped.plot(kind='bar', stacked=True, figsize=(12, 8), color=["pink", "lightblue"])

# Grafiği özelleştirme
plt.title("Kadın ve Erkeklerin Okuma Yazma Durumu Bilinmeyen Sayısı (Yığılmış Bar Grafiği)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Bilinmeyen Sayısı (Milyon Kişi)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Grafiği gösterme
plt.tight_layout()
plt.show()

#-----------------------------------------------------------------------------------------------------------------------------------------------

# İllere Göre Okuma Yazma Bilmeyen Sayısı Isı Haritası

# Okuma yazma bilmeyenler için veriyi filtreleme
uneducated_data = melted_data[
    melted_data['Özellik'].isin(["Erkek ve 15+ Yaş ve Okuma Yazma Bilmeyen", "Kadın ve 15+ Yaş ve Okuma Yazma Bilmeyen"])
]

# Veriyi pivot table ile ısı haritası için uygun forma getirme
heatmap_data_uneducated = uneducated_data.pivot_table(
    values="Değer",  # Değer sütununu al
    index="İl",      # Satırları illere göre grupla
    columns="Özellik",  # Sütunları özelliklere göre grupla
    aggfunc="sum"    # Değerleri topla
)

# Minimum ve maksimum değerleri belirle
vmin = 0
vmax = 35000  # Maksimum skala değeri
ticks = np.arange(5000, vmax + 5000, 10000)  # Skala aralıkları: 5000, 15000, 25000, 35000...

# Isı haritası oluşturma
plt.figure(figsize=(14, 8))
sns.heatmap(
    heatmap_data_uneducated, 
    cmap="coolwarm",        # Renk paleti
    annot=True,             # Hücrelerin içine değer yaz
    fmt=".0f",              # Sayıları tam sayı olarak göster
    cbar=True,              # Sağda renk skalasını göster
    vmin=vmin,              # Minimum değer
    vmax=vmax,              # Maksimum değer
    linewidths=0.5,         # Hücreler arasında ince çizgiler
    cbar_kws={"ticks": ticks}  # Skala için özel etiketler
)

# Grafik başlıkları ve etiketler
plt.title("İllere Göre Okuma Yazma Bilmeyen Sayısı Isı Haritası", fontsize=16)
plt.xlabel("Durum", fontsize=12)
plt.ylabel("İl", fontsize=12)

# Grafiği göster
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------

# İllere Göre Okuma Yazma Bilmeyen Sayısı (Çizgi Grafiği)

# Okuma yazma bilmeyenler için veriyi filtreleme
uneducated_data = melted_data[
    melted_data['Özellik'].isin(["Erkek ve 15+ Yaş ve Okuma Yazma Bilmeyen", "Kadın ve 15+ Yaş ve Okuma Yazma Bilmeyen"])
]

# İllere göre toplam değerleri gruplama
grouped_uneducated_data = uneducated_data.groupby(["İl", "Özellik"])["Değer"].sum().reset_index()

# Çizgi grafiği oluşturma
plt.figure(figsize=(14, 8))

# Erkekler ve kadınlar için ayrı ayrı çizgiler
for feature in grouped_uneducated_data['Özellik'].unique():
    subset = grouped_uneducated_data[grouped_uneducated_data['Özellik'] == feature]
    plt.plot(subset['İl'], subset['Değer'], marker='o', label=feature)

# Grafiği özelleştirme
plt.title("İllere Göre Okuma Yazma Bilmeyen Sayısı (Çizgi Grafiği)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilmeyen Sayısı", fontsize=12)
plt.xticks(rotation=90)  # X eksenindeki etiketleri döndür
plt.grid(axis="y", linestyle="--", alpha=0.7)  # Y ekseninde ızgara çizgileri
plt.legend(title="Durum", fontsize=10)  # Etiketlerle bir açıklama kutusu

# Grafiği göster
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------------------------

# İllere Göre Okuma Yazma Bilen Sayısı (Çizgi Grafiği)

# Okuma Yazma Bilenler İçin Veriyi Filtreleme
educated_data = melted_data[
    melted_data['Özellik'].isin(["Erkek ve 15+ Yaş ve Okuma Yazma Bilen", "Kadın ve 15+ Yaş ve Okuma Yazma Bilen"])
]

# İllere göre toplam değerleri gruplama
grouped_educated_data = educated_data.groupby(["İl", "Özellik"])["Değer"].sum().reset_index()

# Çizgi Grafiği Oluşturma
plt.figure(figsize=(14, 8))

# Erkekler ve kadınlar için ayrı ayrı çizgiler
for feature in grouped_educated_data['Özellik'].unique():
    subset = grouped_educated_data[grouped_educated_data['Özellik'] == feature]
    plt.plot(subset['İl'], subset['Değer'], marker='o', label=feature)

# Grafiği Özelleştirme
plt.title("İllere Göre Okuma Yazma Bilen Sayısı (Çizgi Grafiği)", fontsize=16)
plt.xlabel("İl", fontsize=12)
plt.ylabel("Okuma Yazma Bilen Sayısı", fontsize=12)
plt.xticks(rotation=90)  # X eksenindeki etiketleri döndür
plt.grid(axis="y", linestyle="--", alpha=0.7)  # Y ekseninde ızgara çizgileri
plt.legend(title="Durum", fontsize=10)  # Etiketlerle bir açıklama kutusu

# Grafiği Gösterme
plt.tight_layout()
plt.show()



