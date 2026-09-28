# Gyroid: portfolyo anlatımı için örnek

Bu not sana yöneliktir; ziyaretçiye gösterilen siteye dahil edilmez.
İngilizce yazı: [gyroid-structures.md](../content/projects/gyroid-structures.md).
Önizleme: [Gyroid case study](../case-studies/gyroid-structures/index.html).

## Ne kadar detay yeterli?

Bu sayfa teknik bir araştırma projesi için yaklaşık 7–8 dakikalık bir okuma örneği.
Her projenin bu uzunlukta olması gerekmez. Daha küçük bir çalışma için 600–900 kelime,
bu kapsamdaki bir çalışma için 1.200–1.600 kelime iyi bir başlangıç hedefidir.
Süreyi doldurmak yerine, okuyucunun kararlarını ve becerilerini anlayabilmesini hedefle.

Üç okuma katmanı kullandık:

1. **İlk 30 saniye:** Kapak, araştırma sorusu, rolün, 27 kombinasyon / 25 numune ve ana çıkarım.
2. **Birkaç dakika:** Bölüm başlıkları, tasarım tablosu, deney fotoğrafı ve seçilmiş sonuçlar.
3. **Teknik okuma:** Normalizasyon, denklemler, deney eğrileri, ANOVA ve çapraz doğrulama sonuçları.

Yedi bölümün her biri bir soruya cevap veriyor. Üretim aşamalarının tüm ayrıntıları,
her numunenin kırılma fotoğrafları, bütün ham veriler, literatür özeti ve tam kodlar ana
akışa alınmadı. Video isteğe bağlı açılıyor. Tam raporun sitede yayınlanması gerekmiyor.

## Sonraki yazında uygulayabileceğin düzen

| Bölüm | Okuyucunun anlaması gereken | Yaklaşık uzunluk |
| --- | --- | --- |
| Bağlam ve rol | Hangi sorun üzerinde, hangi sorumlulukla çalıştın? | 100–150 kelime |
| Tasarım kararları | Hangi parametreleri veya seçenekleri neden seçtin? | 150–250 kelime |
| Uygulama / doğrulama | Ne ürettin, neyi nasıl test ettin? | 150–200 kelime |
| Teknik kanıt | Girdiler → yöntem → sonuç → yorum | 300–500 kelime |
| Çıkarım | Ne gösterildi, hangi sınırlar var, sonraki adım ne? | 100–150 kelime |

Başlıkları projenin hikâyesine göre değiştir. Her alt başlıkta dört ayrı formül veya
aynı soru-cevap şablonu olması gerekmez. Bu sayfadaki gibi bir tabloyla bir değişkeni
karşılaştırmak, tüm 25 satırı göstermekten daha okunaklıdır. Grafik alt yazısında
yalnızca grafiğin adını değil, okuyucunun neye dikkat etmesi gerektiğini yaz.

Bir teknik örnek için minimum içerik: **koşul + yöntem + birimli sonuç + yorum + sınır**.
Gyroid sayfasında 8 mm / level 3 karşılaştırması bunun örneği. ML bölümünde ölçülen
performansla modelin önerdiği aday ayrı tutuldu. Düşük R²'yi gizlemek yerine,
sonucun hangi karar için yetersiz olduğunu açıklamak mühendislik muhakemesini gösterir.

## Rapordan kullanılan kaynaklar

Kaynak: `2209-a_sonuc_raporu_formati (5).docx.pdf`, 53 sayfa, imza bölümünde
1 Ocak 2026 tarihi. Aşağıdaki sayılar PDF'nin fiziksel sayfa numaralarıdır.
PDF'nin kendisi, idari sayfalar ve harcama bilgileri yayın klasörüne eklenmedi.

| Site içeriği | Kaynak |
| --- | --- |
| Yürütücü, danışman ve başlangıç | s. 5; rapor tarihi s. 53 |
| Üç tasarım parametresi ve 27 kombinasyon | s. 6–10 |
| 48/50 mm kafes boyutları, değişken derinlik, 5 mm pad | s. 7–10; Şekil 5 |
| Yazıcı, malzeme, 4 dakika UV kürleme | s. 10–14 |
| 3 mm/dk basma testi ve video düzeneği | s. 14–16 |
| Gerilme–birim şekil değiştirme, integrasyon ve eğim hesabı | s. 43–49, MATLAB eki |
| Üç satırlık 8 mm / level 3 karşılaştırması | s. 21, Tablo 2 |
| Tepe gerilmesi ANOVA, hücre boyutu p = 0.036 | s. 36, Şekil 47; görselden kontrol edildi |
| 25 numune, dört model ve LOOCV metrikleri | s. 39, Tablo 5; model tanımları s. 51–52 |
| 6 / 1.5 / 2 adayı, tahmin 6.47 MPa | s. 40, Tablo 6 |
| Modellerin tasarım kararı için yetersiz olduğu değerlendirmesi | s. 41 |

PDF'den doğrudan çıkarılan dört görsel:

