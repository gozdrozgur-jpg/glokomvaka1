import streamlit as st
import random
import csv
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Glokom Klinik Sınavı", layout="centered")

# --- OYUN DURUMU (SESSION STATE) BAŞLATMA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_no' not in st.session_state:
    st.session_state.student_no = ""
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
if 'exam_finished' not in st.session_state:
    st.session_state.exam_finished = False

# Sonucu CSV dosyasına kaydetme fonksiyonu
def kayit_olustur(vaka_adi, skor):
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dosya_adi = "sinav_sonuclari.csv"
    try:
        with open(dosya_adi, mode="a", newline="", encoding="utf-8") as dosya:
            yazici = csv.writer(dosya)
            yazici.writerow([zaman, st.session_state.student_no, st.session_state.student_name, vaka_adi, skor])
    except Exception as e:
        st.error(f"Kayıt sırasında bir hata oluştu: {e}")

def reset_to_menu():
    st.session_state.current_case = None
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""
    st.session_state.exam_finished = False

def start_case(case_number):
    st.session_state.current_case = case_number
    st.session_state.fibers = 1200000
    st.session_state.stage = 1
    st.session_state.feedback = ""
    st.session_state.feedback_type = ""
    st.session_state.exam_finished = False

# --- GİRİŞ / KİMLİK DOĞRULAMA EKRANI ---
if not st.session_state.logged_in:
    st.title("Süleyman Demirel Üniversitesi Tıp Fakültesi")
    st.subheader("Göz Hastalıkları - Glokom Simülasyon Sınavı")
    st.write("Lütfen sınava başlamadan önce bilgilerinizi eksiksiz giriniz. Tüm işlemleriniz ve kararlarınız arka planda kayıt altına alınacaktır.")
    
    with st.form("login_form"):
        ogrenci_adi = st.text_input("Adınız ve Soyadınız:")
        ogrenci_numarasi = st.text_input("Öğrenci Numaranız:")
        submit = st.form_submit_button("Sisteme Giriş Yap")
        
        if submit:
            if ogrenci_adi.strip() == "" or ogrenci_numarasi.strip() == "":
                st.error("Lütfen ad, soyad ve öğrenci numarası alanlarını doldurunuz!")
            else:
                st.session_state.student_name = ogrenci_adi
                st.session_state.student_no = ogrenci_numarasi
                st.session_state.logged_in = True
                # CSV dosyası yoksa başlıkları oluştur
                try:
                    with open("sinav_sonuclari.csv", mode="x", newline="", encoding="utf-8") as dosya:
                        yazici = csv.writer(dosya)
                        yazici.writerow(["Tarih_Saat", "Ogrenci_No", "Ad_Soyad", "Vaka", "Kalan_Lif_Skoru"])
                except FileExistsError:
                    pass
                st.rerun()

# --- ANA MENÜ (ÖĞRENCİ SEÇİMİ) ---
elif st.session_state.logged_in and st.session_state.current_case is None:
    st.title("Sınav Modülü")
    st.success(f"Giriş Başarılı: {st.session_state.student_name} ({st.session_state.student_no})")
    st.markdown("Doktor, acil serviste ve poliklinikte bekleyen hastalar var. Sınavınızı başlatmak için rastgele bir hasta çağırın veya doğrudan yönlendirildiğiniz vakayı seçin.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📁 Vaka 1 (Poliklinik)", use_container_width=True):
            start_case(1)
            st.rerun()
    with col2:
        if st.button("🚨 Vaka 2 (Acil Servis)", use_container_width=True):
            start_case(2)
            st.rerun()
    with col3:
        if st.button("🎲 Rastgele Hasta Çağır", use_container_width=True, type="primary"):
            start_case(random.choice([1, 2]))
            st.rerun()

