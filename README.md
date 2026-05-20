# Veri Merkezi (Data Center) Akıllı Soğutma ve Enerji Yönetimi

Bu proje, gerçek dünya problemi olan veri merkezlerindeki aşırı enerji tüketimi ve ısıl optimizasyon sorununa çözüm üretmek amacıyla geliştirilmiş **Bulanık Mantık (Fuzzy Logic)** tabanlı bir akıllı kontrolcü sistemidir. Python ve Streamlit mimarisi kullanılarak dinamik bir grafiksel arayüz (GUI) üzerinden sunulmuştur.

Bulanık Mantık Dersi Dönem Projesi gereksinimlerini eksiksiz şekilde karşılamaktadır.

 Proje Özellikleri

- **3 Giriş Parametresi:** Ortalama CPU Yükü (%), Kabin İçi Sıcaklık (°C), Kabin Bağıl Nemi (%)
- **1 Çıkış Parametresi:** CRAC Klima Fan Hızı (%)
- **Uzman Kural Tabanı:** En az 15 adet (toplam 15) özel kurgulanmış EĞER-İSE (IF-THEN) kural yapısı.
- **Mamdani Çıkarım Mekanizması:** Minimum (t-norm) ve Maksimum (s-norm) operatörleri ile kural aktivasyonları.
- **Durulaştırma (Defuzzification):** Kararlı ve pürüzsüz sonuçlar üreten **Ağırlık Merkezi (Centroid)** metodu.
- **Dinamik Web Arayüzü:** Giriş değerlerinin slider üzerinden anlık değiştirilebilmesi ve çıktı çizgilerinin grafikler üzerinde gerçek zamanlı güncellenmesi.



  Kurulum ve Çalıştırma

Projenin bilgisayarınızda sorunsuz çalışabilmesi için aşağıdaki adımları takip ediniz.

 1. Gerekli Kütüphanelerin Yüklenmesi
Terminal veya komut satırını açarak sistem bağımlılıklarını tek seferde yükleyin:

```bash
pip install streamlit numpy matplotlib scikit-fuzzy networkx

2. Uygulamanın Başlatılması
Proje klasörünün içine giderek terminalden Streamlit sunucusunu tetikleyin:
streamlit run app.py

Sistem Kural Tabanı Yapısı
Sistemde tanımlı olan ve arayüz üzerinden de listelenebilen kuralların özeti şu şekildedir:

Kural ID,EĞER (CPU Yükü),VE (Kabin Sıcaklığı),VE (Nem Oranı),İSE (Fan Hızı)
Kural 1,DÜŞÜK,SERİN,İDEAL,MİNİMUM
Kural 2,DÜŞÜK,ILIK,İDEAL,OPTİMİZE
Kural 3,DÜŞÜK,SICAK,İDEAL,MAKSİMUM
Kural 4,NORMAL,SERİN,İDEAL,MİNİMUM
Kural 5,NORMAL,ILIK,İDEAL,OPTİMİZE
Kural 6,NORMAL,SICAK,İDEAL,MAKSİMUM
Kural 7,YOĞUN,SERİN,İDEAL,OPTİMİZE
Kural 8,YOĞUN,ILIK,İDEAL,MAKSİMUM
Kural 9,YOĞUN,SICAK,İDEAL,MAKSİMUM
Kural 10,DÜŞÜK,ILIK,DÜŞÜK,OPTİMİZE
Kural 11,NORMAL,ILIK,DÜŞÜK,OPTİMİZE
Kural 12,YOĞUN,ILIK,DÜŞÜK,MAKSİMUM
Kural 13,DÜŞÜK,ILIK,YÜKSEK,MAKSİMUM
Kural 14,NORMAL,ILIK,YÜKSEK,MAKSİMUM
Kural 15,YOĞUN,SICAK,YÜKSEK,MAKSİMUM