- `images/gyroid/printed-series.jpeg`: Şekil 13, s. 14; yeni kapak.
- `images/gyroid/specimen-dimensions.png`: Şekil 5, s. 9.
- `images/gyroid/test-setup.jpeg`: Şekil 16, s. 15.
- `images/gyroid/stress-strain.png`: Şekil 20, s. 18; özgün grafik, yeniden hesaplanmadı.

Diğer eksik medyalar kullanıcının verdiği GitHub deposundan geri getirildi.
Mevcut yerel dosyalar korunarak 42 dosya indirildi ve Git blob SHA-1 değerleriyle doğrulandı.
İndirme kaydı `artifacts/restored-media.json` içinde; bu dosya yayınlanmaz.

## Raporda gözden geçirmeni önerdiğim noktalar

Bunlar portfolyo metnini hazırlarken fark edilen kaynak içi tutarsızlıklardır.
Ham test dosyaları mevcut olmadığı için sonuçlar yeniden hesaplanmadı.

1. **En iyi modelin adı:** s. 39'daki tabloda en yüksek R² ve en düşük RMSE Ridge'e ait.
   Metin Linear Regression diyor; s. 40'taki grafik Ridge başlığını taşıyor.
   S. 52'deki kod R²'ye göre ilk modeli seçiyor. Site tabloyu esas alıyor; 6.47 MPa
   tahminini belirli bir regresöre atfetmiyor. Bu seçimi sonuç dosyasından doğrulamak gerekir.
2. **25 / 27 ayrımı:** 27 tasarım kombinasyonu var; analizde 25 numune belirtiliyor.
   Tablo 2'de 10 mm / 1.5 mm / level 3 ve 4 sonuçları boş. Eksik sonuçların nedenini
   rapordan kesinleştiremiyoruz. Site bunları 27 tamamlanmış test gibi sunmuyor.
3. **EA30 kapsamı:** Bazı deneyler 0.3 strain'e ulaşmıyor. Ekteki kod en yakın noktayı
   seçtiğinden, erken biten kaydın son değerini EA30 gibi döndürebilir. Önce
   `max(strain) >= 0.3` kontrolü yapılmalı, ulaşmayanlar eksik tutulmalı; ulaşanlarda
   hedefe kadar integrasyon yapılmalı. EA30 ANOVA sonuçlarını bu kontrol sonrası
   yeniden değerlendirmek gerekir. Sayfaya kesin EA30 sıralaması veya p-değeri alınmadı.
4. **Kesit–dosya eşleştirmesi:** Python eki `os.listdir` sırasıyla sabit `A_list`
   sırasının eşleştiğini varsayıyor. MATLAB'da da sıra tabanlı eşleştirme var.
   Özellikle 10 mm / 1.5 mm serisi için Tablo 1–2 ile kod listesindeki alanlar
   karşılaştırılmalı. Dosya adını anahtar kabul eden bir numune tablosu kullanılmalı.
5. **Normalizasyon:** Minimum katı kesit alanıyla hesaplanan gerilme ile dış kesit
   alanına göre hesaplanan gerilme aynı değildir. EA birimi boyutsal olarak MJ/m³
   olsa da bu yöntemle toplam numune hacmine göre enerji yoğunluğu elde edilmiş
   sayılmaz. Sayfada alan ve referans uzunluğu açıklandı; bağımsız malzeme özelliği
   iddiası kullanılmadı. Çapraz kafa deplasmanının pad/cihaz etkilerini içerip
   içermediği de ham verilerle kontrol edilebilir.
6. **Elastik bölge:** Kod ekinde hem %0.2 hem %2 sınırı geçiyor; aktif birleşik grafik
   ve ANOVA kodu %2 kullanıyor. Sayfada %2 ve “initial stiffness estimate” ifadesi
   kullanıldı. Malzeme Young modülü gibi kesin bir özellik sunulmadı.
7. **Dönem:** Sonuç raporu tarihinden hareketle çalışma tamamlanmış olarak sunuldu;
   raporda idari bitiş tarihi boş olduğundan kesin proje bitiş günü uydurulmadı.
   Önceki sayfanın çelişkili başvuru/onay zaman çizelgesi kaldırıldı.
8. **Kişisel katkı:** Yürütücülük raporda açık; tasarım/test rolü eski sayfada da mevcut.
   Görevlerin başka ekip üyeleriyle paylaşıldıysa birinci şahıs cümlelerini gerçek iş
   bölümüne göre daraltabilirsin. Danışmanın adı kaynakta geçtiği biçimde korunuyor.

Eski sayfadaki 4–8 mm aralığı, 9 numune, standard/tough resin, gelecekte yapılacak
ML anlatısı güncel raporla değiştirildi. Raporda tamamlandığı gösterilmeyen FEA ve
sentetik veri birleştirme işleri bu sayfanın çıktıları olarak listelenmedi.

## Düzenlemeye devam etmek

Sadece Markdown'ı değiştir; aynı içerik hem yeni URL'ye hem `page4.html` adresine
aktarılır. `python scripts/build.py --output .` yerel HTML'leri,
`python scripts/build.py` yayın klasörünü günceller. Genel yazım biçimleri için
[AUTHORING.md](AUTHORING.md), boş başlangıç için [case study şablonu](../templates/case-study.md).
