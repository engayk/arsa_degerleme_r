import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Arsa Fiyat Analizörü", layout="centered")

st.title("⚖️ Arsa Değer Testi")
st.subheader("Bu fiyat gerçekçi mi, yoksa balon mu?")

# --- GİRDİLER ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗺️ İmar Bilgileri")
    arsa_alani = st.number_input("Arsa Alanı (m²)", value=1000)
    kaks = st.number_input("Emsal (KAKS)", value=2.0, step=0.1)
    birim_maliyet = st.number_input("m² İnşaat Maliyeti (₺)", value=30000, help="Brüt inşaat alanı üzerinden")

with col2:
    st.markdown("### 💰 Piyasa Verileri")
    istenen_arsa_fiyati = st.number_input("Arsa İstenen Satış Fiyatı (₺)", value=50000000)
    bolge_satis_m2 = st.number_input("Bölge Konut Satış m² (₺)", value=100000)

# --- HESAPLAMA ---
# 1. Alanlar
toplam_emsal = arsa_alani * kaks
brut_insaat_alani = toplam_emsal * 1.30  # Otopark, sığınak vb. dahil inşaat alanı
satilabilir_alan = toplam_emsal * 1.15  # Balkonlar dahil satılabilir net alan

# 2. Maliyetler
toplam_insaat_gideri = brut_insaat_alani * birim_maliyet
toplam_yatirim = istenen_arsa_fiyati + toplam_insaat_gideri

# 3. Hasılat ve Kâr
potansiyel_hasilat = satilabilir_alan * bolge_satis_m2
net_kar_zarar = potansiyel_hasilat - toplam_yatirim
kar_orani = (net_kar_zarar / toplam_yatirim) * 100 if toplam_yatirim > 0 else 0

# 4. Kritik Eşik (Sıfır Kâr Noktası)
# Hasılat = Arsa + İnşaat -> Arsa = Hasılat - İnşaat
sifir_kar_arsa_bedeli = potansiyel_hasilat - toplam_insaat_gideri

# --- SONUÇLAR ---
st.divider()

# Renklendirme
color = "green" if kar_orani > 15 else "orange" if kar_orani > 0 else "red"

st.markdown(f"""
### 📊 Analiz Raporu
Bu arsayı **{istenen_arsa_fiyati:,.0f} ₺** fiyatla alıp inşaat yaparsanız:

* **Toplam Satış Hasılatınız:** {potansiyel_hasilat:,.0f} ₺
* **İnşaat Harcamanız:** {toplam_insaat_gideri:,.0f} ₺
* **Net Kârınız / Zararınız:** <span style='color:{color}; font-size:20px; font-weight:bold;'>{net_kar_zarar:,.0f} ₺</span>
* **Kâr Marjınız:** <span style='color:{color}; font-size:20px; font-weight:bold;'>%{kar_orani:.1f}</span>
""", unsafe_allow_html=True)

st.divider()

# Şeytanın Avukatı Köşesi
if sifir_kar_arsa_bedeli > 0:
    st.info(f"💡 **Sıfır Kâr Analizi:** Hiç kâr etmeden, sadece 'para bozmak' için bu inşaatı yapacaksanız, bu arsanın edeceği maksimum değer **{sifir_kar_arsa_bedeli:,.0f} ₺**'dir.")
    
    fark = istenen_arsa_fiyati - sifir_kar_arsa_bedeli
    if fark > 0:
        st.error(f"🚨 **Fazla Ödeme:** Arsa şu an olması gerekenden (0 kâr noktasına göre) **{fark:,.0f} ₺** daha pahalıya satılıyor.")
    else:
        st.success(f"✅ **Fırsat:** Arsa fiyatı, 0 kâr noktasına göre **{abs(fark):,.0f} ₺** daha uygun görünüme sahip.")
else:
    st.error("🚨 **Tehlike:** Bu bölgedeki satış fiyatları, inşaat maliyetini bile karşılamıyor! Arsa bedava olsa bile zarar edebilirsiniz.")