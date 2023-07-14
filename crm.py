import importlib.util
import subprocess
import os
import requests
# Gerekli modüllerin adlarını ve yüklenmesi gereken sürümleri belirtin
required_modules = {
    'tkinter': 'tk',
    'sqlite3': 'sqlite3',
    'PIL': 'Pillow'
}

# Eksik modülleri kontrol etme ve yükleme işlemi
for module, package_name in required_modules.items():
    spec = importlib.util.find_spec(module)
    if spec is None:

        subprocess.check_call(['pip', 'install', package_name])
    else:
        pass



def download_image_and_openfloder():
    if os.path.exists("C:/image_crm") == False:
        os.makedirs("C:/image_crm")
    else:
        pass

    liste_link_file = [
        "https://github.com/trojanx6/vt/raw/main/add_user_logo.png",
        "https://github.com/trojanx6/vt/raw/main/crm.jpg",
        "https://github.com/trojanx6/vt/raw/main/del_user.png",
        "https://github.com/trojanx6/vt/raw/main/logo.jpeg"
    ]

    if os.path.exists("C:/image_crm/" + str(liste_link_file[0].split("/")[-1])) == False:
        new_requests_content = requests.get(liste_link_file[0]).content
        with open("C:/image_crm/" + liste_link_file[0].split("/")[-1], "wb") as f:
            f.write(new_requests_content)

    if os.path.exists("C:/image_crm/" + str(liste_link_file[1].split("/")[-1])) == False:
        new_requests_content_crm = requests.get(liste_link_file[1]).content
        with open("C:/image_crm/" + str(liste_link_file[1].split("/")[-1]), "wb") as c:
            c.write(new_requests_content_crm)

    if os.path.exists("C:/image_crm/" + str(liste_link_file[2].split("/")[-1])) == False:
        new_requests_content_del = requests.get(liste_link_file[2]).content
        with open("C:/image_crm/" + str(liste_link_file[2].split("/")[-1]), "wb") as d:
            d.write(new_requests_content_del)

    if os.path.exists("C:/image_crm/" + str(liste_link_file[3].split("/")[-1])) == False:
        new_requests_content_logo = requests.get(liste_link_file[3]).content
        with open("C:/image_crm/" + str(liste_link_file[3].split("/")[-1]), "wb") as l:
            l.write(new_requests_content_logo)


download_image_and_openfloder()


import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

