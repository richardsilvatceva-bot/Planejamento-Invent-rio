import streamlit as st
import pandas as pd
import io

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Planejamento de Inventário Cíclico",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# FUNÇÕES DE APOIO
# ==========================================
@st.cache_data
def carregar_dados():
    # Substitua pelo caminho correto do seu arquivo
    caminho_arquivo = "01 - Planejamento de Curva 2026 V2 (1).xlsx"
    # Pula as duas primeiras linhas de cabeçalho conforme a estrutura da sua planilha
    df = pd.read_excel(caminho_arquivo, sheet_name="PLANEJAMENTO", skiprows=2)
    
    # Tratamento básico de dados (garantir que VALOR TOTAL seja numérico)
    if 'VALOR TOTAL' in df.columns:
        df['VALOR TOTAL'] = pd.to_numeric(df['VALOR TOTAL'], errors='coerce').fillna(0)
    
    return df

def converter_para_excel(df):
    """
    Converte um DataFrame do Pandas nativamente para Excel (.xlsx) na memória.
    Isso resolve o problema de dados agrupados na mesma coluna do CSV.
    """
    output = io.BytesIO()
    # Usamos o engine openpyxl para gerar o arquivo .xlsx
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Planilha1')
    processed_data = output.getvalue()
    return processed_data


# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================
try:
    df_base = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
    st.stop()

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
# (Se você tiver a imagem logo.png, descomente a linha abaixo. 
# Caso contrário, deixei um markdown estilizado como placeholder)
# st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.markdown("<h2 style='text-align: center; color: red;'>📦 GESTÃO DE ESTOQUE</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# 1. FILTRO DE VALOR PLANEJADO (Adicionado aqui em cima)
st.sidebar.markdown("### 💰 Filtro de Valor Planejado")
if 'VALOR TOTAL' in df_base.columns:
    max_valor = float(df_base['VALOR TOTAL'].max())
    # Evita erro caso o max_valor seja 0
    if max_valor == 0: max_valor = 100.0 
    
    valor_min, valor_max = st.sidebar.slider(
        "Intervalo (R$):",
        min_value=0.0,
        max_value=max_valor,
        value=(0.0, max_valor),
        step=100.0,
        format="R$ %.2f"
    )
else:
    st.sidebar.warning("Coluna 'VALOR TOTAL' não encontrada.")
    valor_min, valor_max = 0, 99999999

st.sidebar.markdown("---")

# 2. FILTROS DA CURVA ABC
st.sidebar.markdown("### ⚙️ Filtros da Curva ABC")

qtd_a = st.sidebar.number_input("Qtd. SKUs Curva A", min_value=0, value=7)
qtd_b = st.sidebar.number_input("Qtd. SKUs Curva B", min_value=0, value=2)
qtd_c = st.sidebar.number_input("Qtd. SKUs Curva C", min_value=0, value=2)

st.sidebar.markdown("**Filtrar Curva A por ciclo:**")
ciclo = st.sidebar.radio(
    "",
    ["Todas", "1ª contagem", "2ª contagem", "3ª contagem"],
    label_visibility="collapsed"
)

# ==========================================
# LÓGICA DE FILTRAGEM DOS DADOS
# ==========================================
# Filtra pelo valor planejado
df_filtrado = df_base[
    (df_base['VALOR TOTAL'] >= valor_min) & 
    (df_base['VALOR TOTAL'] <= valor_max)
]

# (Aqui você pode adicionar sua lógica para selecionar as quantidades exatas de curva A, B e C)
# Exemplo genérico de como você estaria limitando as linhas para demonstração:
df_a = df_filtrado[df_filtrado['Curva ABC'] == 'A'].head(qtd_a)
df_b = df_filtrado[df_filtrado['Curva ABC'] == 'B'].head(qtd_b)
df_c = df_filtrado[df_filtrado['Curva ABC'] == 'C'].head(qtd_c)
df_lote = pd.concat([df_a, df_b, df_c])


# ==========================================
# CORPO PRINCIPAL
# ==========================================
st.title("ceva 🔺 Sistema de Planejamento de Inventário Cíclico")

# Criação das Abas
tab1, tab2, tab3 = st.tabs(["📋 Planejamento Diário (Lote)", "📊 Dashboard Gerencial", "🔒 Detalhamento dos Itens Bloqueados"])

# ------------------------------------------
# ABA 1: PLANEJAMENTO DIÁRIO
# ------------------------------------------
with tab1:
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    skus_selecionados = len(df_lote)
    total_locacoes = df_lote['TOTAL POSIÇÕES'].sum() if 'TOTAL POSIÇÕES' in df_lote.columns else 0
    
    col1.metric("SKUs Selecionados", skus_selecionados)
    col2.metric("Total de Locações", int(total_locacoes))
    col3.metric("Meta Operacional", "150 a 200")
    
    # Mensagem de sucesso
    if 150 <= total_locacoes <= 200:
        st.success("✅ **Sucesso:** O lote selecionado está DENTRO da média de locações planejada!")
    elif total_locacoes > 200:
        st.error("⚠️ **Atenção:** O lote selecionado está ACIMA da média de locações planejada!")
    else:
        st.warning("⚠️ **Atenção:** O lote selecionado está ABAIXO da média de locações planejada!")
        
    st.dataframe(df_lote, use_container_width=True)
    
    # Botão de exportação em Excel para o lote diário
    excel_lote = converter_para_excel(df_lote)
    st.download_button(
        label="📥 Exportar Lote para Excel",
        data=excel_lote,
        file_name="Lote_Planejamento.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ------------------------------------------
# ABA 2: DASHBOARD GERENCIAL
# ------------------------------------------
with tab2:
    st.subheader("Dashboard Gerencial")
    st.write("Gráficos e indicadores gerenciais entrarão aqui.")
    # Exemplo: st.bar_chart(df_filtrado['Curva ABC'].value_counts())

# ------------------------------------------
# ABA 3: ITENS BLOQUEADOS (COM OPÇÃO DE EXPORTAR)
# ------------------------------------------
with tab3:
    st.subheader("Detalhamento dos Itens Bloqueados")
    
    # Aqui você carrega ou filtra o dataframe dos itens bloqueados. 
    # Vou simular o seu dataframe da imagem para o exemplo:
    dados_bloqueados_exemplo = {
        "SKU": ["047950", "148282", "248315", "348508"],
        "Curva": ["A", "A", "A", "A"],
        "Esperado (Planilha)": ["PR,PP,PK,LN", "", "PR,PP,PK,LN", "PR,PP,PK,LN"],
        "Encontrado no SAP": ["PP,PR", "", "PR,PK", "PP,PK"]
    }
    df_bloqueados = pd.DataFrame(dados_bloqueados_exemplo)
    
    # Mostrar o dataframe na tela
    st.dataframe(df_bloqueados, use_container_width=True)
    
    # === BOTÃO DE EXPORTAÇÃO AQUI ===
    # Usa a função nativa em Excel que resolve o problema de vírgulas e colunas juntas
    excel_bloqueados = converter_para_excel(df_bloqueados)
    st.download_button(
        label="📥 Exportar Itens Bloqueados para Excel",
        data=excel_bloqueados,
        file_name="Itens_Bloqueados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
