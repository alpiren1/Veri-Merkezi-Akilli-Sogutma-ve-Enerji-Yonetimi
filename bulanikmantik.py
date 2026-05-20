import streamlit as st
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# 1. Sayfa Ayarları
st.set_page_config(page_title="Veri Merkezi Bulanık Kontrolcü", layout="wide")
st.title("🖥️ Veri Merkezi (Data Center) Akıllı Soğutma ve Enerji Yönetimi")
st.write("Bulanık Mantık Dönem Projesi | Geliştirici: Alpi")

# 2. Evrensel Kümelerin Tanımlanması
cpu_yuku = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu_yuku')
sicaklik = ctrl.Antecedent(np.arange(15, 56, 1), 'sicaklik')
nem = ctrl.Antecedent(np.arange(0, 101, 1), 'nem')
crac_fan = ctrl.Consequent(np.arange(0, 101, 1), 'crac_fan')

# 3. Üyelik Fonksiyonları (Üçgen - trimf)
cpu_yuku['dusuk'] = fuzz.trimf(cpu_yuku.universe, [0, 0, 40])
cpu_yuku['normal'] = fuzz.trimf(cpu_yuku.universe, [30, 50, 70])
cpu_yuku['yogun'] = fuzz.trimf(cpu_yuku.universe, [60, 100, 100])

sicaklik['serin'] = fuzz.trimf(sicaklik.universe, [15, 15, 25])
sicaklik['ilik'] = fuzz.trimf(sicaklik.universe, [22, 30, 38])
sicaklik['sicak'] = fuzz.trimf(sicaklik.universe, [35, 55, 55])

nem['dusuk'] = fuzz.trimf(nem.universe, [0, 0, 45])
nem['ideal'] = fuzz.trimf(nem.universe, [40, 50, 60])
nem['yuksek'] = fuzz.trimf(nem.universe, [55, 100, 100])

crac_fan['minimum'] = fuzz.trimf(crac_fan.universe, [0, 0, 35])
crac_fan['optimize'] = fuzz.trimf(crac_fan.universe, [25, 50, 75])
crac_fan['maksimum'] = fuzz.trimf(crac_fan.universe, [65, 100, 100])

