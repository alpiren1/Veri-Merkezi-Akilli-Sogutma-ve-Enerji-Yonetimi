import streamlit as st
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

st.set_page_config(page_title="Veri Merkezi Bulanik Kontrolcu", layout="wide")
st.title("Veri Merkezi (Data Center) Akilli Sogutma ve Enerji Yonetimi")
st.write("Bulanik Mantik Donem Projesi | Gelistirici: Alpi")

cpu_yuku = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu_yuku')
sicaklik = ctrl.Antecedent(np.arange(15, 56, 1), 'sicaklik')
nem = ctrl.Antecedent(np.arange(0, 101, 1), 'nem')
crac_fan = ctrl.Consequent(np.arange(0, 101, 1), 'crac_fan')

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

soogutma_kontrol = ctrl.ControlSystem(rules)
simulasyon = ctrl.ControlSystemSimulation(soogutma_kontrol)

st.sidebar.header("Telemetri Girisleri")
input_cpu = st.sidebar.slider("Ortalama CPU Yuku (%):", 0, 100, 45)
input_sicaklik = st.sidebar.slider("Kabin Ici Sicaklik (C):", 15, 55, 28)
input_nem = st.sidebar.slider("Kabin Bagil Nemi (%):", 0, 100, 50)

simulasyon.input['cpu_yuku'] = input_cpu
simulasyon.input['sicaklik'] = input_sicaklik
simulasyon.input['nem'] = input_nem

try:
    simulasyon.compute()
    output_fan = simulasyon.output['crac_fan']
except Exception as e:
    output_fan = 0

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Giris Degiskenleri Uyelik Grafikleri")

    fig_cpu, ax_cpu = plt.subplots(figsize=(6, 2.5))
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['dusuk'].mf, 'b', linewidth=1.5, label='Dusuk')
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['normal'].mf, 'g', linewidth=1.5, label='Normal')
    ax_cpu.plot(cpu_yuku.universe, cpu_yuku['yogun'].mf, 'r', linewidth=1.5, label='Yogun')
    ax_cpu.set_title("CPU Yuku Uyelik Kumeleri")
    ax_cpu.axvline(x=input_cpu, color='orange', linestyle='--', label=f'Mevcut: {input_cpu}%')
    ax_cpu.legend()
    st.pyplot(fig_cpu)
    plt.close(fig_cpu)
 
    fig_sic, ax_sic = plt.subplots(figsize=(6, 2.5))
    ax_sic.plot(sicaklik.universe, sicaklik['serin'].mf, 'b', linewidth=1.5, label='Serin')
    ax_sic.plot(sicaklik.universe, sicaklik['ilik'].mf, 'g', linewidth=1.5, label='Ilik')
    ax_sic.plot(sicaklik.universe, sicaklik['sicak'].mf, 'r', linewidth=1.5, label='Sicak')
    ax_sic.set_title("Sicaklik Uyelik Kumeleri")
    ax_sic.axvline(x=input_sicaklik, color='orange', linestyle='--', label=f'Mevcut: {input_sicaklik}C')
    ax_sic.legend()
    st.pyplot(fig_sic)
    plt.close(fig_sic)

    fig_nem, ax_nem = plt.subplots(figsize=(6, 2.5))
    ax_nem.plot(nem.universe, nem['dusuk'].mf, 'b', linewidth=1.5, label='Dusuk')
    ax_nem.plot(nem.universe, nem['ideal'].mf, 'g', linewidth=1.5, label='Ideal')
    ax_nem.plot(nem.universe, nem['yuksek'].mf, 'r', linewidth=1.5, label='Yuksek')
    ax_nem.set_title("Nem Orani Uyelik Kumeleri")
    ax_nem.axvline(x=input_nem, color='orange', linestyle='--', label=f'Mevcut: {input_nem}%')
    ax_nem.legend()
    st.pyplot(fig_nem)
    plt.close(fig_nem)

with col2:
    st.header("Hesaplanan Cikti ve Durulastirma")
    st.metric(label="Onerilen CRAC Fan Hizi", value=f"% {output_fan:.2f}")

    fig_out, ax_out = plt.subplots(figsize=(6, 3.5))
    ax_out.plot(crac_fan.universe, crac_fan['minimum'].mf, 'b', linewidth=1.5, label='Minimum')
    ax_out.plot(crac_fan.universe, crac_fan['optimize'].mf, 'g', linewidth=1.5, label='Optimize')
    ax_out.plot(crac_fan.universe, crac_fan['maksimum'].mf, 'r', linewidth=1.5, label='Maksimum')
    ax_out.set_title("Fan Hizi Durulastirma Grafigi (Centroid)")
    ax_out.axvline(x=output_fan, color='purple', linestyle='-', linewidth=2.5, label=f'Net Cikti: %{output_fan:.1f}')
    ax_out.legend()
    st.pyplot(fig_out)
    plt.close(fig_out)
    
    st.subheader("Senaryo Yorumu")
    if output_fan < 35:
        st.success("Sunucular stabil durumda. Enerji tasarrufu modu aktif: Fanlar minimum hizda.")
    elif 35 <= output_fan <= 70:
        st.warning("Orta duzey isi yuku algilandi. Denge modu aktif: Fanlar optimize hizda.")
    else:
        st.error("Kritik esik! Yuksek CPU veya nem anomalisi. Isil hasari onlemek icin fanlar maksimum hizda!")

st.markdown("---")
st.subheader("Sistem Kural Tabani Yapisi (IF - THEN Yapisi)")

kural_tanimlari = [
    "**EGER** **CPU YUKU** 'DUSUK' **VE** **KABIN SICAKLIGI** 'SERIN' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MINIMUM'",
    "**EGER** **CPU YUKU** 'DUSUK' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'OPTIMIZE'",
    "**EGER** **CPU YUKU** 'DUSUK' **VE** **KABIN SICAKLIGI** 'SICAK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'NORMAL' **VE** **KABIN SICAKLIGI** 'SERIN' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MINIMUM'",
    "**EGER** **CPU YUKU** 'NORMAL' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'OPTIMIZE'",
    "**EGER** **CPU YUKU** 'NORMAL' **VE** **KABIN SICAKLIGI** 'SICAK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'YOGUN' **VE** **KABIN SICAKLIGI** 'SERIN' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'OPTIMIZE'",
    "**EGER** **CPU YUKU** 'YOGUN' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'YOGUN' **VE** **KABIN SICAKLIGI** 'SICAK' **VE** **NEM ORANI** 'IDEAL' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'DUSUK' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'DUSUK' $\\rightarrow$ **FAN HIZI** 'OPTIMIZE'",
    "**EGER** **CPU YUKU** 'NORMAL' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'DUSUK' $\\rightarrow$ **FAN HIZI** 'OPTIMIZE'",
    "**EGER** **CPU YUKU** 'YOGUN' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'DUSUK' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'DUSUK' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'YUKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'NORMAL' **VE** **KABIN SICAKLIGI** 'ILIK' **VE** **NEM ORANI** 'YUKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'",
    "**EGER** **CPU YUKU** 'YOGUN' **VE** **KABIN SICAKLIGI** 'SICAK' **VE** **NEM ORANI** 'YUKSEK' $\\rightarrow$ **FAN HIZI** 'MAKSIMUM'"
]

kural_listesi = []
for i, metin in enumerate(kural_tanimlari, 1):
    kural_listesi.append({
        "Kural ID": f"Kural {i}",
        "Metinsel Kurallar Yapisi": metin
    })

st.table(kural_listesi)
