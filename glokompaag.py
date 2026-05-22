import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Glokom Vaka Simülatörü", layout="centered")

# --- OYUN DURUMU (SESSION STATE) BAŞLATMA ---
if 'fibers' not in st.session_state:
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""

def reset_game():
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""

# --- SAĞLIK BARI GÖRSELLEŞTİRME ---
st.title("Vaka 1: Sinsi Tehlike ve Progresyon Yönetimi")

# Oran hesaplama ve renk belirleme
oran = max(0.0, st.session_state.fibers / 1200000.0)
if oran > 0.7:
    renk = "#28a745" # Yeşil
elif oran > 0.4:
    renk = "#ffc107" # Sarı
else:
    renk = "#dc3545" # Kırmızı

# Sağlık barı HTML/CSS
st.markdown(f"### Optik Sinir Rezervi: {int(st.session_state.fibers):,} Lif")
st.markdown(
    f"""
    <div style="width: 100%; background-color: #e9ecef; border-radius: 5px; margin-bottom: 20px;">
        <div style="width: {oran * 100}%; background-color: {renk}; height: 24px; border-radius: 5px; transition: width 0.5s, background-color 0.5s;"></div>
    </div>
    """, unsafe_allow_html=True
)

# --- GERİ BİLDİRİM EKRANI ---
if st.session_state.feedback:
    if st.session_state.feedback_type == "error":
        st.error(st.session_state.feedback)
    elif st.session_state.feedback_type == "success":
        st.success(st.session_state.feedback)

# --- AŞAMALAR ---

# AŞAMA 1: İlk Temas
if st.session_state.stage == 1:
    st.subheader("Aşama 1: Poliklinik Muayenesi")
    st.write("**Hikaye:** 55 yaşında erkek hasta. Şikayeti yok, yakın gözlüğünü değiştirmek için geldi. Ön segment doğal, açılar açık.")
    st.write("**GİB Ölçümü:** Sağ: 22 mmHg, Sol: 23 mmHg.")
    
    q1 = st.radio(
        "Glokom tanısını kesinleştirmeden önce bu aşamada yapılması gereken en kritik İLK tetkik nedir?",
        ["Seçim yapınız...", 
         "A) Vakit kaybetmeden topikal antiglokomatöz tedavi başlamak.", 
         "B) KİBAS şüphesiyle hastayı nörolojiye yönlendirmek.", 
         "C) Pakimetri ile kornea kalınlığını ölçmek."],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn1"):
        if q1 == "C) Pakimetri ile kornea kalınlığını ölçmek.":
            st.session_state.feedback = "Doğru! İnce kornealar GİB'i olduğundan düşük gösterebilir. Pakimetri: 490 mikron. Düzeltilmiş GİB aslında 26 mmHg!"
            st.session_state.feedback_type = "success"
            st.session_state.stage = 2
            st.rerun()
        elif q1 == "A) Vakit kaybetmeden topikal antiglokomatöz tedavi başlamak.":
            st.session_state.fibers -= 100000
            st.session_state.feedback = "Yanlış! Henüz hasar olup olmadığını ve gerçek GİB'i bilmiyorsunuz. (100.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q1 == "B) KİBAS şüphesiyle hastayı nörolojiye yönlendirmek.":
            st.session_state.fibers -= 50000
            st.session_state.feedback = "Yanlış! Hastayı gereksiz yere korkuttunuz ve zaman kaybettirdiniz. (50.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 2: Yapısal Değerlendirme
