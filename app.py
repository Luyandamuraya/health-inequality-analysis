# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Health Inequality Dashboard", layout="wide")

# ------------------------------------------------------
# DARK THEME + CUSTOM COMPONENTS
# ------------------------------------------------------

st.markdown("""
<style>

body, .main {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-family: 'Inter', sans-serif;
}

/* HEADERS */
h1, h2, h3, h4 {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* PARAGRAPH + LABELS */
p, label, span {
    color: #000000 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #F5F7FA !important;
    padding-top: 25px;
    border-right: 1px solid #D0D0D0;
    color: #000000 !important;
}

/* INSIGHT CARDS */
.insight-card {
    background-color: #F2F4F7;
    padding: 18px 20px;
    border-radius: 10px;
    border: 1px solid #D3D3D3;
    margin-bottom: 12px;
}

.insight-title {
    font-size: 19px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 8px;
}

.insight-text {
    font-size: 15px;
    color: #000000;
    line-height: 1.45;
}

/* FIX STREAMLIT WIDGETS */
.stSelectbox label, .stMetric label, .stRadio label {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------
df = pd.read_csv("data/health_inequality_dataset.csv")
gdf = gpd.read_file("data/uk_lad_2023.gpkg")

# ------------------------------------------------------
# RENAME COLUMNS
# ------------------------------------------------------
rename_dict = {
    "area_code": "Area Code",
    "area_name": "Area Name",
    "life_expectancy": "Life Expectancy",
    "num_population": "Population",
    "imd_rank_avg": "IMD Rank",
    "imd_decile_avg": "IMD Decile",
    "edu_rank_avg": "Education Rank",
    "health_rank_avg": "Health Rank",
    "barriers_rank_avg": "Barriers to Housing Rank",
    "living_env_rank_avg": "Living Environment Rank",
    "employment_rank_avg": "Employment Rank",
    "weighted_prev_copd": "COPD Prevalence (%)",
    "weighted_prev_ast": "Asthma Prevalence (%)",
    "weighted_prev_hyp": "Hypertension Prevalence (%)",
    "weighted_prev_bp": "Blood Pressure Prevalence (%)",
    "weighted_prev_obo": "Obesity Prevalence (%)",
    "weighted_achiev_smo": "Smoking Cessation Achievement (%)",
    "gpwalkt": "GP Travel Time (Walk)",
    "gpcyct": "GP Travel Time (Cycle)",
    "gpcart": "GP Travel Time (Car)",
    "gpptt": "GP Travel Time (Public Transport)",
    "hospwalkt": "Hospital Travel Time (Walk)",
    "hospcyct": "Hospital Travel Time (Cycle)",
    "hospcart": "Hospital Travel Time (Car)",
    "hospptt": "Hospital Travel Time (Public Transport)",
    "emissions_pp": "Emissions Per Capita (kg)",
    "emissions_tons": "Total Emissions (tons)",
    "wightd_mmrc1_perc_vac": "MMR Dose 1 (%)",
    "wightd_mmrc2_perc_vac": "MMR Dose 2 (%)",
    "wightd_dtapipv_perc_vac": "DTaP/IPV (%)",
    "wightd_hibmenc_perc_vac": "Hib/MenC (%)",
    "deaths_per_100k": "Deaths Per 100k",
}
df = df.rename(columns=rename_dict)

# ------------------------------------------------------
# ROUND ALL NUMERIC COLUMNS (2 DECIMAL PLACES)
# ------------------------------------------------------
for col in df.select_dtypes(include=[np.number]).columns:
    df[col] = df[col].round(2)

# ------------------------------------------------------
# GEO MERGE + CLEAN
# ------------------------------------------------------
gdf = gdf.to_crs(epsg=4326)
merged = gdf.merge(df, left_on="LAD23CD", right_on="Area Code", how="left")
merged["geometry"] = merged["geometry"].buffer(0).simplify(0.005, preserve_topology=True)

# ------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------
MENU = ["Overview", "Map", "Inequalities", "Comparison"]
page = st.sidebar.selectbox("Navigation", MENU)

# ------------------------------------------------------
# PAGE 1 — OVERVIEW
# ------------------------------------------------------
if page == "Overview":

    st.markdown("<h1>Health Inequality Across England</h1>", unsafe_allow_html=True)
    st.write("Explore structural, behavioural and environmental determinants of inequality.")

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Life Expectancy", f"{df['Life Expectancy'].mean():.2f} yrs")
    c2.metric("Average IMD Rank", f"{df['IMD Rank'].mean():.2f}")
    c3.metric("Average GP Walk Time", f"{df['GP Travel Time (Walk)'].mean():.2f} mins")
    c4.metric("Average Asthma Prevalence", f"{df['Asthma Prevalence (%)'].mean():.2f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            df,
            x="IMD Rank",
            y="Life Expectancy",
            color="Life Expectancy",
            color_continuous_scale="Viridis",
            title="Life Expectancy vs IMD Rank"
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            df,
            x="Emissions Per Capita (kg)",
            y="Asthma Prevalence (%)",
            color="Asthma Prevalence (%)",
            size="Population",
            color_continuous_scale="Inferno",
            title="Asthma Prevalence vs Emissions"
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------
    # CORRELATION HEATMAP
    # ------------------------------------------------------
    st.subheader("Correlation Heatmap")

    heat_cols = [
        "Life Expectancy",
        "IMD Rank",
        "COPD Prevalence (%)",
        "Asthma Prevalence (%)",
        "Smoking Cessation Achievement (%)",
        "Emissions Per Capita (kg)"
    ]

    corr = df[heat_cols].corr().round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Inferno",
        labels=dict(color="Correlation")
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------
    # AI-GENERATED INSIGHTS — CLEAN VERSION
    # ------------------------------------------------------
    st.markdown("<h3>Automated Insights</h3>", unsafe_allow_html=True)

    corr_pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .reset_index()
    )
    corr_pairs.columns = ["Feature A", "Feature B", "Correlation"]
    corr_pairs["abs_corr"] = corr_pairs["Correlation"].abs()

    top_pos = corr_pairs.sort_values("Correlation", ascending=False).head(3)
    top_neg = corr_pairs.sort_values("Correlation").head(3)
    weak = corr_pairs.sort_values("abs_corr").head(2)

    # Positive
    st.markdown("<div class='insight-card'><div class='insight-title'>Strongest Positive Relationships</div>", unsafe_allow_html=True)
    for _, r in top_pos.iterrows():
        st.markdown(
            f"<div class='insight-text'>• {r['Feature A']} and {r['Feature B']} "
            f"move together strongly (r = {r['Correlation']:.2f}).</div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Negative
    st.markdown("<div class='insight-card'><div class='insight-title'>Strongest Negative Relationships</div>", unsafe_allow_html=True)
    for _, r in top_neg.iterrows():
        st.markdown(
            f"<div class='insight-text'>• {r['Feature A']} decreases as {r['Feature B']} increases "
            f"(r = {r['Correlation']:.2f}).</div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Weak
    st.markdown("<div class='insight-card'><div class='insight-title'>Weak or Minimal Relationships</div>", unsafe_allow_html=True)
    for _, r in weak.iterrows():
        st.markdown(
            f"<div class='insight-text'>• There is limited linear association between "
            f"{r['Feature A']} and {r['Feature B']} (r = {r['Correlation']:.2f}).</div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)



# ------------------------------------------------------
# PAGE 2 — MAP
# ------------------------------------------------------
if page == "Map":

    st.title("Interactive Inequality Map")

    map_groups = {
        "Health Outcomes": ["Life Expectancy", "Deaths Per 100k"],
        "Deprivation": ["IMD Rank", "IMD Decile", "Education Rank", "Health Rank", "Employment Rank"],
        "Chronic Disease": ["COPD Prevalence (%)", "Asthma Prevalence (%)", "Hypertension Prevalence (%)"],
        "Behaviour": ["Smoking Cessation Achievement (%)"],
        "Access to Services": [
            "GP Travel Time (Walk)", "GP Travel Time (Cycle)", "GP Travel Time (Car)",
            "GP Travel Time (Public Transport)", "Hospital Travel Time (Walk)",
            "Hospital Travel Time (Cycle)", "Hospital Travel Time (Car)", "Hospital Travel Time (Public Transport)"
        ],
        "Environment": ["Emissions Per Capita (kg)", "Total Emissions (tons)"],
        "Vaccination": ["MMR Dose 1 (%)", "MMR Dose 2 (%)", "DTaP/IPV (%)", "Hib/MenC (%)"]
    }

    category = st.selectbox("Category", map_groups.keys())
    metric = st.selectbox("Metric", map_groups[category])

    merged[metric] = merged[metric].fillna(0)

    # Build simple GeoJSON
    features = [
        {"type": "Feature",
         "geometry": row["geometry"].__geo_interface__,
         "properties": {"LAD23CD": row["LAD23CD"]}}
        for _, row in merged.iterrows()
    ]
    geojson = {"type": "FeatureCollection", "features": features}

    fig = px.choropleth_mapbox(
        merged,
        geojson=geojson,
        locations="LAD23CD",
        featureidkey="properties.LAD23CD",
        color=metric,
        color_continuous_scale="Viridis",
        mapbox_style="carto-darkmatter",
        hover_name="Area Name",
        center={"lat": 53.5, "lon": -1.5},
        zoom=5,
        opacity=0.75,
        height=700
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------
# PAGE 3 — INEQUALITIES
# ------------------------------------------------------
if page == "Inequalities":

    st.title("Inequality Profiles")

    metric = st.selectbox("Select Indicator", df.columns[2:])
    st.subheader("Top 10 Areas")
    st.dataframe(df.nlargest(10, metric)[["Area Name", metric]])

    st.subheader("Bottom 10 Areas")
    st.dataframe(df.nsmallest(10, metric)[["Area Name", metric]])


# ------------------------------------------------------
# PAGE 4 — COMPARISON
# ------------------------------------------------------
if page == "Comparison":

    st.title("Compare Areas")

    a1, a2 = st.columns(2)
    area1 = a1.selectbox("Area 1", df["Area Name"].unique())
    area2 = a2.selectbox("Area 2", df["Area Name"].unique())

    d1 = df[df["Area Name"] == area1].iloc[0]
    d2 = df[df["Area Name"] == area2].iloc[0]

    metrics = [
        "Life Expectancy", "IMD Rank",
        "Asthma Prevalence (%)", "COPD Prevalence (%)",
        "Emissions Per Capita (kg)"
    ]

    cols = st.columns(len(metrics))

    for col, m in zip(cols, metrics):
        col.metric(m, f"{d1[m]:.2f}", f"{d1[m] - d2[m]:+.2f}")
