import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Glokom Vaka Simülatörü", layout="centered")

# --- OYUN DURUMU (SESSION STATE) BAŞLATMA ---
if 'current_case' not in st.session_state:
    st.session_state.current_case = None # None: Ana Menü, 1: Vaka 1, 2: Vaka 2
if 'fibers' not in st.session_state:
    st.session_state.fibers = 1200000
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'feedback_type' not in st.session_state:
    st.session_state.feedback_type = ""

# Oyunu tamamen sıfırlayıp Ana Menüye dönme fonksiyonu
def reset_to_menu():
    st.session_state.current_case = None
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""

# Seçilen veya rastgele gelen vakayı başlatma fonksiyonu
def start_case(case_number):
    st.session_state.current_case = case_number
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""

# --- ANA MENÜ ---
if st.session_state.current_case is None:
    st.title("👁️ Glokom Klinik Karar Simülatörü")
    st.markdown("Hoş geldiniz Doktor. Bugün nöbettesiniz. Karşınıza sinsi bir poliklinik vakası da gelebilir, acil serviste zamanla yarıştığınız bir kriz de... Hazır mısınız?")
    
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Vaka 1'i Seç (Poliklinik)", use_container_width=True):
            start_case(1)
            st.rerun()
    with col2:
        if st.button("🚨 Vaka 2'yi Seç (Acil Servis)", use_container_width=True):
            start_case(2)
            st.rerun()
    with col3:
        if st.button("🎲 Rastgele Hasta Çağır", use_container_width=True, type="primary"):
            start_case(random.choice([1, 2]))
            st.rerun()