# --- VAKA OYNANIŞ EKRANI ---
else:
    if st.session_state.current_case == 1:
        st.title("Vaka 1: Sinsi Tehlike (Poliklinik)")
        vaka_adi = "Vaka 1 (PAAG)"
    else:
        st.title("Vaka 2: Acil Serviste Zamanla Yarış")
        vaka_adi = "Vaka 2 (Akut Açı Kapanması)"
        
    oran = max(0.0, st.session_state.fibers / 1200000.0)
    renk = "#28a745" if oran > 0.7 else "#ffc107" if oran > 0.4 else "#dc3545"

    st.markdown(f"### Kalan Optik Sinir Rezervi (SKOR): {int(st.session_state.fibers):,} Lif")
    st.markdown(
        f"""
        <div style="width: 100%; background-color: #e9ecef; border-radius: 5px; margin-bottom: 20px;">
            <div style="width: {oran * 100}%; background-color: {renk}; height: 24px; border-radius: 5px; transition: width 0.5s;"></div>
        </div>
        """, unsafe_allow_html=True
    )

    if st.session_state.feedback:
        if st.session_state.feedback_type == "error":
            st.error(st.session_state.feedback)
        else:
            st.success(st.session_state.feedback)
            
    # ==========================================
    # VAKA 1 (PAAG) İŞLEYİŞİ
    # ==========================================
    if st.session_state.current_case == 1:
        if st.session_state.stage == 1:
            st.write("**GİB Ölçümü:** Sağ: 22 mmHg, Sol: 23 mmHg.")
            q1 = st.radio("Bu aşamada yapılması gereken en kritik İLK tetkik nedir?",
                ["Seçim yapınız...", "A) Topikal tedavi başlamak.", "B) Nörolojiye yönlendirmek.", "C) Pakimetri ile kornea kalınlığını ölçmek."], index=0)
            if st.button("Onayla"):
                if q1.startswith("C)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 2
                    st.session_state.feedback = "Doğru! Düzeltilmiş GİB 26 mmHg."
                elif q1.startswith("A)"):
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! Hasar olup olmadığını bilmiyorsunuz. (-100K Lif)"
                elif q1.startswith("B)"):
                    st.session_state.fibers -= 50000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! Gereksiz sevk. (-50K Lif)"
                st.rerun()

        elif st.session_state.stage == 2:
            st.write("Fundus muayenesinde C/D oranı 0.7. OCT'de inferior RNFL tabakasında incelme saptandı.")
            q2 = st.radio("Normalde 0.4'ün altında olması beklenen C/D oranının 0.7 olmasını nasıl yorumlarsınız?",
                ["Seçim yapınız...", "A) Fizyolojik büyük çukurluk.", "B) Glokomatöz hasar (Nörodejeneratif süreç)."], index=0)
            if st.button("Onayla"):
                if q2.startswith("B)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 3
                    st.session_state.feedback = "Doğru! Nörodejeneratif süreci yakaladınız."
                else:
                    st.session_state.fibers -= 150000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! Nörodejenerasyonu atladınız. (-150K Lif)"
                st.rerun()

        elif st.session_state.stage == 3:
            q3 = st.radio("OCT'de 'inferior RNFL incelmesi'ne göre görme alanı testinde hangi defekti beklersiniz?",
                ["Seçim yapınız...", "A) Santral skotom", "B) Superior arkuat skotom veya nazal step", "C) Bitemporal hemianopsi"], index=0)
            if st.button("Onayla"):
                if q3.startswith("B)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 4
                    st.session_state.feedback = "Mükemmel klinik korelasyon!"
                else:
                    st.session_state.fibers -= 50000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış defekt alanı. (-50K Lif)"
                st.rerun()

        elif st.session_state.stage == 4:
            q4 = st.radio("Kesin Tanı: PAAG. İlk basamak tedaviniz ne olmalıdır?",
                ["Seçim yapınız...", "A) Cerrahi Trabekülektomi", "B) Lazer periferik iridotomi (LPI)", "C) Topikal Antiglokomatöz damla"], index=0)
            if st.button("Onayla"):
                if q4.startswith("C)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 5
                    st.session_state.feedback = "Doğru tedavi! Monoterapiye başlandı."
                else:
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış tedavi basamağı. (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 5:
            st.warning("⚠️ Görme alanında progresyon var ve GİB: 21 mmHg.")
            q5 = st.radio("Ne yapalım?", ["Seçim yapınız...", "A) Takibe devam", "B) Yeni (ikinci) ilaç ekle", "C) İlacı kesip cerrahi planla"], index=0)
            if st.button("Onayla"):
                if q5.startswith("B)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 6
                    st.session_state.feedback = "Doğru! Basamak artırıldı."
                else:
                    st.session_state.fibers -= 150000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! Progresyon önlenemedi. (-150K Lif)"
                st.rerun()

        elif st.session_state.stage == 6:
            st.info("ℹ️ İnceme durdu, görme alanı STABİL. GİB: 15 mmHg.")
            q6 = st.radio("Sonraki adımınız nedir?", ["Seçim yapınız...", "A) Yeni ilaç ekle", "B) Cerrahi yapalım", "C) İlaçları keselim", "D) Mevcut tedaviye aynen devam"], index=0)
            if st.button("Onayla"):
                if q6.startswith("D)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 7
                    st.session_state.feedback = "Harika! Progresyonu durdurdunuz."
                else:
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Hatalı karar! Stabilite bozuldu. (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 7:
            if not st.session_state.exam_finished:
                kayit_olustur(vaka_adi, int(st.session_state.fibers))
                st.session_state.exam_finished = True
                
            st.header("🏁 SINAV TAMAMLANDI")
            st.success(f"Nihai Skorunuz: {int(st.session_state.fibers):,} Lif")
            
            # Sınav Sonuç Belgesi İndirme (Öğrenci Makbuzu)
            belge_icerigi = f"""SULEYMAN DEMIREL UNIVERSITESI TIP FAKULTESI
GOZ HASTALIKLARI - GLOKOM SIMULASYON SINAVI SONUC BELGESI
---------------------------------------------------
Tarih/Saat    : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Ogrenci No    : {st.session_state.student_no}
Ad Soyad      : {st.session_state.student_name}
Cozulen Vaka  : {vaka_adi}
Nihai Skor    : {int(st.session_state.fibers):,} Optik Sinir Lifi
---------------------------------------------------
Bu belge elektronik olarak uretilmistir."""
            
            st.download_button(
                label="📥 Sınav Sonuç Belgesini İndir",
                data=belge_icerigi,
                file_name=f"SinavSonucu_{st.session_state.student_no}.txt",
                mime="text/plain"
            )

    # ==========================================
    # VAKA 2 (AAKG) İŞLEYİŞİ
    # ==========================================
    elif st.session_state.current_case == 2:
        if st.session_state.stage == 1:
            st.write("**Hikaye:** 60 yaşında, +4.00 D hipermetrop Çinli kadın turist. Şiddetli baş ağrısı, kusma ve loş ışıkta puslu görme.")
            q1 = st.radio("En olası ön tanınız nedir?", 
                ["Seçim yapınız...", "A) İdyopatik intrakraniyal hipertansiyon", "B) Santral retinal arter tıkanıklığı", "C) Akut açı kapanması glokomu"], index=0)
            if st.button("Onayla"):
                if q1.startswith("C)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 2
                    st.session_state.feedback = "Doğru ön tanı!"
                elif q1.startswith("A)"):
                    st.session_state.fibers -= 300000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Ölümcül Hata! Nörolojiye sevk ettiniz! (-300K Lif)"
                elif q1.startswith("B)"):
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış tanı. (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 2:
            q2 = st.radio("Sol gözde hangi bulgu üçlüsünü beklersiniz?", 
                ["Seçim yapınız...", "A) Kiraz kırmızısı leke", "B) Konjunktival hiperemi, bulanık kornea, middilate pupilla", "C) Derin ön kamara, miyozis"], index=0)
            if st.button("Onayla"):
                if q2.startswith("B)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 3
                    st.session_state.feedback = "Doğru bulgu! GİB: 60 mmHg."
                else:
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış bulgu eşleştirmesi! (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 3:
            st.error("GİB 60 mmHg! Acil düşürülmesi gerekiyor.")
            q3 = st.radio("Aşağıdakilerden hangisini İLK ANDA KESİNLİKLE VERMEMELİSİNİZ?", 
                ["Seçim yapınız...", "A) İntravenöz Mannitol", "B) Topikal Beta Blokörler", "C) Topikal Pilokarpin"], index=0)
            if st.button("Onayla"):
                if q3.startswith("C)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 4
                    st.session_state.feedback = "Doğru tespit!"
                else:
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! Kontrendike ajanı bulamadınız. (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 4:
            q4 = st.radio("Neden ilk anda Pilokarpin etkisizdir?", 
                ["Seçim yapınız...", "A) Kornea ödemi engeller.", "B) Aköz üretimi artar.", "C) Yüksek basınç nedeniyle iris sfinkter kasında iskemi gelişmiştir."], index=0)
            if st.button("Onayla"):
                if q4.startswith("C)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 5
                    st.session_state.feedback = "Mükemmel! İskemi tuzağını çözdünüz."
                else:
                    st.session_state.fibers -= 150000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış! İskemi atlandı. (-150K Lif)"
                st.rerun()

        elif st.session_state.stage == 5:
            q5 = st.radio("Tekrarlamasını önlemek ve diğer gözü korumak için KESİN (küratif) tedaviniz nedir?", 
                ["Seçim yapınız...", "A) Ömür boyu Pilokarpin", "B) Lazer Periferik İridotomi (LPI)", "C) Cerrahi Trabekülektomi"], index=0)
            if st.button("Onayla"):
                if q5.startswith("B)"):
                    st.session_state.feedback_type = "success"; st.session_state.stage = 6
                    st.session_state.feedback = "Doğru Karar! Her iki göze LPI yapıldı."
                else:
                    st.session_state.fibers -= 100000; st.session_state.feedback_type = "error"
                    st.session_state.feedback = "Yanlış tedavi seçimi. (-100K Lif)"
                st.rerun()

        elif st.session_state.stage == 6:
            if not st.session_state.exam_finished:
                kayit_olustur(vaka_adi, int(st.session_state.fibers))
                st.session_state.exam_finished = True
                
            st.header("🏁 SINAV TAMAMLANDI")
            st.success(f"Nihai Skorunuz: {int(st.session_state.fibers):,} Lif")
            
            # Sınav Sonuç Belgesi İndirme
            belge_icerigi = f"""SULEYMAN DEMIREL UNIVERSITESI TIP FAKULTESI
GOZ HASTALIKLARI - GLOKOM SIMULASYON SINAVI SONUC BELGESI
---------------------------------------------------
Tarih/Saat    : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Ogrenci No    : {st.session_state.student_no}
Ad Soyad      : {st.session_state.student_name}
Cozulen Vaka  : {vaka_adi}
Nihai Skor    : {int(st.session_state.fibers):,} Optik Sinir Lifi
---------------------------------------------------
Bu belge elektronik olarak uretilmistir."""
            
            st.download_button(
                label="📥 Sınav Sonuç Belgesini İndir",
                data=belge_icerigi,
                file_name=f"SinavSonucu_{st.session_state.student_no}.txt",
                mime="text/plain"
            )
