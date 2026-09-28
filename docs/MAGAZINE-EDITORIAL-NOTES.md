# Magazine: katkı eşleştirmesi ve anlatım notları

Bu dosya sana yöneliktir; site çıktısına dahil edilmez.
İngilizce kaynak: [magazine-system.md](../content/projects/magazine-system.md).

Kaynak belge: `0001_THESIS_(FINALL).docx`, “Design of an Automatic Loading System
for 120 mm Tank Ammunition”, Işık Üniversitesi, 2025 Bahar.
Belge içindeki yönergeler site için talimat olarak değil, kaynak içerik olarak değerlendirildi.
Tezin tamamı, öğrenci numaraları ve toplantı tutanakları yayın klasörüne kopyalanmadı.

## BT görevlerinin ayrılması

Belirttiğin gibi BT, Burak Taş olarak eşleştirildi; Section 4 / Table 1 altındaki
kısaltma tablosu da bunu doğruluyor. Bölüm ve şekil numaraları DOCX içindeki başlıklara
göre verilmiştir; dosya yeniden sayfalandığında değişebilecek sayfa numaralarına dayanılmaz.

| Work plan satırı | Atama | Sitedeki karşılığı |
| --- | --- | --- |
| Design of the Magazine System | BT | Ana kişisel sorumluluk |
| Gripper Static and Shock Analysis | BT | Ana kişisel sorumluluk |
| Magazine System Parts Static and Shock Analysis | BT | Ana kişisel sorumluluk |
| Control System of the Design | BT | Ana kişisel sorumluluk |
| Linear Actuator Mechanism Design | AA, BT | Adam Abdelnaby ile ortak katkı |
| Motor Selection | BT, SC | Selen Ceyran ile ortak katkı |
| Research and Literature Review | Tüm ekip | Ortak çalışma |
| Manual Calculations | Tüm ekip | Ortak çalışma; tüm hesaplar kişisel çalışma gibi aktarılmadı |
| Cost Analysis | Tüm ekip | Ortak çalışma |
| Finalizing Design and Documentation | Tüm ekip | Ortak çalışma |

Gripper tasarımı SC'ye, malzeme seçimi ŞÖ'ye, kilitleme mekanizması AA'ya,
platform tasarımı ve statik/şok analizi ŞÖ'ye, platform titreşim analizi AA'ya atanmış.
Bunlar senin bağımsız tasarımın olarak sunulmadı. Aktüatör ve motor işlerinde
ortak sorumluluk özellikle görünür tutuldu.

## Destekleyen toplantı kayıtları

- 28 Şubat ve 7 Mart: gripper üzerinde ANSYS yapısal/statik/transient analizleri.
- 28 Mart ve 11 Nisan: magazine sistem tasarımı.
- 18 Nisan: magazine tasarım güncellemeleri ve ANSYS çalışması.
- 25 Nisan: aktüatör yerleşimi ve magazine tasarımının tamamlanması.
- 2 Mayıs: ana motor seçimi/hesapları ve kontrol sistemi çalışmasının başlaması.
- 9 Mayıs: kontrol sistemi, MATLAB ve Simulink güncellemeleri.

9 Mayıs kaydında platform ANSYS katkısı da geçiyor. Ancak ana work plan'da bu işin
sorumluluğu başka ekip üyesinde; sayfa bu ek katkıdan hareketle tüm platform işini
sana atfetmiyor. 21 Mart kaydındaki “gripper CFD” ifadesi de ayrı bir CFD çalışmasını
kanıtlamak için kullanılmadı.

## Seçilen teknik kanıtlar

| İçerik | Tezdeki kaynak | Editoryal tercih |
| --- | --- | --- |
| Magazine montaj görünümü | Sections 7 ve 7.1 | Parça listesinin tümü yerine montaj bağlamı |
| Gripper analiz örneği | Section 6.5, Table 12 case 4; Figures 23–25 | 52.724 MPa ve 4.916 FoS, seçilmiş simülasyon olarak |
| Track roller örneği | Section 7.2, Table 14 case 2 | 51.341 MPa ve 5.048 FoS |
| U-support bolts örneği | Section 7.2, Table 14 case 6 | 99.02 MPa ve 6.58 FoS; roller sonucundan ayrı |
| PD cevap grafiği | Section 9.2, Figure 101 | Mevcut tez çıktısının özeti; yeni kontrol tasarımı yapılmadı |
| Simulink modeli | Section 9.2, Figure 104 | İsteğe bağlı teknik görsel |