# 4. 15 Adet Akademik Kural Kurulumu
rules = [
    ctrl.Rule(cpu_yuku['dusuk'] & sicaklik['serin'] & nem['ideal'], crac_fan['minimum']),
    ctrl.Rule(cpu_yuku['dusuk'] & sicaklik['ilik'] & nem['ideal'], crac_fan['optimize']),
    ctrl.Rule(cpu_yuku['dusuk'] & sicaklik['sicak'] & nem['ideal'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['normal'] & sicaklik['serin'] & nem['ideal'], crac_fan['minimum']),
    ctrl.Rule(cpu_yuku['normal'] & sicaklik['ilik'] & nem['ideal'], crac_fan['optimize']),
    ctrl.Rule(cpu_yuku['normal'] & sicaklik['sicak'] & nem['ideal'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['yogun'] & sicaklik['serin'] & nem['ideal'], crac_fan['optimize']),
    ctrl.Rule(cpu_yuku['yogun'] & sicaklik['ilik'] & nem['ideal'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['yogun'] & sicaklik['sicak'] & nem['ideal'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['dusuk'] & sicaklik['ilik'] & nem['dusuk'], crac_fan['optimize']),
    ctrl.Rule(cpu_yuku['normal'] & sicaklik['ilik'] & nem['dusuk'], crac_fan['optimize']),
    ctrl.Rule(cpu_yuku['yogun'] & sicaklik['ilik'] & nem['dusuk'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['dusuk'] & sicaklik['ilik'] & nem['yuksek'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['normal'] & sicaklik['ilik'] & nem['yuksek'], crac_fan['maksimum']),
    ctrl.Rule(cpu_yuku['yogun'] & sicaklik['sicak'] & nem['yuksek'], crac_fan['maksimum'])
]

# Çıkarım Motoru Bağlantısı
soogutma_kontrol = ctrl.ControlSystem(rules)
simulasyon = ctrl.ControlSystemSimulation(soogutma_kontrol)

# --- ARAYÜZ (STREAMLIT) ---

st.sidebar.header("🎛️ Telemetri Girişleri")
input_cpu = st.sidebar.slider("Ortalama CPU Yükü (%):", 0, 100, 45)
input_sicaklik = st.sidebar.slider("Kabin İçi Sıcaklık (°C):", 15, 55, 28)
input_nem = st.sidebar.slider("Kabin Bağıl Nemi (%):", 0, 100, 50)

# Simülasyona Girdileri Besle
simulasyon.input['cpu_yuku'] = input_cpu
simulasyon.input['sicaklik'] = input_sicaklik
simulasyon.input['nem'] = input_nem

try:
    simulasyon.compute()
    output_fan = simulasyon.output['crac_fan']
except Exception as e:
    output_fan = 0

# Ekran Düzeni (Sol Sütun: Grafikler, Sağ Sütun: Sonuçlar)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📈 Giriş Değişkenleri Üyelik Grafikleri")
    
    # 1. CPU Yükü Grafiği
    fig_cpu, ax_cpu = plt.subplots(figsize=(6, 2.5))
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['dusuk'].mf, 'b', linewidth=1.5, label='Düşük')
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['normal'].mf, 'g', linewidth=1.5, label='Normal')
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['yogun'].mf, 'r', linewidth=1.5, label='Yoğun')
    ax_cpu.set_title("CPU Yükü Üyelik Kümeleri")
    ax_cpu.axvline(x=input_cpu, color='orange', linestyle='--', label=f'Mevcut: {input_cpu}%')
    ax_cpu.legend()
    st.pyplot(fig_cpu)
    plt.close(fig_cpu)
    
    # 2. Sıcaklık Grafiği
    fig_sic, ax_sic = plt.subplots(figsize=(6, 2.5))
    ax_sic.plot(sicaklik.universe, sicaklik['serin'].mf, 'b', linewidth=1.5, label='Serin')
    ax_sic.plot(sicaklik.universe, sicaklik['ilik'].mf, 'g', linewidth=1.5, label='Ilık')
    ax_sic.plot(sicaklik.universe, sicaklik['sicak'].mf, 'r', linewidth=1.5, label='Sıcak')
    ax_sic.set_title("Sıcaklık Üyelik Kümeleri")
    ax_sic.axvline(x=input_sicaklik, color='orange', linestyle='--', label=f'Mevcut: {input_sicaklik}°C')
    ax_sic.legend()
    st.pyplot(fig_sic)
    plt.close(fig_sic)

    # 3. Nem Grafiği
    fig_nem, ax_nem = plt.subplots(figsize=(6, 2.5))
    ax_nem.plot(nem.universe, nem['dusuk'].mf, 'b', linewidth=1.5, label='Düşük')
    ax_nem.plot(nem.universe, nem['ideal'].mf, 'g', linewidth=1.5, label='İdeal')
    ax_nem.plot(nem.universe, nem['yuksek'].mf, 'r', linewidth=1.5, label='Yüksek')
    ax_nem.set_title("Nem Oranı Üyelik Kümeleri")
    ax_nem.axvline(x=input_nem, color='orange', linestyle='--', label=f'Mevcut: {input_nem}%')
    ax_nem.legend()
    st.pyplot(fig_nem)
    plt.close(fig_nem)

with col2:
    st.header("🎯 Hesaplanan Çıktı ve Durulaştırma")
    st.metric(label="Önerilen CRAC Fan Hızı", value=f"% {output_fan:.2f}")
    
    # 4. Çıktı / Durulaştırma Grafiği
    fig_out, ax_out = plt.subplots(figsize=(6, 3.5))
    ax_out.plot(crac_fan.universe, crac_fan['minimum'].mf, 'b', linewidth=1.5, label='Minimum')
    ax_out.plot(crac_fan.universe, crac_fan['optimize'].mf, 'g', linewidth=1.5, label='Optimize')
    ax_out.plot(crac_fan.universe, crac_fan['maksimum'].mf, 'r', linewidth=1.5, label='Maksimum')
    ax_out.set_title("Fan Hızı Durulaştırma Grafiği (Centroid)")
    ax_out.axvline(x=output_fan, color='purple', linestyle='-', linewidth=2.5, label=f'Net Çıktı: %{output_fan:.1f}')
    ax_out.legend()
    st.pyplot(fig_out)
    plt.close(fig_out)
    
    st.subheader("💡 Senaryo Yorumu")
    if output_fan < 35:
        st.success("Sunucular stabil durumda. Enerji tasarrufu modu aktif: Fanlar minimum hızda.")
    elif 35 <= output_fan <= 70:
        st.warning("Orta düzey ısı yükü algılandı. Denge modu aktif: Fanlar optimize hızda.")
    else:
        st.error("Kritik eşik! Yüksek CPU veya nem anomalisi. Isıl hasarı önlemek için fanlar maksimum hızda!")

# --- GARANTİLİ VE TEMİZ METİN FORMATINDA KURAL TABLOSU ---
st.markdown("---")
st.subheader("📋 Sistem Kural Tabanı Yapısı (IF - THEN Yapısı)")

# Kuralları doğrudan statik ve tertemiz metin olarak tanımlıyoruz (Hata ihtimali %0)
kural_tanimlari = [
    "**EĞER** **CPU YÜKÜ** 'DÜŞÜK' **VE** **KABİN SICAKLIĞI** 'SERİN' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MİNİMUM'",
    "**EĞER** **CPU YÜKÜ** 'DÜŞÜK' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'OPTİMİZE'",
    "**EĞER** **CPU YÜKÜ** 'DÜŞÜK' **VE** **KABİN SICAKLIĞI** 'SICAK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'NORMAL' **VE** **KABİN SICAKLIĞI** 'SERİN' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MİNİMUM'",
    "**EĞER** **CPU YÜKÜ** 'NORMAL' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'OPTİMİZE'",
    "**EĞER** **CPU YÜKÜ** 'NORMAL' **VE** **KABİN SICAKLIĞI** 'SICAK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'YOĞUN' **VE** **KABİN SICAKLIĞI** 'SERİN' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'OPTİMİZE'",
    "**EĞER** **CPU YÜKÜ** 'YOĞUN' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'YOĞUN' **VE** **KABİN SICAKLIĞI** 'SICAK' **VE** **NEM ORANI** 'İDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'DÜŞÜK' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'DÜŞÜK' $\\rightarrow$ **FAN HIZI** 'OPTİMİZE'",
    "**EĞER** **CPU YÜKÜ** 'NORMAL' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'DÜŞÜK' $\\rightarrow$ **FAN HIZI** 'OPTİMİZE'",
    "**EĞER** **CPU YÜKÜ** 'YOĞUN' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'DÜŞÜK' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'DÜŞÜK' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'YÜKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'NORMAL' **VE** **KABİN SICAKLIĞI** 'ILIK' **VE** **NEM ORANI** 'YÜKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'",
    "**EĞER** **CPU YÜKÜ** 'YOĞUN' **VE** **KABİN SICAKLIĞI** 'SICAK' **VE** **NEM ORANI** 'YÜKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSİMUM'"
]

temiz_kural_listesi = []
for i, metin in enumerate(kural_tanimlari, 1):
    temiz_kural_listesi.append({
        "Kural ID": f"Kural {i}",
        "Metinsel Kurallar Yapısı": metin
    })

st.table(temiz_kural_listesi)