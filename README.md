# 🏓 Pong Hand Tracking

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Game **Pong 2D klasik** interaktif yang dikendalikan menggunakan gerakan tangan (*hand tracking*) secara *real-time* melalui *webcam* laptop tanpa butuh pengontrol tambahan[cite: 1].

---

## 💡 Demo Preview

> *Tambahkan file GIF/Screenshot gameplay kamu di folder assets/ lalu aktifkan baris berikut:*  
> `![Demo Preview](assets/demo.gif)`

---

## ✨ Fitur Utama

- ✋ **Hand Motion Control:** Kendalikan *paddle* pemain hanya dengan menggerakkan jari telunjuk ke atas dan bawah[cite: 1].
- 🤖 **Smart AI Opponent:** Lawan komputer dengan pergerakan responsif[cite: 1].
- 🎯 **Real-time Detection:** Visualisasi titik *landmark* tangan pada jendela *webcam*[cite: 1].
- 📊 **HUD & Status Indicator:** Menampilkan skor pertandingan dan status deteksi tangan (`YES / NO`) secara *live*[cite: 1].
- ⚙️ **Smooth Physics:** Logika pantulan bola dan sistem skor klasik khas Pong[cite: 1].

---

## 🛠️ Teknologi & Tools

- **Python 3.12** — Bahasa pemrosesan utama.
- **OpenCV** — Mengambil *feed* video dari webcam[cite: 1].
- **MediaPipe Hands** — Pelacakan koordinat titik tangan secara presisi[cite: 1].
- **Pygame** — *Engine* visualisasi dan logika game 2D[cite: 1].

---

## 📁 Struktur Proyek

```text
pong-hand-tracking/
├── 📁 .venv/               # Virtual environment (Lokal)
├── 📄 .gitignore           # File pengabaian Git
├── 📄 README.md            # Dokumentasi proyek
├── 📄 hand_detector.py     # Modul isolasi OpenCV & MediaPipe
├── 📄 game_logic.py        # Modul engine Pygame & objek game
├── 📄 main.py              # Entry point aplikasi
└── 📄 requirements.txt     # Daftar dependency proyek
```

## Persyaratan

- Python 3.12 (direkomendasikan)
- Webcam laptop
- Windows / macOS / Linux

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/pong-hand-tracking.git
cd pong-hand-tracking
```

### 2. Buat virtual environment

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Kalau PowerShell memblokir script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependency

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Jalankan game

```bash
python main.py
```

## Kontrol

- Gerakkan jari telunjuk ke atas dan bawah untuk menggerakkan paddle pemain
- Paddle kanan dikendalikan AI
- Tekan `ESC` untuk keluar
- Tekan `q` pada jendela webcam untuk menutup kamera

## Catatan

Pastikan webcam aktif dan izin akses webcam diberikan.

Jika kamera tidak terbuka, coba ubah:

```python
camera = cv2.VideoCapture(0)
```

menjadi:

```python
camera = cv2.VideoCapture(1)
```

## License

Project ini dibuat untuk pembelajaran dan eksperimen game Python + hand tracking.
