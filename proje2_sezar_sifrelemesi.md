# Sezar Şifrelemesi ile Kriptoloji

## Proje Kimliği

| Alan | Bilgi |
|------|-------|
| **Proje Türü** | Bilgisayar Bilimi / Kriptografi |
| **Ana Alan** | Bilişim & Matematik |
| **Tematik Alan** | Veri Güvenliği ve Şifreleme |

---

## Problem / Soru Cümlesi

> **"Tarihte kullanılan Sezar şifreleme yöntemi bilgisayar ile kolayca kırılabilir mi ve bu süreç bize modern kriptografinin neden gerekli olduğunu nasıl açıklar?"**

---

## Özet

Bu proje, MÖ 1. yüzyılda Julius Caesar tarafından kullanılan ve alfabedeki harfleri belirli bir sayı kadar kaydırma prensibine dayanan Sezar şifreleme yöntemini incelemektedir. Öğrenciler hem metni şifreleyebilmekte hem de şifreli bir metni kırmayı deneyebilmektedir. Uygulama, tüm olası anahtarları deneyerek (kaba kuvvet) hangi çözümün Türkçe'ye en yakın olduğunu frekans analizi ile sıralayarak göstermektedir. Bu sayede güvenli şifrelemenin neden yalnızca alfabetik kaydırmadan ibaret olamayacağı somut biçimde ortaya konmaktadır.

---

## Yöntem

### Şifreleme
- Türkçe alfabe (29 harf + boşluk = 30 karakter) kullanılır
- Kullanıcının girdiği metin, rastgele veya seçilen anahtar sayısı kadar kaydırılarak şifrelenir
- Her harf `alfabe[(alfabe.index(harf) - anahtar) % len(alfabe)]` formülüyle dönüştürülür

### Şifre Kırma
- **Kaba Kuvvet:** 0'dan 29'a kadar tüm olası anahtarlar denenir (30 ihtimal)
- **Frekans Analizi (opsiyonel):** Türkçe'de en sık kullanılan harfler (A, E, İ, N) ile şifreli metindeki en sık harf eşleştirilerek olası anahtar daraltılır
- Her çözüm aday kelime listesine göre puanlanır ve en yüksek puan alan üstte gösterilir

### Araçlar
- Python 3.x (mevcut kod tabanı kullanılacak)
- Streamlit (web arayüzü)
- Türkçe yaygın kelime listesi (JSON dosyası)
- Streamlit Community Cloud (yayın)

### Uygulama Akışı
1. Kullanıcı metin girer → şifreleme seçer → şifreli metin ekranda belirir
2. VEYA şifreli metin girer → "Şifreyi Kır" butonuna basar
3. 30 olası çözüm listelenir, en olası Türkçe çözüm vurgulanır
4. Doğruluk skoru (%) gösterilir

---

## Bulgular

- Sezar şifrelemesinin yalnızca 30 olası anahtarı bulunduğundan bilgisayar tüm ihtimalleri milisaniyeler içinde dener.
- Frekans analizi ile anahtar sayısı çoğunlukla ilk 3 tahmin içinde bulunmaktadır.
- Bu sonuç, tek başına alfabe kaydırmasının modern güvenlik için yetersiz olduğunu kanıtlamaktadır.
- Türkçe karakter seti (Ğ, Ş, İ, Ö, Ü, Ç) İngilizce uygulamalardan farklı bir alfabe boyutu gerektirmekte; bu da dile özgü şifreleme tasarımının önemini göstermektedir.

---

## Sonuçlar ve Tartışma

Sezar şifrelemesi tarihsel açıdan önemli olmakla birlikte, günümüz bilgisayarları için son derece kırılgan bir yöntemdir. Bu proje öğrencilerin şifreleme kavramını sezgisel olarak kavramasını sağlarken, aynı zamanda modern kriptografide (AES, RSA) neden çok daha karmaşık matematiğin kullanıldığını sorgulamalarına zemin hazırlar. Veri güvenliği, dijital gizlilik ve siber güvenlik gibi güncel kavramlarla doğrudan ilişkilendirilmiştir.