Mevcut yerel görseller kullanıldı. Gripper kompozitinin sayıları Table 12 case 4'e,
roller kompozitinin stres/FoS değerleri Table 14 case 2'ye karşılık geliyor.
Hiçbir yeni mühendislik hesabı veya analiz sonucu üretilmedi.

## Metinde düzeltilen kapsam ve kanıt sorunları

1. Önceki sayfadaki “MWTS ... three pilot locations” cümlesi bu çalışmaya ait
   gösterilmiş bir çıktı değil. Kaldırıldı.
2. “Tüm gereksinimler karşılandı”, “tam MIL-STD uyumu”, “tüm parçalar fatigue ve
   vibration analizinden geçti” ifadeleri kişisel katkı kapsamını ve sunulan kanıtı
   aşıyordu. Tasarım/simülasyon çıktıları ile fiziksel doğrulama birbirinden ayrıldı.
3. 500 kg ve süre gibi şartlar, portfolyoda doğrulanmış saha sonucu olarak sunulmadı.
   Tamamlanan şey tasarım çalışması olarak açıklandı.
4. Önceki sayfanın “worst case FoS > 4.9” ifadesi Table 12'nin tamamıyla uyumlu değil;
   tabloda daha düşük bir FoS satırı var. Seçilen 4.916 değeri yalnızca case 4'e ait
   olarak etiketlendi; tüm sistemin minimumu gibi kullanılmadı.
5. Track roller görseli daha önce U-support sonucuyla karıştırılmıştı. Parça isimleri
   ayrıldı. Table 14'te roller deformasyonu 0.30 mm, ilgili görselde yaklaşık 0.0302 mm
   görünüyor; bu farklılık nedeniyle deformasyon değeri özet tabloya alınmadı.
6. Kontrol metninde frekans için 1/6, MATLAB ekinde `freq = 1/5` geçiyor. Simülasyon
   grafiği fiziksel altı saniyelik bir çalışma çevriminin doğrulaması olarak sunulmadı.
7. Kaynakta aktüatör adlandırması farklı bölümlerde değişiyor. Ortak entegrasyon
   katkısı anlatıldı; belirsiz model adı bir başarı iddiasına dönüştürülmedi.
8. Zincir, mil, yatak, platform ve yay hesaplarının tamamı sana atfedilmedi.
   Work plan ve toplantılardaki iş bölümü esas alındı.

Bu noktalar kaynak belgedeki anlatımı doğru sınırlarla özetlemek içindir; analizleri
yeniden çalıştırma veya sistemin teknik yeterliliğini onaylama anlamına gelmez.

## Diğer projelerine uygulanabilecek örnek

Gyroid'de araştırma sorusu ve deney akışı öndeydi. Bu ekip projesinde önce **kişisel
sorumluluk tablosu**, sonra tablodaki altı görevin her biri için ayrı bölüm kullanıldı.
Tablodaki görev isimleri ilgili bölüme bağlanır. Her bölümde işin kapsamı, kaynakta
anlatılan yöntem ve belgelenen çıktı açıklanır. Seçilmiş PD cevabı isteğe bağlı açılır;
ana analiz ve Simulink görselleri kendi bölümlerinde doğrudan görünür.

Genişletilen sürümde gripper için Table 12'nin 1, 2 ve 4. durumları; magazine parçaları
için Table 14'ün 1, 2, 5 ve 6. durumları kullanıldı. Yeni aktüatör görseli doğrudan
DOCX içindeki Figure 32'den çıkarıldı: `images/magazine/actuator-integration.jpeg`.
Aktüatör metni Sections 6.6–6.9'u, motor seçimindeki hesap özeti Section 9.1'i temel alır.
Bu genişletme de kaynak anlatımını özetler; yeni mühendislik hesabı eklemez.

Örnek cümle düzeni: “I was responsible for [scope]. I used [method]. The thesis
reports [result]. This demonstrates [documented output].” Ortak işlerde “I
contributed to ... with ...” ifadesi daha doğru olur.