class CRM: # Daha iyi okunabilmesi için class yapısına aldım
    def __init__(self):
        self.root = tk.Tk()  #Kök penceredir bütün pencereler bunun altından oluşur
        self.root.title("CRM Otomasyonu")
        self.root.geometry("1000x800")
        self.root.resizable(width=False, height=False) # Ana Pencerenin Büyütülmesini engeller
        self.root.configure(bg="white") # Arka plan Beyaz olarak ayarlanır "Bg='white'"
        self.conn = sqlite3.connect("C:/image_crm/crm.db") # veritabanı bağlantısı atadık self olan her fonksiyon için
        self.cursor = self.conn.cursor() # imleç olşturdu SQL komutları girmek için
        self.merhaba_yazisi()
        self.musteri_ekle()
        self.musteri_sil()
        self.musteri_info()
        self.root.mainloop()


    def merhaba_yazisi(self):
        # Merhaba yazısını ve resmi gösteren bir etiket oluşturdum
        yazi = tk.Label(self.root, text="WELCOME TO CRM SYSTEM", font=("Arial", 16, "bold"), justify="center",
                        anchor="center",bg="white")
        yazi.pack()
        yazi2 = tk.Label(self.root, text="Seçim Giriniz", font=("Arial", 8, "bold"), bg="white")
        yazi2.pack()

        ## Alt kısım Arka Plana resim ekler, resimi arka plandan bağımsız olarak gösterir
        resim_yolu = "C:/image_crm/crm.jpg"
        resim = Image.open(resim_yolu)
        resim = resim.resize((346, 146))
        resim_tk = ImageTk.PhotoImage(resim)
        resim_etiket = tk.Label(self.root)
        resim_etiket.pack()
        resim_etiket.place(x=300, y=210)
        resim_etiket.configure(image=resim_tk)
        resim_etiket.image = resim_tk


        #DBS gelen iki veriyi yazdıracam
        conn = sqlite3.connect("C:/image_crm/crm.db")
        cursor = conn.cursor()
        puan_sorgusu = "SELECT MemnuniyetPuani FROM SatisBilgileri"
        nerden_buldu_sorgusu = "SELECT NerdenGordu FROM SatisBilgileri"
        cursor.execute(puan_sorgusu)
        result_puan = cursor.fetchall()
        cursor.execute(nerden_buldu_sorgusu)
        result_nerden = cursor.fetchall()

        # Müşterilerin ürünleri bulduğu yerliern ortalaması olarak gösterir
        find_product = []
        for raw in result_nerden:
            product = raw[0]
            find_product.append(product)

        veri = [eleman.lower() for eleman in find_product]  # Verileri küçük harfe dönüştür
        frekanslar = {eleman: veri.count(eleman) for eleman in veri}
        toplam = len(veri)
        oranlar = {eleman: (frekans / toplam) * 100 for eleman, frekans in frekanslar.items()}
        output = ""
        for eleman, oran in oranlar.items():
            output += f"{eleman}: %{int(oran)}\n"
        final = tk.Label(self.root,text=f"Müşterilerin Ürünü Bulduğu yerler\n{output}",font=("Arial", 16, "bold"),bg="white")
        final.pack()
        final.place(x=320,y=580)


        # Müşterilerin Üründen Memnun Oldukları puanları 1-10 arasından seçer ve bunların ortalamasını alır
        puanlar = []  # Puanları tutmak için boş bir liste oluşturun
        for row in result_puan:
            puan = row[0]
            puanlar.append(puan)  # Puanları toplayın ve puanlar listesine ekleyin
        toplam = sum(puanlar)
        ortalama = toplam / len(puanlar)
        yazdir_ortalama = tk.Label(self.root,text=f"Müşteri Memnuniyeti Ortalaması:{ortalama}\n({len(puanlar)}) Müşteriden",font=("Arial", 16, "bold"),bg="white")
        yazdir_ortalama.pack()
        yazdir_ortalama.place(x=220, y=500)



    def open_user_add(self):
        # Kullanıcı ekleme penceresini açan fonksiyon açtım
        self.musteri_ekle_pencere()

    def open_info(self):
        # Kullanıcı bilgileri penceresini açan fonksiyon
        self.musteri_info_pencere()

    def open_delete(self):
        # Kullanıcı silme penceresini açan fonksiyon
        self.musteri_delete_pencere()

    def musteri_ekle(self):
        # Kullanıcı ekleme butonu oluşturdum
        new_button = tk.Button(self.root, text="Kullanıcı Ekle", width=20, height=5, bg="Grey", command=self.open_user_add)
        new_button.pack()
        new_button.place(x=120, y=90)

    def musteri_sil(self):
        # Kullanıcı silme butonu yaptım
        new_button = tk.Button(self.root, text="Kullanıcı Sil", width=20, height=5, bg="Grey", command=self.open_delete)
        new_button.pack()
        new_button.place(x=420, y=90)

    def musteri_info(self):
        # Kullanıcı bilgileri ve ürün ekleme butonu ekledim
        new_button = tk.Button(self.root, text="Kullanıcı Bilgisi ve Ürün Ekle", width=20, height=5, bg="Grey", command=self.open_info)
        new_button.pack()
        new_button.place(x=720, y=90)

    def kaydet(self, ad_entry, soyad_entry, telefon_entry, email_entry): # müşteriyi veritabanına kaydetmek için kaydetr adından bir fonksiyon
        conn = sqlite3.connect("C:/image_crm/crm.db")
        cursor = conn.cursor()
        ad = ad_entry.get()
        soyad = soyad_entry.get()
        telefon = telefon_entry.get()
        email = email_entry.get()

        if not (ad and soyad and telefon and email):  # kullanıcı bir alanı boş bırakırsa eğer uyarı veriecek
            messagebox.showwarning("Uyarı", "Tüm alanları doldurunuz.")
            return
        cursor.execute(f"SELECT COUNT(*) FROM Musteriler WHERE MAIL ='{email}'",)
        result = cursor.fetchone()[0]

        if result > 0:
            messagebox.showwarning("Uyarı", "Bu e-posta adresi zaten mevcut.") # bug olmasın diye eklenen e-posta bir daha eklemiyor uyarı veriyor
            return

        cursor.execute("INSERT INTO  Musteriler (NAME, SURNAME,MAIL, PHONE) VALUES (?, ?, ?, ?)",
                       (ad, soyad, email,telefon)) # veritabanına yazan kod bloğu
        conn.commit()

        # Veritabanı bağlantısını kapat
        conn.close()

        messagebox.showinfo("Bilgi", "Kullanıcı eklendi")
        ad_entry.delete(0, tk.END)
        soyad_entry.delete(0, tk.END)
        telefon_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    def musteri_ekle_pencere(self):
        # Alt pencere (Toplevel) oluştur
        alt_pencere = tk.Toplevel(self.root) # Bu kod bloğu ana pencerye bağlı kalarak yeni bir pencere açar
        alt_pencere.title("User Add")
        alt_pencere.geometry("800x600")
        alt_pencere.resizable(width=False, height=False)
        alt_pencere.configure(bg="white")

        # Pencere içeriği ekle
        label = tk.Label(alt_pencere, text="Yeni Müşteri Ekleme Sayfası", font=("Arial", 16, "bold"))
        label.place(x=300, y=50)
        label.pack()

        # Resim ekle
        resim_yolu_user_add = "C:/image_crm/add_user_logo.png"
        resim_user_add = Image.open(resim_yolu_user_add)
        resim_add = resim_user_add.resize((225, 225))
        resim_tk_add = ImageTk.PhotoImage(resim_add)
        resim_etiket_add = tk.Label(alt_pencere, image=resim_tk_add)
        resim_etiket_add.place(x=300, y=60)
        resim_etiket_add.image = resim_tk_add

        # Müşteri Adı
        ad_label = tk.Label(alt_pencere, text="Müşteri Adı:")
        ad_label.pack()
        ad_label.place(x=5, y=55)
        ad_entry = tk.Entry(alt_pencere, width=40)
        ad_entry.pack()
        ad_entry.place(x=5, y=80)

        # Müşteri Soyadı
        soyad_label = tk.Label(alt_pencere, text="Müşteri Soyadı:")
        soyad_label.pack()
        soyad_label.place(x=5, y=114)
        soyad_entry = tk.Entry(alt_pencere, width=40)
        soyad_entry.pack()
        soyad_entry.place(x=5, y=140)

        # Müşteri E-posta
        email_label = tk.Label(alt_pencere, text="Müşteri E-posta:")
        email_label.pack()
        email_label.place(x=5, y=170)
        email_entry = tk.Entry(alt_pencere, width=40)
        email_entry.pack()
        email_entry.place(x=5, y=197)

        # Müşteri Telefon Numarası
        telefon_label = tk.Label(alt_pencere, text="Müşteri Telefon Numarası:")
        telefon_label.pack()
        telefon_label.place(x=5, y=225)
        telefon_entry = tk.Entry(alt_pencere, width=40)
        telefon_entry.pack()
        telefon_entry.place(x=5, y=250)

        # Geri Dön butonu
        geri_button = tk.Button(alt_pencere, text="Geri Dön", width=10, height=2, bg="Grey",
                                command=alt_pencere.destroy)
        geri_button.pack()
        geri_button.place(x=708, y=13)

        # Kaydet butonu
        kaydet_button = tk.Button(alt_pencere, text="Kaydet", width=10, height=2, bg="Grey",
                                  command=lambda: self.kaydet(ad_entry, soyad_entry, telefon_entry, email_entry))
        kaydet_button.pack()
        kaydet_button.place(x=5, y=280)

    def musteri_delete_pencere(self):
        # Alt pencere (Toplevel) oluştur
        alt_pencere = tk.Toplevel(self.root)
        alt_pencere.title("User Delete")
        alt_pencere.geometry("800x600")
        alt_pencere.resizable(width=False, height=False)

        # Resmi ekle
        resim_yolu_user_del = "C:/image_crm/del_user.png"
        resim_user_del = Image.open(resim_yolu_user_del)
        resim_del = resim_user_del.resize((128, 128))
        resim_tk_del = ImageTk.PhotoImage(resim_del)
        resim_etiket_del = tk.Label(alt_pencere, image=resim_tk_del)
        resim_etiket_del.pack()
        resim_etiket_del.place(x=300, y=50)
        resim_etiket_del.image = resim_tk_del

        # Pencere içeriği
        label = tk.Label(alt_pencere, text="Müşteri Silme Sayfası", font=("Arial", 16, "bold"))
        label.pack()

        # Geri dönüş butonunu ekle
        geri_button = tk.Button(alt_pencere, text="Geri Dön", width=10, height=2, bg="Grey",
                                command=alt_pencere.destroy)
        geri_button.pack()
        geri_button.place(x=708, y=13)

        # Müşteri ID'yi girmek için Entry alanı ekle
        id_label = tk.Label(alt_pencere, text="Müşteri ID:")
        id_label.pack()
        id_label.place(x=10, y=50)
        id_entry = tk.Entry(alt_pencere, width=40)
        id_entry.pack()
        id_entry.place(x=10, y=70)

        # Silme işlemini gerçekleştiren fonksiyon
        def sil():
            musteri_id = id_entry.get()
            conn = sqlite3.connect("C:/image_crm/crm.db")
            cursor = conn.cursor()

            # ID giriş ekranına bir şey girilmez ise burası çalışır
            if not musteri_id:
                messagebox.showwarning("Uyarı", "Müşteri ID'si giriniz.")
                return

            # Müşteriyi veritabanından sil
            cursor.execute("SELECT * FROM Musteriler WHERE ID=?", (musteri_id,))
            row = cursor.fetchone()

            # Eğer girilen ID yok ise uyarı verir
            if row is None:
                messagebox.showwarning("Uyarı", "Müşteri bulunamadı.")
            else:
                cursor.execute("DELETE FROM Musteriler WHERE ID=?", (musteri_id,))
                conn.commit()
                messagebox.showinfo("Bilgi", "Müşteri silindi")

            # ID giriş alanını temizle
            id_entry.delete(0, tk.END)

        # Silme butonu
        sil_button = tk.Button(alt_pencere, text="Sil", width=10, height=2, bg="Grey", command=sil)
        sil_button.pack()
        sil_button.place(x=10, y=110)

    def musteri_info_pencere(self):
        # Alt pencere (Toplevel) oluşturur
        alt_pencere = tk.Toplevel(self.root)
        alt_pencere.title("User info and sales")
        alt_pencere.configure(bg="white")
        alt_pencere.geometry("900x700")
        alt_pencere.resizable(width=False, height=False)

        # Pencere içeriği eklenir
        label_giris = tk.Label(alt_pencere, text="Kullanıcı Bilgi sayfası", font=("Ariel", 15, "bold"), bg="white")
        label_giris.pack()


        # ############################ kullanıcı bilgileri gösteme ##########################
        # Kullanıcı Adı ve İd'si girme yeri
        user_posta = tk.Label(alt_pencere, text="E-posta Adresi Giriniz:", bg="white")
        user_posta.pack()
        user_posta.place(x=10, y=30)
        user_posta_entry = tk.Entry(alt_pencere, width=40)
        user_posta_entry.pack()
        user_posta_entry.place(x=10, y=50)


        def ara():
            mail = user_posta_entry.get()
            conn = sqlite3.connect("C:/image_crm/crm.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM Musteriler WHERE MAIL ='{mail}'")
            result_ = cursor.fetchall()
            if not mail:
                messagebox.showwarning("Uyarı", "Müşteri E-postası'si giriniz.")
                return
            for bilgiler in result_:
                id = tk.Label(alt_pencere, text=f"İd:{bilgiler[0]}",bg="white")
                id.pack()
                id.place(x=280, y=45)
                ad = tk.Label(alt_pencere, text=f"Name:{bilgiler[1]}",bg="white")
                ad.pack()
                ad.place(x=280, y=65)
                soyad = tk.Label(alt_pencere, text=f"Surname:{bilgiler[2]}",bg="white")
                soyad.pack()
                soyad.place(x=280, y=85)
                mail = tk.Label(alt_pencere, text=f"E-Mail:{bilgiler[3]}",bg="white")
                mail.pack()
                mail.place(x=280, y=105)
                phone = tk.Label(alt_pencere, text=f"Phone:{bilgiler[4]}",bg="white")
                phone.pack()
                phone.place(x=280, y=125)
            user_posta_entry.delete(0, tk.END)

        ara_button = tk.Button(alt_pencere, text="Ara", width=10, height=2, bg="Grey", command=ara)
        ara_button.pack()
        ara_button.place(x=10, y=70)

        # #################################### Ürün Ekleme ####################################
        # şatış penceresi
        satis_yazisi = tk.Label(alt_pencere,text="Müşteri Ürün Ekleme",font=("Ariel", 15, "bold"), background="white")
        satis_yazisi.pack()
        satis_yazisi.place(x=353, y=220)


        # Kaydet Butonu sql kaydetme si için
        def kaydet():
            conn = sqlite3.connect("C:/image_crm/crm.db")
            cursor = conn.cursor()
            musteri_id = musteri_id_entry.get()
            satis_urun = satis_urun_entry.get()
            urun_fiyat = urun_fiyat_entry.get()
            urun_stok = urun_stok_entry.get()
            satis_tarih = satis_tarih_entry.get()
            satan_eleman = satan_eleman_entry.get()
            magaza = magaza_entry.get()
            iletisim_turu = iletisim_turu_entry.get()
            memnuniyet_puani = memnuniyet_puani_entry.get()
            nerden_gordu = nerden_gordu_entry.get()

            if not musteri_id or not satis_urun or not urun_fiyat or not urun_stok or not satis_tarih or not satan_eleman or not magaza or not iletisim_turu or not memnuniyet_puani or not nerden_gordu:
                messagebox.showerror("Hata", "Boş alanları doldurunuz!")
            else:
                pass
            cursor.execute("SELECT ID FROM Musteriler WHERE ID = ?", (musteri_id,))
            musteri = cursor.fetchone()

            if musteri:
                # Musteri bulundu, SatisBilgileri tablosuna veri ekle
                satis_veri = (musteri_id , satis_urun, urun_fiyat, urun_stok, satis_tarih, satan_eleman, magaza, iletisim_turu , memnuniyet_puani , nerden_gordu)
                cursor.execute("INSERT INTO SatisBilgileri (MusteriID, Urun, Fiyat, StokDurumu, SatisTarihi, SatanEleman, Magaza, IletisimTuru, MemnuniyetPuani, NerdenGordu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" ,satis_veri)
                conn.commit()
                messagebox.showinfo("Bilgi", "Müşteri ürün eklendi")
                # Veri kaydetme işleminden sonra giriş alanlarını temizle
                musteri_id_entry.delete(0, tk.END)
                satis_urun_entry.delete(0, tk.END)
                urun_fiyat_entry.delete(0, tk.END)
                urun_stok_entry.delete(0, tk.END)
                satis_tarih_entry.delete(0, tk.END)
                satan_eleman_entry.delete(0, tk.END)
                magaza_entry.delete(0, tk.END)
                iletisim_turu_entry.delete(0, tk.END)
                memnuniyet_puani_entry.delete(0, tk.END)
                nerden_gordu_entry.delete(0, tk.END)

        kaydet_buton = tk.Button(alt_pencere, text="Kaydet", command=kaydet)
        kaydet_buton.place(x=10, y=580)

        # İnput Alanları dikey bir şekilde
        musteri_id_label = tk.Label(alt_pencere, text="Müşteri ID:", bg="white")
        musteri_id_label.place(x=10, y=280)
        musteri_id_entry = tk.Entry(alt_pencere, width=20)
        musteri_id_entry.place(x=150, y=280)


        satis_urun_label = tk.Label(alt_pencere, text="Satış Yapılan Ürün:", bg="white")
        satis_urun_label.place(x=10, y=310)
        satis_urun_entry = tk.Entry(alt_pencere, width=20)
        satis_urun_entry.place(x=150, y=310)


        urun_fiyat_label = tk.Label(alt_pencere, text="Ürün Fiyatı:", bg="white")
        urun_fiyat_label.place(x=10, y=340)
        urun_fiyat_entry = tk.Entry(alt_pencere, width=20)
        urun_fiyat_entry.place(x=150, y=340)


        urun_stok_label = tk.Label(alt_pencere, text="Ürün Stok Durumu:", bg="white")
        urun_stok_label.place(x=10, y=370)
        urun_stok_entry = tk.Entry(alt_pencere, width=20)
        urun_stok_entry.place(x=150, y=370)


        satis_tarih_label = tk.Label(alt_pencere, text="Satış Tarihi ve Saati:", bg="white")
        satis_tarih_label.place(x=10, y=400)
        satis_tarih_entry = tk.Entry(alt_pencere, width=20)
        satis_tarih_entry.place(x=150, y=400)


        satan_eleman_label = tk.Label(alt_pencere, text="Satan Eleman:", bg="white")
        satan_eleman_label.place(x=10, y=430)
        satan_eleman_entry = tk.Entry(alt_pencere, width=20)
        satan_eleman_entry.place(x=150, y=430)


        magaza_label = tk.Label(alt_pencere, text="Mağaza:", bg="white")
        magaza_label.place(x=10, y=460)
        magaza_entry = tk.Entry(alt_pencere, width=20)
        magaza_entry.place(x=150, y=460)


        iletisim_turu_label = tk.Label(alt_pencere, text="İletişim Türü:", bg="white")
        iletisim_turu_label.place(x=10, y=490)
        iletisim_turu_entry = tk.Entry(alt_pencere, width=20)
        iletisim_turu_entry.place(x=150, y=490)


        memnuniyet_puani_label = tk.Label(alt_pencere, text="Memnuniyet Puanı:", bg="white")
        memnuniyet_puani_label.place(x=10, y=520)
        memnuniyet_puani_entry = tk.Entry(alt_pencere, width=20)
        memnuniyet_puani_entry.place(x=150, y=520)


        nerden_gordu_label = tk.Label(alt_pencere, text="Nerden Gördü:", bg="white")
        nerden_gordu_label.place(x=10, y=550)
        nerden_gordu_entry = tk.Entry(alt_pencere, width=20)
        nerden_gordu_entry.place(x=150, y=550)


        geri_button = tk.Button(alt_pencere, text="Geri Dön", width=10, height=2, bg="Grey", command=alt_pencere.destroy)
        geri_button.pack()
        geri_button.place(x=800, y=20)

        resim_logo = "C:/image_crm/logo.jpeg"
        resim_user = Image.open(resim_logo)
        resim = resim_user.resize((400, 400))
        resim_tk = ImageTk.PhotoImage(resim)
        resim_etiket = tk.Label(alt_pencere, image=resim_tk)
        resim_etiket.pack()
        resim_etiket.place(x=350, y=260)
        resim_etiket.image = resim_tk
if __name__ == "__main__":
     app = CRM()