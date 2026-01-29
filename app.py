import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração básica da página
st.set_page_config(
    page_title="Vehicles Dashboard MX",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")  # seu arquivo renomeado
    return df

# Carregar dados
df = load_data()

st.title("Vehicles Dashboard MX")
st.markdown("Análise exploratória dos anúncios de veículos (dataset `vehicles_us`).")

# Mostrar uma amostra dos dados
with st.expander("Ver amostra dos dados"):
    st.write(df.head())
    st.write("Formato do dataset:", df.shape)

# --- Barra lateral de filtros ---
st.sidebar.header("Filtros")

# Filtro por ano do modelo (se existir a coluna)
if "model_year" in df.columns and df["model_year"].notna().any():
    year_min = int(df["model_year"].min())
    year_max = int(df["model_year"].max())

    year_range = st.sidebar.slider(
        "Ano do modelo",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max)
    )
else:
    year_range = None

# Filtro por condição do veículo (se existir a coluna)
if "condition" in df.columns:
    condition_options = ["all"] + sorted(df["condition"].dropna().unique().tolist())
    condition = st.sidebar.selectbox("Condição do veículo", condition_options)
else:
    condition = "all"

# --- Aplicar filtros ---
df_filtered = df.copy()

if year_range is not None and "model_year" in df_filtered.columns:
    df_filtered = df_filtered[
        (df_filtered["model_year"] >= year_range[0]) &
        (df_filtered["model_year"] <= year_range[1])
    ]
if condition != "all" and "condition" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["condition"] == condition]

# --- Checkbox para mostrar dados brutos ---
show_data = st.checkbox('Mostrar tabela de dados brutos')

if show_data:
    st.subheader('Tabela de dados filtrados')
    st.dataframe(df_filtered)

st.subheader("Resumo dos dados filtrados")
st.write(df_filtered.describe(include="all"))

# --- Gráfico 1: Distribuição de preços ---
if "price" in df_filtered.columns:
    st.subheader("Distribuição de preços dos veículos")
    fig_price = px.histogram(
        df_filtered,
        x="price",
        nbins=50,
        title="Distribuição de preços"
    )
    st.plotly_chart(fig_price, use_container_width=True)
else:
    st.info("Coluna 'price' não encontrada no dataset.")

# --- Gráfico 2: Preço vs Quilometragem ---
if "price" in df_filtered.columns and "odometer" in df_filtered.columns:
    st.subheader("Relação entre preço e quilometragem")
    fig_scatter = px.scatter(
        df_filtered,
        x="odometer",
        y="price",
        color="condition" if "condition" in df_filtered.columns else None,
        title="Preço vs Quilometragem por condição",
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Coluna 'odometer' ou 'price' não encontrada no dataset.")

# --- Gráfico 3: Contagem por tipo de veículo ---
if "type" in df_filtered.columns:
    st.subheader("Contagem de veículos por tipo")
    contagem_tipo = df_filtered["type"].value_counts().reset_index()
    contagem_tipo.columns = ["Tipo", "Quantidade"]

    fig_type = px.bar(
        contagem_tipo,
        x="Tipo",
        y="Quantidade",
        title="Quantidade de veículos por tipo"
    )
    st.plotly_chart(fig_type, use_container_width=True)
else:
    st.info("Coluna 'type' não encontrada no dataset.")



