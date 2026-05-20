# PROJE RAPORU: "SEZAR ŞİFRELEME: 2000 Yıllık Şifrenin Kaba Kuvvet ile Çözümü ve Modern Şifre Güvenliğiyle Karşılaştırması"

---

**Problem/Soru Cümlesi:**
MÖ 1. yüzyılda Julius Caesar tarafından icat edilen ve harfleri alfabede belirli sayıda kaydırarak çalışan Sezar Şifreleme yöntemi, bilgisayarın tüm olası anahtarları sırayla denemesi (kaba kuvvet) ile kaç adımda kırılabilir? Bu yöntemin ne kadar kolay kırılabildiği anlaşıldığında, gerçekten kırılması güç bir şifre oluşturmak için harf, rakam ve sembol kullanımı kaba kuvvet adım sayısını nasıl etkiler?

---

**Özet:**
TYMM Bilişim Teknolojileri dersinin *"Bilgi güvenliğini kavrar ve güçlü şifreler oluşturur"* ile Matematik dersinin *"Üslü sayıları problemlerin çözümünde kullanır"* öğrenme çıktılarını birleştirerek bu web sitesini hazırladık.

Projenin özünde **Sezar Şifreleme** yöntemi ve bu yöntemin kaba kuvvetle kırılması yer almaktadır. Julius Caesar, MÖ 1. yüzyılda askeri mesajlarını gizlemek için her harfi alfabede belirli bir sayı kadar ileri kaydıran bu yöntemi kullanmıştır. Örneğin anahtar 3 ise "A" harfi "D" olur, "B" harfi "E" olur. Şifreyi çözmek için bu kaydırma miktarının, yani anahtarın bilinmesi gerekir. Sitemizde kullanıcılar istedikleri Türkçe metni seçtikleri bir anahtarla şifreleyebilir, şifreli mesajları çözebilir ve ardından bilgisayarın tüm olası anahtarları sırayla deneyerek (kaba kuvvet yöntemiyle) şifreyi nasıl kırdığını adım adım izleyebilir.

Türkçe alfabesi 29 harf ve boşluk karakteriyle birlikte 30 karakterlik bir havuz oluşturduğundan Sezar şifresinin yalnızca **30 olası anahtarı** vardır. Bilgisayar bu 30 anahtarın tamamını deneyerek doğru mesajı Türkçe kelime listesiyle eşleştirmekte ve şifreyi kırmaktadır. Bu sonuç, Sezar şifrelemesinin bilgisayar karşısında ne denli korumasız olduğunu açıkça ortaya koymaktadır.

Buradan hareketle projenin ikinci sorusuna geçtik: peki gerçekten kırılması güç bir şifre nasıl oluşturulur? Bunun yanıtını bulmak için 8 karakterlik bir şifreye harf, rakam ve sembol eklendikçe bilgisayarın kaba kuvvetle kırmak için atması gereken adım sayısını hesapladık. Şifre havuzu büyüdükçe deneme sayısının üslü sayılar matematiğiyle nasıl astronomik boyutlara ulaştığını sitemizde görselleştirdik.

---

**Yöntem:**
Projede iki aşamalı bir yöntem izlendi; ikinci aşama doğrudan birincinin bulgusu üzerine kuruldu.

**Birinci Aşama — Sezar Şifrelemesi ve Kaba Kuvvet Kırma:**
Web sitesine Türkçe alfabesi (29 harf + boşluk = 30 karakter) temel alınarak Sezar şifreleme algoritması kodlandı. Şifreleme işlemi her harf için `alfabe[(alfabe.index(harf) - anahtar) % 30]` formülüyle, çözme işlemi ise `alfabe[(alfabe.index(harf) + anahtar) % 30]` formülüyle gerçekleştirildi. Kaba kuvvet kırma aşamasında bilgisayar 0'dan 29'a kadar tüm olası anahtarları sırayla denedi; her denemede elde edilen metni, önceden hazırlanmış Türkçe kelime listesiyle karşılaştırarak bir puan hesapladı. En yüksek puanı alan çözüm "en olası doğru metin" olarak önerildi. Her deneme bir adım olarak sayıldı ve toplam adım sayısı kaydedildi.

**İkinci Aşama — Havuz Büyüklüğü ve Üslü Sayı Hesaplama:**
Sezar şifrelemesinin yalnızca 30 adımda kırıldığı görüldükten sonra "güçlü bir şifre kaç adımda kırılır?" sorusu araştırıldı. 8 karakterlik bir şifreyi kırmak için bilgisayarın en kötü ihtimalde atacağı maksimum adım sayısını hesaplamak amacıyla `Havuz Büyüklüğü⁸` formülü kullanıldı. Web sitesindeki araç bu formülü doğrudan hesaplayıp sonuçları tabloya dökmektedir. Karakter havuzları beş kategoride belirlendi: yalnızca rakamlar (10 karakter), yalnızca küçük harfler (26 karakter), büyük ve küçük harfler birlikte (52 karakter), harf ve rakamlar birlikte (62 karakter) ve tüm semboller dahil (100 karakter).