---

## Stant Düzeni (80x100 cm)

```
┌─────────────────────────────────────────┐
│       SEZAR ŞİFRELEMESİ 🔐              │  ← Başlık
│  "2000 Yıllık Şifreyi Bilgisayar Kırar" │
├────────────────┬────────────────────────┤
│  PROBLEM       │  ÖZET                  │
│  (küçük kutu)  │  (2-3 cümle)           │
├────────────────┴────────────────────────┤
│         YÖNTEM                          │
│  [Alfabe kaydırma şeması - görsel]      │
│  A→D  B→E  C→F  (anahtar=3 örneği)     │
├─────────────────────────────────────────┤
│  BULGULAR                               │
│  30 anahtar → bilgisayar hepsini dener  │
│  [Doğruluk skoru tablosu görseli]       │
├─────────────────────────────────────────┤
│  SONUÇ      │  QR KOD (Streamlit app)  │
└─────────────────────────────────────────┘
```

---

## Mevcut Python Kodu

```python
import random as rn

alfabe = ["A","B","C","Ç","D","E","F","G","Ğ","H","I",
          "İ","J","K","L","M","N","O","Ö","P","R","S",
          "Ş","T","U","Ü","V","Y","Z"," "]

def sifrele(metin, anahtar=None):
    if anahtar is None:
        anahtar = rn.randint(1, len(alfabe)-1)
    sifreler = []
    for harf in metin.upper():
        if harf in alfabe:
            sifreler.append(alfabe[(alfabe.index(harf) - anahtar) % len(alfabe)])
    return ''.join(sifreler), anahtar

def coz(metin):
    sonuclar = []
    for i in range(len(alfabe)):
        cozumler = []
        for karakter in metin:
            if karakter in alfabe:
                anahtar = (alfabe.index(karakter) + i) % len(alfabe)
                cozumler.append(alfabe[anahtar])
        sonuclar.append((i, ''.join(cozumler)))
    return sonuclar
```

---

## Streamlit Uygulaması — Yapılacaklar Listesi

### Genel Yapı
- [ ] İki modlu arayüz: "Şifrele" ve "Şifreyi Kır" sekmeleri (`st.tabs`)
- [ ] Büyük, okunabilir yazı tipi (tablet uyumu)
- [ ] Türkçe karakter desteği doğrulanacak

### Şifreleme Sekmesi
- [ ] `st.text_area` — metin girişi
- [ ] `st.slider` — anahtar seç (1-29) veya "Rastgele" checkbox
- [ ] Şifreli metin büyük kutuda göster
- [ ] Kullanılan anahtar `st.metric` ile göster
- [ ] "Kopyala" butonu

### Şifre Kırma Sekmesi
- [ ] `st.text_area` — şifreli metin girişi
- [ ] "Şifreyi Kır!" butonu
- [ ] 30 olası çözümü `st.dataframe` ile listele
- [ ] En yüksek puanlı çözümü `st.success` kutusuyla vurgula
- [ ] Doğruluk skoru `st.metric` ile göster (%)
- [ ] Skor hesaplama: Türkçe kelime listesiyle eşleşme oranı

### Python Modülleri (eklenecek / düzenlenecek)
- [ ] Mevcut `sifrele()` ve `coz()` fonksiyonlarını Streamlit'e entegre et
- [ ] `turkce_skor(metin, kelime_listesi)` → float döndür
- [ ] `en_iyi_cozum(sonuclar)` → en yüksek skorlu anahtar ve metni döndür
- [ ] `kelimeler.json` dosyası oluştur (yaygın Türkçe kelimeler, 500-1000 adet)

### Deploy
- [ ] GitHub repo: `tubitak-sezar-sifresi`
- [ ] `requirements.txt`: streamlit
- [ ] `kelimeler.json` repoya ekle
- [ ] Streamlit Community Cloud deploy
- [ ] QR kod üret → stanta yapıştır
```
