import streamlit as st
import pandas as pd
import io

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Planejamento de Inventário",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# FUNÇÕES DE APOIO
# ==========================================
@st.cache_data
def carregar_dados(arquivo_enviado):
    # Lê os dados da planilha que o usuário enviou pulando as 2 linhas de cabeçalho irrelevantes
    df = pd.read_excel(arquivo_enviado, sheet_name="PLANEJAMENTO", skiprows=2)
    
    # Limpa espaços extras no nome das colunas para evitar erros
    df.columns = df.columns.str.strip()
    
    # Garante que VALOR TOTAL é número
    if 'VALOR TOTAL' in df.columns:
        df['VALOR TOTAL'] = pd.to_numeric(df['VALOR TOTAL'], errors='coerce').fillna(0)
    
    return df

def converter_para_excel(df):
    """
    Converte um DataFrame do Pandas para Excel nativo (.xlsx) na memória.
    Isso evita que o Excel junte as colunas na hora de baixar.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Exportação')
    return output.getvalue()


# ==========================================
# BARRA LATERAL (SIDEBAR) E UPLOAD
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: red;'>📦 GESTÃO DE ESTOQUE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 1. UPLOAD DE ARQUIVO (Resolve o erro na nuvem)
st.sidebar.markdown("### 📂 Upload da Planilha")
arquivo_upado = st.sidebar.file_uploader("Envie o Excel de planejamento (.xlsx)", type=["xlsx"])

# Se o usuário ainda não enviou a planilha, o app avisa e para aqui.
if arquivo_upado is None:
    st.title("ceva 🔺 Sistema de Planejamento de Inventário Cíclico")
    st.info("👋 **Bem-vindo!** Por favor, faça o upload da sua planilha de planejamento (Excel) no menu lateral esquerdo para visualizar os dados.")
    st.stop()

# ==========================================
# CARREGAMENTO DOS DADOS (Após Upload)
# ==========================================
try:
    df_base = carregar_dados(arquivo_upado)
except Exception as e:
    st.error(f"Erro ao ler a planilha. Verifique se é o arquivo correto. Detalhe técnico: {e}")
    st.stop()

# ==========================================
# CONTINUAÇÃO DA BARRA LATERAL (FILTROS)
# ==========================================
st.sidebar.markdown("---")

# 2. FILTRO DE VALOR PLANEJADO
st.sidebar.markdown("### 💰 Filtro de Valor Planejado")
if 'VALOR TOTAL' in df_base.columns:
    max_valor = float(df_base['VALOR TOTAL'].max())
    if pd.isna(max_valor) or max_valor <= 0: 
        max_valor = 100.0 # Valor de segurança
    
    valor_min, valor_max = st.sidebar.slider(
        "Intervalo (R$):",
        min_value=0.0,
        max_value=max_valor,
        value=(0.0, max_valor),
        step=50.0,
        format="R$ %.2f"
    )
else:
    st.sidebar.warning("A coluna 'VALOR TOTAL' não foi encontrada.")
    valor_min, valor_max = 0, 999999

st.sidebar.markdown("---")

# 3. FILTROS DA CURVA ABC
st.sidebar.markdown("### ⚙️ Filtros da Curva ABC")
qtd_a = st.sidebar.number_input("Qtd. SKUs Curva A", min_value=0, value=7)
qtd_b = st.sidebar.number_input("Qtd. SKUs Curva B", min_value=0, value=2)
qtd_c = st.sidebar.number_input("Qtd. SKUs Curva C", min_value=0, value=2)

st.sidebar.markdown("**Filtrar Curva A por ciclo:**")
ciclo = st.sidebar.radio("Ciclo", ["Todas", "1ª contagem", "2ª contagem", "3ª contagem"], label_visibility="collapsed")

# ==========================================
# LÓGICA DE FILTRAGEM
# ==========================================
# Filtra pelo valor selecionado no slider da coluna S
df_filtrado = df_base[(df_base['VALOR TOTAL'] >= valor_min) & (df_base['VALOR TOTAL'] <= valor_max)]

# Filtra pelas quantidades de curvas
df_a = df_filtrado[df_filtrado['Curva ABC'] == 'A'].head(qtd_a)
df_b = df_filtrado[df_filtrado['Curva ABC'] == 'B'].head(qtd_b)
df_c = df_filtrado[df_filtrado['Curva ABC'] == 'C'].head(qtd_c)
df_lote = pd.concat([df_a, df_b, df_c])

# ==========================================
# CORPO PRINCIPAL DO APLICATIVO
# ==========================================
st.title("ceva 🔺 Sistema de Planejamento de Inventário Cíclico")

tab1, tab2, tab3 = st.tabs(["📋 Planejamento Diário (Lote)", "📊 Dashboard Gerencial", "🔒 Detalhamento dos Itens Bloqueados"])

# --- ABA 1: PLANEJAMENTO DIÁRIO ---
with tab1:
    col1, col2, col3 = st.columns(3)
    skus_selecionados = len(df_lote)
    total_locacoes = df_lote['TOTAL POSIÇÕES'].sum() if 'TOTAL POSIÇÕES' in df_lote.columns else 0
    
    col1.metric("SKUs Selecionados", skus_selecionados)
    col2.metric("Total de Locações", int(total_locacoes))
    col3.metric("Meta Operacional", "150 a 200")
    
    if 150 <= total_locacoes <= 200:
        st.success("✅ **Sucesso:** O lote selecionado está DENTRO da média de locações planejada!")
    elif total_locacoes > 200:
        st.error("⚠️ **Atenção:** O lote selecionado está ACIMA da média de locações planejada!")
    else:
        st.warning("⚠️ **Atenção:** O lote selecionado está ABAIXO da média de locações planejada!")
        
    st.dataframe(df_lote, use_container_width=True)
    
    # Botão para exportar o lote em formato Excel
    if not df_lote.empty:
        st.download_button(
            label="📥 Exportar Lote para Excel", 
            data=converter_para_excel(df_lote), 
            file_name="Lote_Planejamento.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- ABA 2: DASHBOARD GERENCIAL ---
with tab2:
    st.subheader("Dashboard Gerencial")
    st.write("Em construção... Aqui entrarão os gráficos.")

# --- ABA 3: ITENS BLOQUEADOS ---
with tab3:
    st.subheader("Detalhamento dos Itens Bloqueados")
    
    # Criando o dataframe simulando a imagem dos itens bloqueados que você mandou
    df_bloqueados = pd.DataFrame({
        "SKU": ["047950", "148282", "248315", "348508", "48664", "49252"],
        "Curva": ["A", "A", "A", "A", "A", "A"],
        "Esperado (Planilha)": ["PR,PP,PK,LN", "", "PR,PP,PK,LN", "PR,PP,PK,LN", "PR,PP,PK,LN", "PR,PP,PK,LN"],
        "Encontrado no SAP": ["PP,PR", "", "PR,PK", "PP,PK", "", "PR"]
    })
    
    st.dataframe(df_bloqueados, use_container_width=True)
    
    # Botão para exportar os itens bloqueados em formato Excel
    st.download_button(
        label="📥 Exportar Itens Bloqueados para Excel", 
        data=converter_para_excel(df_bloqueados), 
        file_name="Itens_Bloqueados.xlsx", 
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