---

**Bulgular:**

**Sezar Şifreleme ve Kaba Kuvvet Analizi:**
Türkçe alfabesi üzerine kurulu Sezar şifresinin yalnızca 30 olası anahtarı bulunduğu doğrulandı. Bilgisayar bu 30 anahtarı sırayla deneyerek her denemede üretilen metnin Türkçe kelime listesiyle ne kadar örtüştüğünü puanladı. Testlerde doğru anahtar büyük çoğunlukla ilk birkaç denemede en yüksek puanı aldı ve şifre kırıldı. Kırma işlemi her koşulda en fazla **30 adımda** tamamlandı. Sezar şifrelemesinin tüm zayıflığı burada yatmaktadır: anahtar uzayı o kadar küçüktür ki bilgisayarın hepsini tek tek denemesi bile göz açıp kapayıncaya kadar biter.

**Havuz Büyüklüğü ve Kaba Kuvvet Adım Sayısı Analizi:**
Sezar şifrelemesinin 30 adımda kırılması, bize şu soruyu sordurdu: bir şifrenin gerçekten güçlü olması için kaç adım gerekmektedir? Hesaplamalar sonucunda şifre havuzuna eklenen her yeni karakter türünün deneme adımı sayısını üstel biçimde artırdığı görüldü.

| Şifre Havuzu Türü | Havuz Büyüklüğü | 8 Karakterli Şifre İçin Maksimum Deneme Adımı |
| :--- | :--- | :--- |
| **Sezar Şifresi (karşılaştırma)** | 30 anahtar | **30 Adım** |
| **Sadece Rakamlar** | 10 | 100.000.000 (100 Milyon) |
| **Sadece Küçük Harfler** | 26 | ~208 Milyar |
| **Büyük ve Küçük Harfler** | 52 | ~53 Trilyon |
| **Harfler + Rakamlar** | 62 | ~218 Trilyon |
| **Harfler + Rakamlar + Semboller** | 100 | 10.000.000.000.000.000 (10 Katrilyon) |

Tabloya Sezar şifresini de dahil ederek karşılaştırmayı somutlaştırdık. Sezar şifresi kaba kuvvete karşı yalnızca 30 adım sunarken, yalnızca rakamlardan oluşan 8 haneli bir şifre bile 100 milyon adım gerektirmektedir. Bu 100 milyon adım modern bir bilgisayar tarafından yaklaşık **0,01 saniyede** gerçekleştirilebilir; yani rakam-only şifre de güvenli değildir. Ancak havuza büyük-küçük harf ve semboller eklendiğinde adım sayısı 10 katrilyona ulaşmakta ve bu süre bugünün teknolojisiyle kırılamayacak bir büyüklüğe çıkmaktadır. Havuz büyüklüğü 10'dan 100'e, yani 10 kat artarken adım sayısı 100.000 kat artmaktadır. Bunun sebebi, formüldeki üs sayısının (8) sabit kalması; her yeni karakterin katkısının çarpımsal değil üstel biçimde büyümesidir.

---

**Sonuç ve Tartışma:**
Bu proje, kriptografinin tarihsel kökeninden başlayarak modern şifre güvenliğinin matematiksel temellerine uzanan bir yolculuk sundu. Sezar şifrelemesi, MÖ 1. yüzyılda son derece zekice ve işlevsel bir buluştu; çünkü o dönemde mesajları elle tek tek deneyerek çözmek son derece zahmetliydi. Ancak bilgisayarın devreye girmesiyle bu yöntemin anahtar uzayının küçüklüğü ölümcül bir zayıflığa dönüştü: 30 adım, bir bilgisayar için milisaniyenin bile altında bir süredir.

Buradan çıkan sonuç yalnızca Sezar şifrelemesiyle sınırlı değildir. Herhangi bir şifreleme yönteminin güvenliği, büyük ölçüde kaba kuvvet saldırısına karşı koyabilmesine bağlıdır; bu da doğrudan adım sayısıyla ölçülür. Projemizin ikinci bölümü gösterdi ki bu adım sayısı, havuza eklenen her yeni karakter türüyle üslü sayı mantığına göre büyür. Bir şifredeki tek bir `!` işareti trilyonlarca ekstra adım anlamına gelir. Sonuç olarak matematikteki üslü sayı kavramı soyut bir konu değil, dijital güvenliğin doğrudan temelidir.