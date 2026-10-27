# Ar-Ge Proje Analiz ve Raporlama Aracı

Python ile hazırlanmış, örnek Ar-Ge proje verilerini analiz eden ve raporlayan başlangıç seviyesi portföy projesi.

## Amaç

Bu araç, örnek projelerde planlanan ve gerçekleşen bütçeyi, ilerlemeyi ve takvim sapmalarını analiz eder. Gecikme ve bütçe aşımı gibi durumları belirler; CSV özet raporu ve grafik üretir.

> **Önemli:** Bu depo eğitim ve portföy amaçlıdır. Gerçek TÜBİTAK projelerinin değerlendirme kurallarını veya resmi süreçlerini temsil etmez. Kullanılan tüm veriler sentetiktir (örnek olarak oluşturulmuştur).

## Özellikler

- CSV dosyasından proje verilerini okuma
- Bütçe farkı ve bütçe sapma yüzdesi hesaplama
- Planlanan ve gerçekleşen ilerleme arasındaki farkı hesaplama
- Gecikme ve bütçe aşımı işaretleri üretme
- Analiz sonuçlarını CSV olarak dışa aktarma
- Bütçe karşılaştırma grafiği oluşturma
- Birim testleriyle temel hesaplamaları doğrulama

## Kullanılan teknolojiler

- Python 3.10+
- pandas
- matplotlib
- pytest

## Proje yapısı

```text
arge-proje-analiz-raporlama/
├── data/
│   └── sample_projects.csv
├── docs/
│   └── sample_report.md
├── outputs/
│   └── .gitkeep
├── src/
│   └── project_analyzer.py
├── tests/
│   └── test_project_analyzer.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Kurulum

### 1. Depoyu bilgisayarına indir

GitHub sayfasında **Code → Download ZIP** seçeneğini kullanabilir veya Git ile klonlayabilirsin.

### 2. Sanal ortam oluştur (önerilir)

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Gerekli paketleri yükle

```bash
python -m pip install -r requirements.txt
```

## Çalıştırma

Proje kök klasöründe:

```bash
python src/project_analyzer.py
```

Farklı bir CSV dosyası veya çıktı konumu belirtmek için:

```bash
python src/project_analyzer.py --input data/sample_projects.csv --output-dir outputs
```

Program `outputs/analysis_report.csv` ve `outputs/budget_comparison.png` dosyalarını oluşturur.

## Testleri çalıştırma

```bash
python -m pytest -q
```

## CSV veri alanları

| Alan | Açıklama |
|---|---|
| `project_id` | Örnek proje kimliği |
| `project_name` | Proje adı |
| `planned_budget` | Planlanan bütçe (örnek para birimi: TL) |
| `actual_budget` | Gerçekleşen bütçe (örnek para birimi: TL) |
| `planned_progress` | Planlanan ilerleme yüzdesi (0–100) |
| `actual_progress` | Gerçekleşen ilerleme yüzdesi (0–100) |
| `planned_end_date` | Planlanan bitiş tarihi (YYYY-AA-GG) |
| `forecast_end_date` | Tahmini bitiş tarihi (YYYY-AA-GG) |

## Örnek analiz mantığı

- **Bütçe farkı** = gerçekleşen bütçe − planlanan bütçe
- **Bütçe sapması (%)** = bütçe farkı / planlanan bütçe × 100
- **İlerleme farkı** = gerçekleşen ilerleme − planlanan ilerleme
- **Gecikme (gün)** = tahmini bitiş tarihi − planlanan bitiş tarihi

Bütçe sapması pozitifse planlanan bütçenin üzerinde harcama yapılmış demektir. İlerleme farkı negatifse gerçekleşen ilerleme planlananın gerisindedir.

## Sınırlamalar ve sonraki geliştirmeler

Bu ilk sürüm, sınırlı sayıda basit gösterge üretir. Risk puanları, ağırlıklı iş paketi ilerlemesi, veri doğrulama arayüzü, PDF raporu ve grafiklerin özelleştirilmesi ileride eklenebilir. Çıktılar karar desteği amacıyla kullanılmalı; tek başına proje başarısı veya resmi uygunluk kararı olarak değerlendirilmemelidir.

## Portföy notu

Bu projeyi GitHub'a yüklemeden önce kodu çalıştır, testleri geçir ve üretilen raporu incele. Projeyi kendi başına açıklayabildiğinden emin ol. README'deki ekran görüntülerini ve sonuçları gerçekten elde ettiğinde ekle.
