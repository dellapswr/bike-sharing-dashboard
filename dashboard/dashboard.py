
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# Konfigurasi halaman dashboard
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Membaca dataset hasil pengolahan
@st.cache_data
def load_data():
    data_path = Path(__file__).resolve().parent / "main_data.csv"
    df = pd.read_csv(data_path, parse_dates=["dteday"])
    return df

main_df = load_data()
# Filter interaktif berdasarkan tahun
main_df["year"] = main_df["dteday"].dt.year

selected_years = st.sidebar.multiselect(
    "Pilih Tahun",
    options=[2011, 2012],
    default=[2011, 2012]
)

# Mencegah analisis dijalankan saat tidak ada tahun yang dipilih
if not selected_years:
    st.warning("⚠️ Pilih minimal satu tahun (2011 atau 2012) untuk menampilkan analisis.")
    st.stop()

filtered_df = main_df[
    main_df["year"].isin(selected_years)
].copy()

# Judul dan pengantar dashboard
st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    "Analisis penyewaan sepeda berdasarkan musim, kondisi cuaca, "
    "jenis hari, dan pola permintaan per jam selama periode 2011–2012."
)

# Ringkasan indikator utama (KPI)
st.subheader("📊 Ringkasan Penyewaan Sepeda")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Penyewaan",
        value=f"{filtered_df['cnt'].sum():,}"
    )

with col2:
    st.metric(
        label="Total Pengguna Casual",
        value=f"{filtered_df['casual'].sum():,}"
    )

with col3:
    st.metric(
        label="Total Pengguna Registered",
        value=f"{filtered_df['registered'].sum():,}"
    )

periode_terpilih = (
    ", ".join(str(tahun) for tahun in sorted(selected_years))
    if selected_years
    else "Tidak ada tahun dipilih"
)

st.caption(
    f"Sumber: Bike Sharing Dataset | Tahun dipilih: {periode_terpilih}"
)

# Visualisasi pertanyaan bisnis 1: rata-rata penyewaan berdasarkan musim
st.divider()
st.subheader("🌤️ Rata-rata Penyewaan Sepeda Berdasarkan Musim")

season_order = ["Spring", "Summer", "Fall", "Winter"]

# Agregasi data per hari agar konsisten dengan analisis notebook
daily_df = (
    filtered_df.groupby(
        ["dteday", "season_label"],
        as_index=False
    )["cnt"]
    .sum()
)

season_avg = (
    daily_df.groupby("season_label", as_index=False)["cnt"]
    .mean()
)

season_avg["season_label"] = pd.Categorical(
    season_avg["season_label"],
    categories=season_order,
    ordered=True
)

season_avg = season_avg.sort_values("season_label")

season_chart = (
    alt.Chart(season_avg)
    .mark_bar(color="#3B82F6")
    .encode(
        x=alt.X(
            "season_label:N",
            sort=season_order,
            title="Musim",
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "cnt:Q",
            title="Rata-rata Penyewaan per Hari"
        ),
        tooltip=[
            alt.Tooltip("season_label:N", title="Musim"),
            alt.Tooltip("cnt:Q", title="Rata-rata Penyewaan", format=",.2f")
        ]
    )
    .properties(height=350)
)

st.altair_chart(season_chart, use_container_width=True)

st.caption(
    "Grafik menunjukkan rata-rata jumlah penyewaan sepeda per hari "
    f"untuk setiap musim. Tahun dipilih: {periode_terpilih}."
)

# Insight musim yang mengikuti pilihan tahun
if not season_avg.empty:
    highest_season = season_avg.loc[season_avg["cnt"].idxmax()]
    lowest_season = season_avg.loc[season_avg["cnt"].idxmin()]

    st.info(
        f"💡 Insight: Pada tahun yang dipilih, musim "
        f"{highest_season['season_label']} memiliki rata-rata penyewaan "
        f"tertinggi sebesar {highest_season['cnt']:,.2f} penyewaan per hari. "
        f"Sementara itu, musim {lowest_season['season_label']} memiliki "
        f"rata-rata terendah sebesar {lowest_season['cnt']:,.2f} "
        f"penyewaan per hari. Temuan ini dapat menjadi pertimbangan "
        f"dalam perencanaan kesiapan armada berdasarkan musim."
    )

