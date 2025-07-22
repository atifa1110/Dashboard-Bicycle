import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ======================
# 🔧 PENGATURAN AWAL
# ======================
st.set_page_config(page_title="Dashboard Peminjaman Sepeda", layout="wide")
st.title("Dashboard Peminjaman Sepeda")
sns.set_theme(style="whitegrid")

# ======================
# 📥 LOAD DATA
# ======================
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# ======================
# 🎛️ SIDEBAR FILTER
# ======================
st.sidebar.header("🎚️ Filter")

# Konversi ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Ambil tahun minimum dan maksimum dari data
min_year = day_df['dteday'].dt.year.min()
max_year = day_df['dteday'].dt.year.max()

# Filter berdasarkan tahun dari data (otomatis, tidak hardcode)
filtered_day_df = day_df[
    (day_df['dteday'].dt.year >= min_year) & (day_df['dteday'].dt.year <= max_year)
]

# Tampilkan info tahun yang ditampilkan
st.sidebar.info(f"Menampilkan data tahun {min_year} - {max_year}")

# ======================
# 🔁 TRANSFORMASI DATA
# ======================

# Tambah label musim
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_label'] = day_df['season'].map(season_map)

# Tambah label tahun
day_df['year'] = day_df['yr'].map({0: 2011, 1: 2012})

# Kategori hari
def categorize_day(row):
    if row['holiday'] == 1:
        return 'Hari Libur'
    elif row['workingday'] == 0:
        return 'Akhir Pekan'
    else:
        return 'Hari Kerja'
day_df['day_category'] = day_df.apply(categorize_day, axis=1)

# Cuaca jam
weather_map = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}
hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)

# ======================
# 🧾 TAMPILAN DATA AWAL
# ======================
col1, col2 = st.columns(2)
with col1:
    st.subheader("Data Harian")
    st.write(day_df.head())
with col2:
    st.subheader("Data Jam")
    st.write(hour_df.head())

# ======================
# 📊 GRAFIK 1: Rata-rata per Jam
# ======================
st.subheader("Rata-rata Jumlah Peminjaman Sepeda per Jam")
hourly_avg = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', ax=ax)
ax.set(title="Rata-rata Jumlah Peminjaman Sepeda per Jam", xlabel="Jam (0 - 23)", ylabel="Rata-rata Peminjaman")
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

# ======================
# 📊 GRAFIK 2 & 3 : Pie chart + Bar kategori hari
# ======================
col3, col4 = st.columns(2)
with col3:
    st.subheader("Distribusi Pengguna: Kasual vs Terdaftar")
    total_casual = day_df['casual'].sum()
    total_registered = day_df['registered'].sum()
    labels = ['Pengguna Kasual', 'Pengguna Terdaftar']
    sizes = [total_casual, total_registered]
    colors = ['#66c2a5', '#fc8d62']
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.05, 0))
    ax1.set_title('Persentase Total Peminjaman')
    ax1.axis('equal')
    st.pyplot(fig1)

with col4:
    st.subheader("Rata-rata Peminjaman Berdasarkan Kategori Hari")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=day_df, x='day_category', y='cnt', estimator='mean',
                hue='day_category', palette='Set2', legend=False, ax=ax2)
    ax2.set_title('Peminjaman per Kategori Hari')
    ax2.set_xlabel('Kategori Hari')
    ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
    fig2.tight_layout()
    st.pyplot(fig2)

# ======================
# 📊 GRAFIK 4: Jam Sibuk & Cuaca
# ======================
st.subheader("Rata-rata Jumlah Peminjam Sepeda saat Jam Sibuk berdasarkan Cuaca")
rush_hours = [7, 8, 9, 16, 17, 18]
rush_df = hour_df[hour_df['hr'].isin(rush_hours)]
grouped = rush_df.groupby(['hr', 'weather_label'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=grouped, x='hr', y='cnt', hue='weather_label', marker='o', ax=ax)
ax.set(title='Rata-rata Jumlah Peminjam Sepeda pada Jam Sibuk Berdasarkan Cuaca',
       xlabel='Jam (0-23)', ylabel='Rata-rata Jumlah Peminjam')
ax.grid(True)
st.pyplot(fig)

# ======================
# 📊 GRAFIK 5 & 6: Rata-rata per Musim + Musim vs Tahun
# ======================
col5, col6 = st.columns(2)
with col5:
    st.subheader("Rata-rata Jumlah Peminjaman Sepeda per Musim")
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=day_df, x='season_label', y='cnt', hue='season_label',
                estimator='mean', palette='coolwarm', legend=False, ax=ax3)
    ax3.set_title('Peminjaman per Musim')
    ax3.set_xlabel('Musim')
    ax3.set_ylabel('Rata-rata Jumlah Peminjaman')
    fig3.tight_layout()
    st.pyplot(fig3)

with col6:
    st.subheader("Perbandingan Rata-rata Peminjaman per Musim dan Tahun")
    season_year_df = day_df.groupby(['yr', 'season_label'])['cnt'].mean().reset_index()
    season_year_df['year'] = season_year_df['yr'].map({0: 2011, 1: 2012})
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=season_year_df, x='season_label', y='cnt', hue='year', palette='coolwarm', ax=ax4)
    ax4.set_title('Peminjaman Musiman per Tahun')
    ax4.set_xlabel('Musim')
    ax4.set_ylabel('Rata-rata Jumlah Peminjaman')
    fig4.tight_layout()
    st.pyplot(fig4)