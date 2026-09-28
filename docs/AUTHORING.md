# Case study yazma kılavuzu

Site dili İngilizcedir. Yazını bir proje raporunun seçilmiş ve anlaşılır özeti gibi düşün:
ziyaretçi önce bağlamı ve senin katkını kavrasın, sonra yetkinliğini gösteren teknik örnekleri incelesin.

## Günlük kullanım

1. `python scripts/new_project.py project-slug --title "Project Title"` ile dosya oluştur.
2. `content/projects/project-slug.md` içindeki üst bilgileri ve metni doldur.
3. Görselleri `images/project-slug/` altına koy.
4. Hazır olduğunda `draft: false` yap. Yerel kontrol için `python scripts/dev.py` çalıştır.
5. Önizlemeyi kontrol edip dosyaları GitHub'a gönder. Pages iş akışı kurulmuşsa yayın otomatik güncellenir.

`draft: true` olan dosyalar proje listelerine veya oluşturulan sayfalara dahil edilmez.
Yayımdan kaldırılan bir projenin önceden oluşturulmuş HTML dosyası da sonraki build'de temizlenir.
Git deposuna gönderdiğin Markdown kaynaklarının, deponun görünürlüğüne göre okunabileceğini unutma;
`draft` yalnızca site çıktısını kontrol eder.

## Üst bilgiler

| Alan | Kullanımı |
| --- | --- |
| `title` | Tam başlık; tarayıcı ve paylaşım başlığı |
| `short_title` | Kartta ve sayfa açılışında görünen kısa başlık |
| `slug` | URL adı; küçük harfler ve tireler. Yayımdan sonra değiştirmemek iyi olur. |
| `summary` | Proje listesinde görünen tek cümle |
| `subtitle` | Case study açılışında biraz daha ayrıntılı özet |
| `discipline` | Filtre kategorisi: Mechanical, Manufacturing, Robotics veya ihtiyacın olan yeni bir kategori |
| `tags` | Ek alan etiketleri; ör. `[Mechatronics]`. Proje kendi kategorisinde ve bu ek filtrelerde bulunur. |
| `methods` | Karttaki kısa yöntem etiketleri |
| `tools` | Yazının sonundaki araç listesi; aramada da bulunur |
| `role` | Senin kişisel katkın |
| `period` | Görüntülenecek dönem; ör. `"June 2026"` |
| `status` | `completed` veya `ongoing` |
| `cover` | Kapak yolu; boşsa tipografik kapak |
| `cover_alt` | Görselin erişilebilir açıklaması |
| `order` | Küçük sayı önce görünür |
| `featured` | `true` ise ana sayfa seçkisine aday. İlk üçü gösterilir. |
| `draft` | `true` ise siteye dahil edilmez |
| `legacy` | Mevcut beş projenin eski adresi. Yeni projelerde gerekli değil. |

İlk aktarımda Markdown dosyaları önceki yazıları kayıpsız taşıdı.
Gyroid sayfası sonradan sonuç raporuna göre yeniden düzenlendi; tamamlanmış bir anlatım
örneği için [Gyroid yazısını](../content/projects/gyroid-structures.md) ve
[detay seçimi notlarını](GYROID-EDITORIAL-NOTES.md) inceleyebilirsin.
Ekip projesinde kendi sorumluluğunu ayırmak için [Magazine yazısı](../content/projects/magazine-system.md)
ve [katkı eşleştirme notları](MAGAZINE-EDITORIAL-NOTES.md) ikinci bir örnektir.
Yeni yazılarda `templates/case-study.md` düzenini kullanabilirsin. Başlıklar serbesttir;
`##` seviyesindeki başlıklar içindekiler menüsünü otomatik oluşturur.

Ana sayfadaki üst vitrin, `featured: true` olan ilk üç projeyi gösterir. Altındaki
**More to explore** bölümü vitrinde yer almayan sonraki üç projeyi gösterir;
aynı proje iki bölümde tekrarlanmaz. Numaralar proje dizinindeki `order` sırasına
göre belirlenir. Diğer tüm çalışmalara **Work index** üzerinden ulaşılır.
Ana sayfanın yaklaşım ve profil metinleri `content/site.yml` içindeki `landing` alanındadır.

## Önerilen anlatım

- **Project overview:** Problem, amaç, kapsam ve mevcut durum.
- **My contribution:** Ekibin değil, bizzat senin sorumlulukların.
- **Key decisions:** İki veya üç önemli tercih ve gerekçeleri.
- **Technical evidence:** İki–dört seçilmiş hesaplama, analiz, test veya kod örneği.
- **Results & learnings:** Gösterilen sonuç, sınırlar ve öğrendiklerin.

Teknik örneği **Question → Inputs & assumptions → Method → Result → Interpretation & decision → Limitations**
sırasıyla yaz. Her örnekte formül bulunması şart değil. Açıklamalı bir grafik veya karşılaştırma
tablosu bazen daha anlaşılırdır. Tam türetmeyi veya bütün veriyi eklemen gerekmez.

## Görseller

Yollar depo kökünden başlar. Dosya adında boşluk varsa yolu `<...>` içine al:

```markdown
![Test setup viewed from the side](<images/my-project/test setup.webp> "Figure 1. Test setup and measurement locations.")
```

Tırnak içindeki metin görsel alt yazısı olur. `[...]` içindeki metin ekran okuyucu açıklamasıdır.
Görsele tıklanınca büyür; Escape ile kapanır. Kapakta gerçek proje görseli tercih et.
Eksik dosyalar build raporuna yazılır; içeriği silinmez.

## Denklemler

Blok denklem:

```latex
$$
\sigma = \frac{F}{A_0}
$$
```

Satır içi: `\(E = \Delta\sigma / \Delta\epsilon\)`.
`$...$` tek dolar biçimi desteklenmez; para tutarlarıyla karışmaması için `\(...\)` kullan.
Sembolleri, birimleri ve varsayımları açıkla. Uzun denklemler mobilde kendi alanında kayar.

## Tablolar ve kod

```markdown
| Parameter | Value | Unit |
| --- | --- | --- |
| Your measured input | Actual value | SI unit |
```

Kod için üç ters tırnak ve dil adını kullan (`python`, `matlab` vb.). Kod blokları kaydırılabilir;
tarayıcı destekliyorsa kopyalama düğmesi görünür. Otomatik renkli sözdizimi vurgulaması yoktur.

## Video ve isteğe bağlı detay

```markdown
[Prototype demonstration](<images/my-project/demo.mp4>)
```

Yerel MP4/WebM dosyası oynatıcıya dönüşür. Uzun bir teknik ek gerektiğinde:

```html
<details>
<summary>Additional calculation notes</summary>

Markdown paragraphs, equations or tables can go here.

</details>
```

## Düzenleme sonrası

```powershell
python scripts/build.py
python scripts/check_site.py
```

Kökteki eski bağlantılarla açılan HTML dosyalarını da güncellemek için `--output .` ekle.
Yayıma `_site/` gönderilir; `.md` dosyaları tarayıcıda her ziyarette yeniden işlenmez.
GitHub Actions kurulumundan sonra senin düzenlemen gerekenler Markdown ve görsel dosyalarıdır.
