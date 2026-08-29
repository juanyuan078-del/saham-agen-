# config.py
# Konfigurasi daftar saham & kriteria screening.
# Silakan tambah/kurangi kode saham sesuai kebutuhan kamu.

# Daftar saham sektor ENERGI di IDX (batu bara, migas, EBT).
# Format pakai suffix ".JK" karena kita ambil datanya dari Yahoo Finance.
SAHAM_ENERGI = [
    "ADRO.JK",  # Alamtri Resources (d/h Adaro Energy)
    "PTBA.JK",  # Bukit Asam
    "ITMG.JK",  # Indo Tambangraya Megah
    "INDY.JK",  # Indika Energy
    "HRUM.JK",  # Harum Energy
    "BUMI.JK",  # Bumi Resources
    "MEDC.JK",  # Medco Energi
    "ELSA.JK",  # Elnusa
    "PGAS.JK",  # Perusahaan Gas Negara
    "AKRA.JK",  # AKR Corporindo
    "BRPT.JK",  # Barito Pacific
    "DEWA.JK",  # Darma Henwa
    "GEMS.JK",  # Golden Energy Mines
    "TOBA.JK",  # TBS Energi Utama
]

# ==== Kriteria Screening 1: Jangka Panjang (Value + Energi) ====
LONGTERM_CRITERIA = {
    "per_max": 15,
    "pbv_max": 2,
    "roe_min": 0.15,       # 15%
    "der_max": 1.0,
    "dividend_yield_min": 0.03,  # 3%
}

# ==== Kriteria Screening 2: Trading/Momentum ====
TRADING_CRITERIA = {
    "rsi_min": 30,
    "rsi_max": 50,
    "volume_ratio_min": 1.2,  # volume hari ini vs rata-rata 20 hari
}

# Kata kunci untuk deteksi "cerita" akuisisi/korporasi di judul berita
NEWS_KEYWORDS = [
    "akuisisi", "merger", "right issue", "private placement",
    "strategic partner", "investor asing", "divestasi", "konsolidasi",
    "tender offer", "backdoor listing",
]

# Sumber RSS berita (bisa ditambah)
NEWS_RSS_FEEDS = [
    "https://www.cnbcindonesia.com/market/rss",
    "https://www.kontan.co.id/rss/investasi",
]