# Visualisasi pertanyaan bisnis 1: rata-rata penyewaan berdasarkan cuaca
st.divider()
st.subheader("🌦️ Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

# Menggunakan data harian agar konsisten dengan notebook analisis utama
day_data_path = Path(__file__).resolve().parent / "day.csv"
weather_day_df = pd.read_csv(day_data_path)

# Filter data harian sesuai tahun yang dipilih
weather_day_df["dteday"] = pd.to_datetime(weather_day_df["dteday"])

weather_day_df = weather_day_df[
    weather_day_df["dteday"].dt.year.isin(selected_years)
].copy()

weather_labels = {
    1: "Clear",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

weather_day_df["weather_label"] = (
    weather_day_df["weathersit"].map(weather_labels)
)

weather_avg = (
    weather_day_df.groupby("weather_label", as_index=False)["cnt"]
    .mean()
    .rename(columns={"cnt": "avg_rentals"})
)

weather_order = [
    "Clear",
    "Mist/Cloudy",
    "Light Rain/Snow",
    "Heavy Rain/Snow"
]

weather_chart = (
    alt.Chart(weather_avg)
    .mark_bar(color="#14B8A6")
    .encode(
        x=alt.X(
            "weather_label:N",
            sort=weather_order,
            title="Kondisi Cuaca",
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "avg_rentals:Q",
            title="Rata-rata Penyewaan per Hari"
        ),
        tooltip=[
            alt.Tooltip("weather_label:N", title="Kondisi Cuaca"),
            alt.Tooltip(
                "avg_rentals:Q",
                title="Rata-rata Penyewaan",
                format=",.2f"
            )
        ]
    )
    .properties(height=350)
)

st.altair_chart(weather_chart, use_container_width=True)

st.caption(
    "Rata-rata penyewaan sepeda per hari berdasarkan kondisi cuaca. "
    f"Tahun dipilih: {periode_terpilih}. "
    "Kategori tanpa observasi tidak ditampilkan."
)

# Insight kondisi cuaca yang mengikuti filter tahun
if not weather_avg.empty:
    highest_weather = weather_avg.loc[weather_avg["avg_rentals"].idxmax()]
    lowest_weather = weather_avg.loc[weather_avg["avg_rentals"].idxmin()]

    st.info(
        f"💡 Insight: Pada tahun yang dipilih, kondisi cuaca "
        f"{highest_weather['weather_label']} memiliki rata-rata penyewaan "
        f"tertinggi sebesar {highest_weather['avg_rentals']:,.2f} "
        f"penyewaan per hari. Sebaliknya, kondisi cuaca "
        f"{lowest_weather['weather_label']} memiliki rata-rata terendah "
        f"sebesar {lowest_weather['avg_rentals']:,.2f} penyewaan per hari. "
        f"Perbedaan ini dapat menjadi pertimbangan dalam perencanaan "
        f"operasional berdasarkan kondisi cuaca, tanpa mengasumsikan "
        f"hubungan sebab-akibat."
    )


# Visualisasi pertanyaan bisnis 2: pola penyewaan berdasarkan jam dan jenis hari
st.divider()
st.subheader("🕒 Pola Penyewaan per Jam Berdasarkan Jenis Hari")

hourly_avg = (
    filtered_df.groupby(
        ["hr", "day_type"],
        as_index=False
    )["cnt"]
    .mean()
    .rename(columns={"cnt": "avg_rentals"})
)

day_type_order = ["Working Day", "Non-Working Day"]

hourly_chart = (
    alt.Chart(hourly_avg)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X(
            "hr:Q",
            title="Jam",
            scale=alt.Scale(domain=[0, 23]),
            axis=alt.Axis(values=list(range(24)), labelAngle=0)
        ),
        y=alt.Y(
            "avg_rentals:Q",
            title="Rata-rata Penyewaan per Jam"
        ),
        color=alt.Color(
            "day_type:N",
            title="Jenis Hari",
            sort=day_type_order,
            scale=alt.Scale(
                domain=day_type_order,
                range=["#3B82F6", "#F59E0B"]
            )
        ),
        tooltip=[
            alt.Tooltip("hr:Q", title="Jam", format=".0f"),
            alt.Tooltip("day_type:N", title="Jenis Hari"),
            alt.Tooltip(
                "avg_rentals:Q",
                title="Rata-rata Penyewaan",
                format=",.2f"
            )
        ]
    )
    .properties(height=380)
)

st.altair_chart(hourly_chart, use_container_width=True)

st.caption(
    "Rata-rata jumlah penyewaan pada setiap jam tercatat, "
    "dibandingkan antara Working Day dan Non-Working Day. "
    f"Tahun dipilih: {periode_terpilih}."
)

# Insight pola penyewaan yang mengikuti filter tahun
if not hourly_avg.empty:
    working_avg = hourly_avg[
        hourly_avg["day_type"] == "Working Day"
    ]

    nonworking_avg = hourly_avg[
        hourly_avg["day_type"] == "Non-Working Day"
    ]

    if not working_avg.empty and not nonworking_avg.empty:
        working_peak = working_avg.loc[
            working_avg["avg_rentals"].idxmax()
        ]

        nonworking_peak = nonworking_avg.loc[
            nonworking_avg["avg_rentals"].idxmax()
        ]

        st.info(
            f"💡 Insight: Pada tahun yang dipilih, puncak rata-rata "
            f"penyewaan Working Day terjadi pukul "
            f"{int(working_peak['hr']):02d}.00 dengan rata-rata "
            f"{working_peak['avg_rentals']:,.2f} penyewaan per jam tercatat. "
            f"Sementara itu, puncak Non-Working Day terjadi pukul "
            f"{int(nonworking_peak['hr']):02d}.00 dengan rata-rata "
            f"{nonworking_peak['avg_rentals']:,.2f} penyewaan per jam tercatat. "
            f"Perbedaan pola ini dapat membantu menentukan prioritas "
            f"kesiapan armada berdasarkan permintaan historis."
        )


# Analisis lanjutan: rule-based clustering menggunakan binning
st.divider()
st.subheader("🔥 Segmentasi Tingkat Permintaan Berdasarkan Jam dan Jenis Hari")

# Menggunakan rata-rata penyewaan dari 48 kombinasi jam dan jenis hari
demand_df = hourly_avg.copy()

# Menentukan batas kategori berdasarkan persentil
low_threshold = demand_df["avg_rentals"].quantile(1 / 3)
high_threshold = demand_df["avg_rentals"].quantile(2 / 3)

# Mengelompokkan tingkat permintaan
demand_df["demand_level"] = pd.cut(
    demand_df["avg_rentals"],
    bins=[-float("inf"), low_threshold, high_threshold, float("inf")],
    labels=["Low Demand", "Medium Demand", "High Demand"],
    include_lowest=True
)

demand_order = ["Low Demand", "Medium Demand", "High Demand"]

# Membuat heatmap interaktif
demand_heatmap = (
    alt.Chart(demand_df)
    .mark_rect(stroke="#1F2937", strokeWidth=1)
    .encode(
        x=alt.X(
            "hr:O",
            title="Jam",
            sort=list(range(24)),
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y(
            "day_type:N",
            title="Jenis Hari",
            sort=["Working Day", "Non-Working Day"]
        ),
        color=alt.Color(
            "demand_level:N",
            title="Tingkat Permintaan",
            sort=demand_order,
            scale=alt.Scale(
                domain=demand_order,
                range=["#BFDBFE", "#60A5FA", "#1D4ED8"]
            )
        ),
        tooltip=[
            alt.Tooltip("hr:O", title="Jam"),
            alt.Tooltip("day_type:N", title="Jenis Hari"),
            alt.Tooltip("demand_level:N", title="Kategori"),
            alt.Tooltip(
                "avg_rentals:Q",
                title="Rata-rata Penyewaan",
                format=",.2f"
            )
        ]
    )
    .properties(height=220)
)

st.altair_chart(demand_heatmap, use_container_width=True)

st.caption(
    "Segmentasi menggunakan rule-based clustering dengan teknik "
    "binning berdasarkan persentil 33,33% dan 66,67% dari "
    "48 kombinasi jam dan jenis hari. "
    f"Tahun dipilih: {periode_terpilih}. "
    "Kategori menunjukkan tingkat permintaan relatif historis."
)

st.write("Jumlah kombinasi per kategori:")
st.dataframe(
    demand_df["demand_level"]
    .value_counts()
    .reindex(demand_order)
    .rename_axis("Kategori")
    .reset_index(name="Jumlah Kombinasi"),
    hide_index=True
)

# Insight analisis lanjutan yang mengikuti filter tahun
def format_jam(jam_list):
    jam_list = sorted(int(jam) for jam in jam_list)

    if not jam_list:
        return "tidak ditemukan"

    rentang = []
    awal = akhir = jam_list[0]

    for jam in jam_list[1:]:
        if jam == akhir + 1:
            akhir = jam
        else:
            rentang.append(
                f"{awal:02d}.00"
                if awal == akhir
                else f"{awal:02d}.00–{akhir:02d}.00"
            )
            awal = akhir = jam

    rentang.append(
        f"{awal:02d}.00"
        if awal == akhir
        else f"{awal:02d}.00–{akhir:02d}.00"
    )

    return " dan ".join(rentang)


jumlah_kategori = demand_df["demand_level"].value_counts()

working_high = demand_df[
    (demand_df["day_type"] == "Working Day")
    & (demand_df["demand_level"] == "High Demand")
]["hr"]

nonworking_high = demand_df[
    (demand_df["day_type"] == "Non-Working Day")
    & (demand_df["demand_level"] == "High Demand")
]["hr"]

st.info(
    f"💡 Insight Analisis Lanjutan: Pada tahun {periode_terpilih}, "
    f"segmentasi menghasilkan "
    f"{jumlah_kategori.get('Low Demand', 0)} kombinasi Low Demand, "
    f"{jumlah_kategori.get('Medium Demand', 0)} kombinasi Medium Demand, "
    f"dan {jumlah_kategori.get('High Demand', 0)} kombinasi High Demand. "
    f"Pada Working Day, High Demand ditemukan pada pukul "
    f"{format_jam(working_high)}. "
    f"Sementara itu, pada Non-Working Day, High Demand ditemukan "
    f"pada pukul {format_jam(nonworking_high)}. "
    f"Kategori ini menunjukkan tingkat permintaan historis relatif, "
    f"bukan kapasitas armada aktual."
)