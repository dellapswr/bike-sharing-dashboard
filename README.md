# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda menggunakan **Bike Sharing Dataset** selama periode Januari 2011 hingga Desember 2012.

Analisis dilakukan menggunakan Python dan mencakup tahapan *data wrangling*, *exploratory data analysis* (EDA), visualisasi data, serta analisis lanjutan menggunakan **rule-based clustering dengan teknik binning**.

Hasil analisis disajikan melalui Jupyter Notebook dan dashboard interaktif menggunakan Streamlit.

## Pertanyaan Bisnis

1. Bagaimana rata-rata jumlah penyewaan sepeda berbeda berdasarkan musim dan kondisi cuaca selama periode 2011–2012?
2. Bagaimana pola rata-rata penyewaan sepeda per jam berbeda antara Working Day dan Non-Working Day selama periode 2011–2012?

## Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset**, terdiri atas:

- `day.csv`: data penyewaan sepeda berdasarkan hari.
- `hour.csv`: data penyewaan sepeda berdasarkan jam.

Dataset mencakup **731 observasi harian** dan **17.379 observasi per jam**, dengan total **3.292.679 penyewaan**. Kedua file merepresentasikan aktivitas penyewaan yang sama pada tingkat agregasi berbeda, sehingga totalnya tidak dijumlahkan satu sama lain.

## Tahapan Analisis

1. **Data Gathering** — memuat data penyewaan sepeda.
2. **Data Assessing** — memeriksa nilai kosong, duplikasi, konsistensi, dan kualitas data.
3. **Data Cleaning** — menyiapkan tipe data tanggal serta label kategori untuk analisis.
4. **Exploratory Data Analysis** — mengeksplorasi pola penyewaan berdasarkan musim, cuaca, jam, dan jenis hari.
5. **Data Visualization** — membuat grafik untuk menjawab kedua pertanyaan bisnis.
6. **Advanced Analysis** — melakukan segmentasi tingkat permintaan menggunakan rule-based clustering dengan teknik binning.
7. **Conclusion & Recommendation** — merumuskan kesimpulan dan rekomendasi operasional berdasarkan temuan.

## Hasil Analisis

### Pertanyaan Bisnis 1 — Musim dan Kondisi Cuaca

Selama periode 2011–2012:

- Musim **Fall** memiliki rata-rata penyewaan tertinggi, yaitu **5.644,30 penyewaan per hari**.
- Musim **Spring** memiliki rata-rata terendah, yaitu **2.604,13 penyewaan per hari**.
- Kondisi cuaca **Clear** memiliki rata-rata tertinggi, yaitu **4.876,79 penyewaan per hari**.
- Kondisi cuaca **Light Rain/Snow** memiliki rata-rata terendah, yaitu **1.803,29 penyewaan per hari**.

Hasil ini menunjukkan perbedaan pola penyewaan berdasarkan musim dan cuaca, tanpa menyimpulkan adanya hubungan sebab-akibat.

### Pertanyaan Bisnis 2 — Pola Penyewaan per Jam

- Pada **Working Day**, dua puncak penyewaan yang menonjol terlihat pada pukul **08.00** (rata-rata **477,01**) dan **17.00** (rata-rata **525,29** penyewaan per jam tercatat).
- Pada **Non-Working Day**, rata-rata penyewaan tertinggi terjadi pada pukul **13.00**, yaitu **372,73 penyewaan per jam tercatat**.

Temuan ini dapat menjadi pertimbangan dalam penentuan prioritas kesiapan armada pada periode permintaan historis tinggi.

### Analisis Lanjutan — Rule-Based Clustering

Analisis lanjutan menggunakan teknik binning berdasarkan persentil 33,33% dan 66,67% dari **48 kombinasi jam dan jenis hari** (24 jam × 2 jenis hari).

Hasil segmentasi seluruh periode 2011–2012:

- **Low Demand:** 16 kombinasi.
- **Medium Demand:** 16 kombinasi.
- **High Demand:** 16 kombinasi.

Kategori **High Demand** ditemukan pada:

- **Working Day:** pukul 07.00–08.00 dan 16.00–20.00.
- **Non-Working Day:** pukul 10.00–18.00.

Kategori permintaan menunjukkan pengelompokan relatif berdasarkan data historis, bukan kapasitas armada aktual. Pada dashboard, ambang segmentasi dihitung ulang berdasarkan tahun yang dipilih.

## Struktur Proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│   ├── day.csv
│   └── hour.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── requirements.txt
└── README.md
```

Struktur tersebut menunjukkan berkas utama untuk submission final. Folder `backup_sementara` dan `.ipynb_checkpoints` tidak perlu disertakan dalam ZIP final.

## Cara Menjalankan Dashboard

Pastikan Python telah terinstal. Buka terminal atau Command Prompt pada folder utama `submission`, lalu jalankan:

**1. Instal dependensi:**

```bash
python -m pip install -r requirements.txt
```

**2. Jalankan dashboard:**

```bash
python -m streamlit run dashboard/dashboard.py
```

**3. Buka dashboard** melalui alamat lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`.

Dashboard menyediakan filter tahun 2011 dan 2012, ringkasan penyewaan, visualisasi musim dan cuaca, pola per jam, serta heatmap segmentasi permintaan. Pilih setidaknya satu tahun untuk menampilkan analisis. Jika kedua tahun dipilih, hasil mencakup periode 2011–2012.

## Keterbatasan Analisis

Analisis bersifat deskriptif dan menggunakan data historis periode 2011–2012. Pada dataset per jam ditemukan **165 timestamp yang tidak tercatat**. Rata-rata per jam dihitung menggunakan observasi yang tersedia; timestamp yang tidak tercatat tidak dianggap sebagai nol penyewaan.

Dataset tidak menyediakan informasi kapasitas armada aktual, sehingga hasil analisis dan rekomendasi perlu divalidasi terhadap kondisi operasional nyata.

## Rekomendasi

- Mempertimbangkan variasi permintaan menurut musim dan kondisi cuaca dalam perencanaan kesiapan armada.
- Memprioritaskan pemeriksaan kesiapan armada menjelang jam dengan permintaan historis tinggi.
- Mempertimbangkan jam dengan permintaan relatif rendah untuk penjadwalan pemeliharaan.
- Memantau kelengkapan data penyewaan secara berkala.
- Mengevaluasi rekomendasi menggunakan data operasional terbaru sebelum diterapkan.

## Sumber Data

**Bike Sharing Dataset — UCI Machine Learning Repository**  
https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