# --- VAKA OYNANIŞ EKRANI (Ortak Sağlık Barı) ---
else:
    # Başlık belirleme
    if st.session_state.current_case == 1:
        st.title("Vaka 1: Sinsi Tehlike (Poliklinik)")
    else:
        st.title("Vaka 2: Acil Serviste Zamanla Yarış")
        
    # Ortak Sağlık Barı
    oran = max(0.0, st.session_state.fibers / 1200000.0)
    renk = "#28a745" if oran > 0.7 else "#ffc107" if oran > 0.4 else "#dc3545"

    st.markdown(f"### Kalan Optik Sinir Rezervi: {int(st.session_state.fibers):,} Lif")
    st.markdown(
        f"""
        <div style="width: 100%; background-color: #e9ecef; border-radius: 5px; margin-bottom: 20px;">
            <div style="width: {oran * 100}%; background-color: {renk}; height: 24px; border-radius: 5px; transition: width 0.5s;"></div>
        </div>
        """, unsafe_allow_html=True
    )

    # Ortak Geri Bildirim Ekranı
    if st.session_state.feedback:
        if st.session_state.feedback_type == "error":
            st.error(st.session_state.feedback)
        else:
            st.success(st.session_state.feedback)
            
    st.button("🔙 Ana Menüye Dön", on_click=reset_to_menu)
    st.write("---")

    # ==========================================
    # VAKA 1 (PAAG) İŞLEYİŞİ
    # ==========================================
    if st.session_state.current_case == 1:
        if st.session_state.stage == 1:
            st.subheader("Aşama 1: Poliklinik Muayenesi")
            st.write("**Hikaye:** 55 yaşında erkek hasta. Şikayeti yok, yakın gözlüğünü değiştirmek için geldi. Ön segment doğal, açılar açık.")
            st.write("**GİB Ölçümü:** Sağ: 22 mmHg, Sol: 23 mmHg.")
            
            q1 = st.radio("Glokom tanısını kesinleştirmeden önce bu aşamada yapılması gereken en kritik İLK tetkik nedir?",
                ["Seçim yapınız...", "A) Topikal tedavi başlamak.", "B) Nörolojiye yönlendirmek.", "C) Pakimetri ile kornea kalınlığını ölçmek."], index=0)
            
            if st.button("Onayla", key="v1_b1"):
                if q1.startswith("C)"):
                    st.session_state.feedback = "Doğru! İnce kornealar GİB'i olduğundan düşük gösterebilir. Pakimetri: 490 mikron. Düzeltilmiş GİB aslında 26 mmHg!"
                    st.session_state.feedback_type = "success"
                    st.session_state.stage = 2
                    st.rerun()
                elif q1.startswith("A)"):
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış! Henüz hasar olup olmadığını bilmiyorsunuz. (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()
                elif q1.startswith("B)"):
                    st.session_state.fibers -= 50000
                    st.session_state.feedback = "Yanlış! Hastaya zaman kaybettirdiniz. (50.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 2:
            st.subheader("Aşama 2: Yapısal Değerlendirme")
            st.write("Fundus muayenesinde C/D oranı 0.7. OCT'de inferior RNFL tabakasında incelme saptandı.")
            
            q2 = st.radio("Normalde 0.4'ün altında olması beklenen C/D oranının 0.7 olmasını nasıl yorumlarsınız?",
                ["Seçim yapınız...", "A) Fizyolojik büyük çukurluk.", "B) Glokomatöz hasar (Nörodejeneratif süreç)."], index=0)
            
            if st.button("Onayla", key="v1_b2"):
                if q2.startswith("B)"):
                    st.session_state.feedback = "Doğru! Nörodejeneratif süreci yakaladınız."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 3; st.rerun()
                else:
                    st.session_state.fibers -= 150000
                    st.session_state.feedback = "Yanlış! OCT'deki incelmeyi gözden kaçırdınız! (150.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 3:
            st.subheader("Aşama 3: Klinik Korelasyon")
            q3 = st.radio("OCT'de 'inferior RNFL incelmesi'ne göre görme alanı testinde hangi defekti beklersiniz?",
                ["Seçim yapınız...", "A) Santral skotom", "B) Superior arkuat skotom veya nazal step", "C) Bitemporal hemianopsi"], index=0)
            
            if st.button("Onayla", key="v1_b3"):
                if q3.startswith("B)"):
                    st.session_state.feedback = "Mükemmel korelasyon!"
                    st.session_state.feedback_type = "success"; st.session_state.stage = 4; st.rerun()
                else:
                    st.session_state.fibers -= 50000
                    st.session_state.feedback = "Yanlış! Glokomda santral veya bitemporal görme alanı ilk etapta tipik değildir. (50.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 4:
            st.subheader("Aşama 4: Tedavi Planı")
            q4 = st.radio("Kesin Tanı: Primer Açık Açılı Glokom (PAAG). İlk basamak tedaviniz ne olmalıdır?",
                ["Seçim yapınız...", "A) Cerrahi Trabekülektomi", "B) Lazer periferik iridotomi (LPI)", "C) Topikal Antiglokomatöz damla"], index=0)
            
            if st.button("Onayla", key="v1_b4"):
                if q4.startswith("C)"):
                    st.session_state.feedback = "Doğru tedavi! Monoterapiye başlandı."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 5; st.rerun()
                else:
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış! LPI kapalı açı içindir, cerrahi ilk seçenek değildir. (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 5:
            st.subheader("⏳ Aşama 5: 6 Ay Sonra Kontrol")
            st.warning("⚠️ Görme alanında progresyon var ve OCT'de RNFL'de ek incelme saptandı. GİB: 21 mmHg.")
            q5 = st.radio("Ne yapalım?", ["Seçim yapınız...", "A) Takibe devam", "B) Yeni (ikinci) ilaç ekle", "C) İlacı kesip cerrahi planla"], index=0)
            
            if st.button("Onayla", key="v1_b5"):
                if q5.startswith("B)"):
                    st.session_state.feedback = "Doğru! Maksimum medikal tedaviye geçiyorsunuz."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 6; st.rerun()
                else:
                    st.session_state.fibers -= 150000
                    st.session_state.feedback = "Yanlış hamle! Progresyon varken basamak artırılmalıdır. (150.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 6:
            st.subheader("⏳ Aşama 6: Bir 6 Ay Sonra Daha")
            st.info("ℹ️ İnceme durdu, görme alanı STABİL. GİB: 15 mmHg.")
            q6 = st.radio("Sonraki adımınız nedir?", ["Seçim yapınız...", "A) Yeni ilaç ekle", "B) Cerrahi yapalım", "C) İlaçları keselim", "D) Mevcut tedaviye aynen devam"], index=0)
            
            if st.button("Onayla", key="v1_b6"):
                if q6.startswith("D)"):
                    st.session_state.feedback = "Harika! Progresyonu durdurdunuz."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 7; st.rerun()
                else:
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Hatalı karar! Stabil hastanın tedavisini bozmayın. (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 7:
            st.header("🏁 POLİKLİNİK VAKA SONUCU")
            if st.session_state.fibers > 800000:
                st.success(f"Tebrikler Doktor! Sinsi progresyonu yönettiniz. Kalan Lif: {int(st.session_state.fibers):,}")
                st.balloons()
            else:
                st.error(f"Başarısız! Optik sinir rezervi {int(st.session_state.fibers):,} life düştü.")


    # ==========================================
    # VAKA 2 (AAKG) İŞLEYİŞİ
    # ==========================================
    elif st.session_state.current_case == 2:
        if st.session_state.stage == 1:
            st.subheader("Aşama 1: Triage ve Anamnez")
            st.write("**Hikaye:** 60 yaşında, +4.00 D hipermetrop Çinli kadın turist. Şiddetli baş ağrısı, kusma ve loş ışıkta puslu görme.")
            
            q1 = st.radio("En olası ön tanınız nedir?", 
                ["Seçim yapınız...", "A) İdyopatik intrakraniyal hipertansiyon", "B) Santral retinal arter tıkanıklığı", "C) Akut açı kapanması glokomu"], index=0)
            
            if st.button("Onayla", key="v2_b1"):
                if q1.startswith("C)"):
                    st.session_state.feedback = "Doğru! Kusursuz fırtına: Hipermetropi, ileri yaş, Asya ırkı, loş ışık."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 2; st.rerun()
                elif q1.startswith("A)"):
                    st.session_state.fibers -= 300000
                    st.session_state.feedback = "Ölümcül Hata! Nörolojiye sevk edip zaman kaybettirdiniz! (300.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()
                elif q1.startswith("B)"):
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış tanı. (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 2:
            st.subheader("Aşama 2: Fizik Muayene")
            q2 = st.radio("Sol gözde hangi bulgu üçlüsünü beklersiniz?", 
                ["Seçim yapınız...", "A) Kiraz kırmızısı leke", "B) Konjunktival hiperemi, bulanık kornea, middilate pupilla", "C) Derin ön kamara, miyozis"], index=0)
            
            if st.button("Onayla", key="v2_b2"):
                if q2.startswith("B)"):
                    st.session_state.feedback = "Doğru bulgu! GİB: 60 mmHg."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 3; st.rerun()
                else:
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış bulgu! (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 3:
            st.subheader("Aşama 3: İlk Medikal Müdahale Kararı")
            st.error("GİB 60 mmHg! Acil düşürülmesi gerekiyor.")
            q3 = st.radio("Aşağıdakilerden hangisini İLK ANDA KESİNLİKLE VERMEMELİSİNİZ?", 
                ["Seçim yapınız...", "A) İntravenöz Mannitol", "B) Topikal Beta Blokörler", "C) Topikal Pilokarpin"], index=0)
            
            if st.button("Onayla", key="v2_b3"):
                if q3.startswith("C)"):
                    st.session_state.feedback = "Çok doğru! İlk anda Pilokarpin verilmez."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 4; st.rerun()
                else:
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış! O ajanı kullanmalıyız. Kontrendike olanı bulun. (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 4:
            st.subheader("Aşama 4: İskemi Tuzağının Nedeni")
            q4 = st.radio("Neden ilk anda Pilokarpin etkisizdir?", 
                ["Seçim yapınız...", "A) Kornea ödemi engeller.", "B) Aköz üretimi artar.", "C) Yüksek basınç nedeniyle iris sfinkter kasında iskemi gelişmiştir."], index=0)
            
            if st.button("Onayla", key="v2_b4"):
                if q4.startswith("C)"):
                    st.session_state.feedback = "Mükemmel! İskemi çözülmeden kas kasılamaz."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 5; st.rerun()
                else:
                    st.session_state.fibers -= 150000
                    st.session_state.feedback = "Yanlış! İskemi tuzağına düştünüz. (150.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 5:
            st.subheader("Aşama 5: Kesin Çözüm ve Profilaksi")
            st.write("GİB düştü, kriz kırıldı.")
            q5 = st.radio("Tekrarlamasını önlemek ve diğer gözü korumak için KESİN (küratif) tedaviniz nedir?", 
                ["Seçim yapınız...", "A) Ömür boyu Pilokarpin", "B) Lazer Periferik İridotomi (LPI)", "C) Cerrahi Trabekülektomi"], index=0)
            
            if st.button("Onayla", key="v2_b5"):
                if q5.startswith("B)"):
                    st.session_state.feedback = "Doğru Karar! Her iki göze LPI yapıldı."
                    st.session_state.feedback_type = "success"; st.session_state.stage = 6; st.rerun()
                else:
                    st.session_state.fibers -= 100000
                    st.session_state.feedback = "Yanlış tedavi seçimi. LPI şarttır! (100.000 lif kaybettiniz)"
                    st.session_state.feedback_type = "error"; st.rerun()

        elif st.session_state.stage == 6:
            st.header("🏁 ACİL SERVİS VAKA SONUCU")
            if st.session_state.fibers > 800000:
                st.success(f"Tebrikler Doktor! Krizi başarıyla atlattınız. Kalan Lif: {int(st.session_state.fibers):,}")
                st.balloons()
            else:
                st.error(f"Kriz atlatıldı ancak gecikmeler yüzünden rezerv {int(st.session_state.fibers):,} life düştü.")
