# Pong Hand Tracking

Game Pong 2D klasik yang dikendalikan menggunakan hand tracking melalui webcam laptop.

## Teknologi

- Python 3
- OpenCV
- MediaPipe
- Pygame

## Fitur

- Control paddle pemain dengan gerakan tangan
- AI sederhana untuk lawan
- Bola dan fisika Pong
- Sistem skor
- Status deteksi tangan: YES / NO
- Tampilan landmark tangan di jendela webcam

## Struktur Project

```text
pong-hand-tracking/
├── .gitignore
├── README.md
├── hand_detector.py
├── game_logic.py
├── main.py
├── requirements.txt
└── .venv/   # dibuat lokal, tidak di-upload ke GitHub
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
