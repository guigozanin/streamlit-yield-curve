import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pandas_datareader as pdr

# Função para pegar os dados da curva de juros
def retrieve_us_yield_curve_data():
    start = '1990-01-01'
    tickers = ['GS30', 'GS10', 'GS5', 'GS3', 'GS2', 'GS1', 'GS6m', 'GS3m', 'GS1m']
    df = pdr.get_data_fred(tickers, start)
    df.columns = ['30-year', '10-year', '5-year', '3-year', '2-year', '1-year', '6-month', '3-month', '1-month']
    df.index = df.index + pd.offsets.MonthEnd(0)
    df.index = df.index.strftime('%d-%m-%Y')  # Alteração do formato da data
    return df

# Função para criar o gráfico 3D da curva de juros
def plot_yield_curve_surface(df, source_text):
    fig = go.Figure()
    fig.add_trace(
        go.Surface(x=df.columns,
                   y=df.index,
                   z=df.values,
                   colorscale='RdYlGn',
                   reversescale=True)
    )
    fig.update_layout(
        title='Superfície de Juros - Gráfico 3D',
        height=600,
        scene=dict(
            xaxis_title="Duration",
            yaxis_title="Período",
            zaxis_title="Taxa %"
        )
    )
    return fig

# Interface do Streamlit
st.title("📈 Superfície da Curva de Juros dos EUA")
st.write("Este app exibe a evolução da curva de juros americana ao longo do tempo.")

# Carregar os dados
with st.spinner('Carregando dados...'):
    base = retrieve_us_yield_curve_data()

# Exibir tabela de dados
st.subheader("📊 Dados da Curva de Juros")
st.write(base.tail())

# Exibir gráfico 3D
st.subheader("📉 Gráfico 3D da Curva de Juros")
fig = plot_yield_curve_surface(base, "Fonte: FRED, elaboração Guilherme Zanin, CFA")
st.plotly_chart(fig)

st.subheader("Gui Zanin, CFA - Fonte: FRED")