elif st.session_state.stage == 2:
    st.subheader("Aşama 2: Yapısal Değerlendirme")
    st.write("Gerçek GİB'in yüksek olduğunu tespit ettiniz. Hasar analizi için Fundus ve OCT istediniz.")
    st.write("**Bulgular:** Fundus muayenesinde C/D oranı 0.7, damarlar nazale itilmiş. OCT'de inferior RNFL tabakasında incelme saptandı.")
    
    q2 = st.radio(
        "Normalde 0.4'ün altında olması beklenen C/D oranının bu hastada 0.7 olmasını ve OCT bulgusunu nasıl yorumlarsınız?",
        ["Seçim yapınız...", 
         "A) Fizyolojik büyük çukurluk.", 
         "B) Glokomatöz hasar (Nörodejeneratif süreç)."],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn2"):
        if q2 == "B) Glokomatöz hasar (Nörodejeneratif süreç).":
            st.session_state.feedback = "Doğru! Nörodejeneratif süreci yakaladınız."
            st.session_state.feedback_type = "success"
            st.session_state.stage = 3
            st.rerun()
        elif q2 == "A) Fizyolojik büyük çukurluk.":
            st.session_state.fibers -= 150000
            st.session_state.feedback = "Yanlış! OCT'deki incelmeyi gözden kaçırdınız, tanı gecikti! (150.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 3: Fonksiyonel Değerlendirme
elif st.session_state.stage == 3:
    st.subheader("Aşama 3: Klinik Korelasyon")
    st.write("Yapısal hasarı kesinleştirdiniz. Fonksiyonel karşılığını görmek için Görme Alanı testi istediniz.")
    
    q3 = st.radio(
        "OCT'de saptadığınız 'inferior RNFL incelmesi'ne göre görme alanı testinde hangi spesifik defekti beklersiniz?",
        ["Seçim yapınız...", 
         "A) Santral skotom", 
         "B) Superior arkuat skotom veya nazal step", 
         "C) Bitemporal hemianopsi"],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn3"):
        if q3 == "B) Superior arkuat skotom veya nazal step":
            st.session_state.feedback = "Mükemmel anatomi-klinik korelasyonu! Görme alanında superior arkuat skotom saptandı."
            st.session_state.feedback_type = "success"
            st.session_state.stage = 4
            st.rerun()
        elif q3 == "A) Santral skotom":
            st.session_state.fibers -= 50000
            st.session_state.feedback = "Yanlış! Glokomda santral görme en son etkilenir. (50.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q3 == "C) Bitemporal hemianopsi":
            st.session_state.fibers -= 50000
            st.session_state.feedback = "Yanlış! Bu kiazma lezyonu bulgusudur. (50.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 4: Tanı ve İlk Tedavi
elif st.session_state.stage == 4:
    st.subheader("Aşama 4: Tedavi Planı")
    st.write("Tüm bulguları (Anamnez, Pakimetri, Fundus, OCT, Görme Alanı) birleştirdiniz.")
    st.write("**Kesin Tanı:** Primer Açık Açılı Glokom (PAAG)")
    
    q4 = st.radio(
        "İlk basamak tedavi yaklaşımınız ne olmalıdır?",
        ["Seçim yapınız...", 
         "A) Cerrahi Trabekülektomi", 
         "B) Lazer periferik iridotomi (LPI)", 
         "C) Topikal Antiglokomatöz damla (Örn: Prostaglandin analogları)"],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn4"):
        if q4 == "C) Topikal Antiglokomatöz damla (Örn: Prostaglandin analogları)":
            st.session_state.feedback = "Doğru tedavi seçimi! Monoterapiye başlandı. Bakalım süreç nasıl ilerleyecek..."
            st.session_state.feedback_type = "success"
            st.session_state.stage = 5
            st.rerun()
        elif q4 == "A) Cerrahi Trabekülektomi":
            st.session_state.fibers -= 100000
            st.session_state.feedback = "Yanlış! İlk basamakta invaziv cerrahi tercih edilmez. (100.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q4 == "B) Lazer periferik iridotomi (LPI)":
            st.session_state.fibers -= 100000
            st.session_state.feedback = "Yanlış! Bu kapalı açılı glokom tedavisidir, açılarımız açık! (100.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 5: Progresyon Değerlendirmesi
elif st.session_state.stage == 5:
    st.subheader("⏳ Aşama 5: 6 Ay Sonra Kontrol Muayenesi")
    st.write("Hastanız ilk ilacını düzenli kullanıyor ancak kontrole geldiğinde yapılan tetkiklerde:")
    st.warning("⚠️ Görme alanında progresyon (ilerleme) var ve OCT'de RNFL tabakasında ek incelme saptandı. GİB: 21 mmHg (Hedef basınca ulaşılamamış).")
    
    q5 = st.radio(
        "Mevcut tedavinin yetersiz kaldığı ve hasarın ilerlediği bu durumda ne yapalım?",
        ["Seçim yapınız...", 
         "A) Mevcut ilaçla takibe devam edelim.", 
         "B) Tedaviye yeni (ikinci bir) ilaç ekleyelim.", 
         "C) Doğrudan ilacı kesip cerrahi planlayalım."],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn5"):
        if q5 == "B) Tedaviye yeni (ikinci bir) ilaç ekleyelim.":
            st.session_state.feedback = "Doğru karar! Maksimum medikal tedaviye doğru ilerlemek adına ikinci bir molekül eklediniz."
            st.session_state.feedback_type = "success"
            st.session_state.stage = 6
            st.rerun()
        elif q5 == "A) Mevcut ilaçla takibe devam edelim.":
            st.session_state.fibers -= 150000
            st.session_state.feedback = "Yanlış! Progresyon varken tedavi basamağını artırmamak sinir liflerinin hızla ölmesine neden olur! (150.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q5 == "C) Doğrudan ilacı kesip cerrahi planlayalım.":
            st.session_state.fibers -= 50000
            st.session_state.feedback = "Yanlış! İkinci bir ilaç seçeneği denenmeden doğrudan cerrahiye geçmek ve mevcut ilacı tamamen kesmek uygun değildir. (50.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 6: Stabilizasyon Değerlendirmesi
elif st.session_state.stage == 6:
    st.subheader("⏳ Aşama 6: Bir 6 Ay Sonra Daha (İkinci Muayene)")
    st.write("Tedaviye ikinci ilacı ekledikten sonra hasta tekrar kontrole çağrıldı. Yapılan tetkiklerde:")
    st.info("ℹ️ RNFL tabakasındaki incelmenin DURDUĞU, görme alanı bulgularının tamamen STABİL kaldığı saptandı. GİB: 15 mmHg (Hedef basınca ulaşıldı).")
    
    q6 = st.radio(
        "Progresyonun durduğu ve bulguların stabil seyrettiği bu aşamada sonraki adımınız ne olmalıdır?",
        ["Seçim yapınız...", 
         "A) Yeni ilaç ekleyelim.", 
         "B) Cerrahi yapalım.", 
         "C) Progresyon durduğu için ilaçları keselim.", 
         "D) Mevcut iki ilaçlı tedaviye aynen devam edelim ve stabil seyri izleyelim."],
        index=0
    )
    
    if st.button("Kararı Onayla", key="btn6"):
        if q6 == "D) Mevcut iki ilaçlı tedaviye aynen devam edelim ve stabil seyri izleyelim.":
            st.session_state.feedback = "Mükemmel klinik yaklaşım! Glokomda amaç kaybedileni geri getirmek değil, progresyonu durdurmaktır. Başardınız!"
            st.session_state.feedback_type = "success"
            st.session_state.stage = 7
            st.rerun()
        elif q6 == "A) Yeni ilaç ekleyelim.":
            st.session_state.fibers -= 50000
            st.session_state.feedback = "Yanlış! Zaten stabil olan ve hedef basınca ulaşan hastaya gereksiz yere yan etki ve maliyet getirecek üçüncü bir ilaç eklenmez. (50.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q6 == "B) Cerrahi yapalım.":
            st.session_state.fibers -= 100000
            st.session_state.feedback = "Yanlış! Medikal tedaviyle progresyonu durdurulmuş stabil bir hastada invaziv cerrahi riskine girilmez. (100.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()
        elif q6 == "C) Progresyon durduğu için ilaçları keselim.":
            st.session_state.fibers -= 200000
            st.session_state.feedback = "Büyük Hata! İlaçları keserseniz göz içi basıncı tekrar yükselecek ve progresyon hızla yeniden başlayacaktır! (200.000 lif kaybettiniz)"
            st.session_state.feedback_type = "error"
            st.rerun()

# AŞAMA 7: Final Sonuç Ekranı
elif st.session_state.stage == 7:
    st.header("🏁 VAKA SONUÇ RAPORU")
    if st.session_state.fibers > 800000:
        st.success(f"Tebrikler Doktor! Hastayı {int(st.session_state.fibers):,} sağlıklı sinir lifi ile koruma altına aldınız. Hem sinsi progresyonu doğru hamleyle yakaladınız hem de stabil dönemde tedaviyi başarıyla sürdürdünüz!")
        st.balloons()
    else:
        st.error(f"Vaka tamamlandı ancak hatalı kararlar nedeniyle hastanın optik sinir rezervi {int(st.session_state.fibers):,} life kadar düştü. Takip algoritmasını tekrar gözden geçirmelisiniz.")
        
    if st.button("Oyunu Sıfırla ve Yeniden Başla"):
        reset_game()
        st.rerun()