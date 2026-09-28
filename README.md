# Burak Taş — Engineering portfolio

İngilizce portfolyo; Markdown kaynaklarından üretilen statik HTML sayfaları.
Ana sayfa, proje dizini, proje yazıları, hakkında ve iletişim sayfaları ortak tasarımı kullanır.

## Önizleme

Python 3.12 veya üzeri:

```powershell
python -m pip install -r requirements.txt
python scripts/dev.py
```

`http://127.0.0.1:8000/` adresini aç. İçerik değişince yeniden oluşturulur; tarayıcıyı yenile.
JavaScript kapalıyken de yazılar ve proje bağlantıları çalışır.

## Yeni case study

```powershell
python scripts/new_project.py my-project --title "My Project"
```

`content/projects/my-project.md` dosyasını düzenle. Şablon İngilizcedir ve
`draft: true` olarak başlar; taslaklar siteye çıkmaz. Hazır olduğunda `draft: false` yap.

Alternatif: `templates/case-study.md` dosyasını `content/projects/` klasörüne kopyala.
Dosyanın adı açıklayıcı olsun; URL için esas alınan alan `slug` değeridir.

Detaylı yönergeler: [İçerik yazma kılavuzu](docs/AUTHORING.md).

## İçeriğin yeri

| İçerik | Kaynak |
| --- | --- |
| Beş mevcut proje | `content/projects/*.md` |
| Hakkında | `content/pages/about.md` |
| İletişim metni | `content/pages/contact.md` |
| E-posta, sosyal bağlantılar, CV, kısa profil | `content/site.yml` |
| Yeni yazı şablonu | `templates/case-study.md` |
| Ortak sayfa iskeleti | `templates/base.html` |
| Tasarım ve etkileşimler | `assets/site.css`, `assets/site.js` |

HTML dosyalarını elle düzenleme: sonraki oluşturma sırasında Markdown'dan yeniden yazılır.
Eski `page1.html`–`page5.html` bağlantıları yeni tasarımla çalışmaya devam eder.
Yeni, açıklayıcı adresler `case-studies/<slug>/index.html` biçimindedir.

## Oluşturma ve kontrol

```powershell
python scripts/test_build.py
python scripts/build.py
python scripts/check_site.py
```

Yayınlanabilir çıktı `_site/` içindedir. Sunum, kaynak kod, Markdown taslakları ve
arşiv kopyaları bu çıktıya eklenmez. Kökteki hazır HTML dosyalarını da yenilemek için:

```powershell
python scripts/build.py --output .
```

## GitHub Pages

`.github/workflows/pages.yml`, `main` veya `master` dalına içerik gönderildiğinde
Markdown'ı HTML'e çevirir, kontrol eder ve `_site/` klasörünü yayımlar.
GitHub deposunda **Settings → Pages → Build and deployment → Source: GitHub Actions** seç.
İlk yayını Actions sekmesindeki **Build and publish portfolio → Run workflow** ile de başlatabilirsin.
Farklı bir ana dal kullanıyorsan workflow içindeki `branches` alanını güncelle.

Mevcut `/portfolio/` adresi `content/site.yml` içinde korunmuştur. Başka bir alan adına
geçersen `url` alanını güncelle. Site içi bağlantılar göreli olduğundan hem yerel önizlemede
hem GitHub Pages alt dizininde çalışır.

Bu çalışma klasöründe Git deposu bulunmadığı için ilk aktarımı `.publish/` altındaki
ayrı bir klon üzerinden yapabilirsin. VS Code terminalini proje kökünde aç:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prepare_publish.ps1
git -C .publish commit -m "Redesign portfolio and migrate case studies"
git -C .publish push origin main
```

Hazırlık komutu sayfaları oluşturur, kontrol eder, mevcut GitHub deposunu klonlar ve
yeni dosyaları bu klona kopyalar. Değişiklikleri stage eder; commit veya push yapmaz.
`.tools`, `artifacts`, `archive` ve `design-proposals` klasörleri aktarılmaz.
Eski commit geçmişi korunur; dosyaları GitHub'dan tek tek silmek gerekmez.
GitHub kimlik doğrulaması istenirse kendi hesabınla tamamla.

İlk yayın öncesinde yukarıdaki Pages kaynağını **GitHub Actions** olarak seç.
Push sonrası **Actions → Build and publish portfolio** iş akışının başarılı olduğunu kontrol et.
Site adresi `https://burkutken.github.io/portfolio/` olarak kalır.

Yayın sonrasında düzenlemeye `.publish/` klasörünü VS Code'da açarak devam edebilirsin.
Bu klasör normal bir Git deposudur; Markdown/görsel değişikliklerinden sonra:

```powershell
git add content images
git commit -m "Update case studies"
git push
```

Tasarım dosyalarını da değiştirdiysen ilgili dosyaları `git add` komutuna ekle.
Uzak depo başka bir yerden güncellendiyse çalışmaya başlamadan önce `git pull --ff-only` kullan.

Kaynak: [GitHub Pages özel iş akışları](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Taşınan içerik ve eksik dosyalar

Proje metinleri, listeler, zaman çizelgeleri ve medya referansları eski HTML'den korundu.
Yerel eski dosyalar `archive/original-site/` içinde saklandı; bu arşiv yayına dahil edilmez.

Eksik medya dosyaları mevcut GitHub deposundan geri getirildi. Son build'de eksik
medya referansı bulunmuyor. Sonradan eklenen eksik dosyalar build raporuna yazılır;
dosyayı orijinal yoluna ekleyip yeniden oluşturduğunda görünür.

- [Eksik medya listesi](docs/missing-media.json)
- [İçerik tutarsızlıkları ve taşıma notları](docs/MIGRATION.md)

İletişim sayfası doğrudan e-posta ve sosyal bağlantıları kullanır.
Eski Formspree formu kaldırılmıştır; ayrıca bir form hizmeti gerektirmez.

## Tarayıcı doğrulaması

Yerel geliştirme testi için isteğe bağlı `playwright` paketi kullanılır; sitenin
çalışması veya yayımlanması için gerekmez. `scripts/browser_check.py`, Windows'taki
yerel Chrome ile masaüstü/mobil gezinme, filtreleme, görsel büyütme ve JavaScript
kapalı okuma davranışını kontrol eder. Ekran görüntüleri `artifacts/` altına yazılır.

KaTeX 0.16.22, lisansıyla birlikte `assets/vendor/katex/` altında yereldir.
Formüller için çalışma anında dış CDN isteği yapılmaz.
