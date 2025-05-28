# Aplikasi Pencarian Jalur Tercepat di Kampus UNIB

Proyek ini adalah aplikasi berbasis Python dengan antarmuka GUI menggunakan `Tkinter`, yang memungkinkan pengguna mencari rute tercepat antar titik di dalam lingkungan kampus Universitas Bengkulu (UNIB). Aplikasi ini menggunakan algoritma graf dan data waktu tempuh untuk menyesuaikan aksesibilitas lokasi, serta menyajikan peta interaktif menggunakan OpenRouteService dan Folium.

## 🧭 Fitur Utama

- Pencarian rute tercepat berbasis waktu antar gedung di kampus UNIB.
- Visualisasi jalur pada peta interaktif menggunakan Folium.
- Penyesuaian rute berdasarkan waktu dan hari operasional (misalnya gerbang kampus tutup setelah jam tertentu).
- Antarmuka pengguna (GUI) yang mudah digunakan.
- Dukungan integrasi dengan OpenRouteService API.

## 🖼️ Tampilan Antarmuka

> (Tambahkan screenshot GUI jika tersedia)

## 📂 Struktur Proyek

```

proyek-jalur-unib/
├── main.py                 # File utama aplikasi
├── README.md               # Dokumentasi proyek ini
└── (output HTML peta akan dibuat otomatis saat aplikasi dijalankan)

````

## 🔧 Instalasi dan Menjalankan Aplikasi

### 1. Kloning Repositori

```bash
git clone https://github.com/username/proyek-jalur-unib.git
cd proyek-jalur-unib
````

### 2. Buat dan Aktifkan Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Instalasi Dependensi

```bash
pip install -r requirements.txt
```

Jika belum ada file `requirements.txt`, gunakan ini:

```bash
pip install tkinter folium openrouteservice
```

> Catatan: `tkinter` sudah tersedia secara default pada banyak distribusi Python, namun di beberapa sistem Linux, kamu mungkin perlu menginstalnya secara terpisah (contoh: `sudo apt install python3-tk`).

### 4. Jalankan Aplikasi

```bash
python main.py
```

## 🔑 Konfigurasi API

Aplikasi ini menggunakan [OpenRouteService](https://openrouteservice.org/) untuk visualisasi peta rute. Untuk menjalankan aplikasi:

1. Daftarkan akun di OpenRouteService.
2. Ambil API Key dari dashboard.
3. Masukkan API key kamu ke dalam variabel `ORS_API_KEY` di dalam `main.py`:

```python
ORS_API_KEY = "API_KEY_KAMU"
```

> Kunci default pada repo ini hanya untuk uji coba dan memiliki batasan penggunaan.

## 🗺️ Data Lokasi dan Graf Kampus

Aplikasi menggunakan representasi graf berbobot yang berisi:

* Node: Titik-titik lokasi penting di kampus UNIB.
* Edge: Hubungan antar titik, lengkap dengan atribut `jarak (meter)` dan `waktu (detik)`.

Contoh:

```python
"Pasca Hukum": [("Gerbang Depan", {"jarak": 200, "waktu": 120})]
```

## 🕒 Penyesuaian Dinamis Berdasarkan Waktu

Fungsi `get_modified_graph()` akan menonaktifkan akses ke simpul tertentu (misalnya gerbang kampus) jika waktu saat ini melewati pukul 16:00.

## ✅ Ketergantungan

* Python 3.7+
* tkinter
* folium
* openrouteservice

## 💡 Rencana Pengembangan

* Menambahkan algoritma pencarian rute (misal: Bellman-Ford atau Dijkstra).
* Menambahkan mode transportasi (jalan kaki, sepeda, motor).
* Integrasi database lokal untuk penyimpanan rute historis.
* Penambahan layer filter (misal: hanya gedung akademik).

## 🤝 Kontribusi

Pull request sangat diterima! Untuk perubahan besar, harap buka *issue* terlebih dahulu untuk mendiskusikan apa yang ingin diubah.

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - silakan lihat file [LICENSE](LICENSE) untuk detailnya.

## 🙌 Kredit

* Data lokasi berdasarkan lingkungan kampus UNIB.
* Visualisasi rute oleh [OpenRouteService](https://openrouteservice.org/).
* GUI dengan Tkinter.
