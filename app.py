import streamlit as st
import pandas as pd
import plotly.express as px

# Ícone da aba do navegador
st.set_page_config(page_title="Inventário Cíclico | CEVA", page_icon="🔺", layout="wide")

# --- INJEÇÃO DE CSS PREMIUM ---
st.markdown("""
    <style>
        /* Tipografia Global Limpa */
        html, body, [class*="css"]  {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }

        /* Fundo Dinâmico de Grid */
        .stApp {
            background-color: #f4f6f9 !important;
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px) !important;
            background-size: 25px 25px !important;
        }
        
        .block-container, [data-testid="stAppViewBlockContainer"] {
            background-color: transparent !important;
            padding-top: 2rem !important; /* Mais espaço no topo */
        }

        header, [data-testid="stHeader"] {
            background-color: transparent !important;
            background: transparent !important;
        }

        /* Títulos e Textos Principais */
        .main h1, .main h2, .main h3, .main p, .main span {
            color: #001439 !important;
        }
        .main h1, .main h2, .main h3 {
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }

        /* Menu Lateral */
        [data-testid="stSidebar"] {
            background-color: #001439 !important;
            border-right: 1px solid rgba(0,0,0,0.1);
        }
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
            color: #e3000f !important; 
        }

        /* Inputs do Menu Lateral */
        [data-testid="stSidebar"] div[data-baseweb="input"] > div {
            background-color: #ffffff !important;
            border-radius: 6px !important;
            border: 1px solid rgba(227, 0, 15, 0.3) !important;
        }
        [data-testid="stSidebar"] input {
            color: #001439 !important;
            -webkit-text-fill-color: #001439 !important;
            font-weight: 600 !important;
        }

        /* Upload no Menu Lateral */
        [data-testid="stFileUploadDropzone"] {
            background-color: #ffffff !important;
            border: 2px dashed #e3000f !important; 
            border-radius: 8px !important;
        }
        [data-testid="stFileUploadDropzone"] div, 
        [data-testid="stFileUploadDropzone"] span, 
        [data-testid="stFileUploadDropzone"] small,
        [data-testid="stFileUploadDropzone"] p {
            color: #e3000f !important;
        }
        [data-testid="stFileUploadDropzone"] button {
            background-color: #e3000f !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: bold !important;
        }
        [data-testid="stFileUploadDropzone"] button * {
            color: #ffffff !important;
        }
        [data-testid="stFileUploadDropzone"] svg {
            fill: #e3000f !important;
            stroke: #e3000f !important;
        }

        /* Cartões de Métricas */
        [data-testid="metric-container"] {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0,20,57,0.1);
            transition: all 0.2s ease-in-out;
            text-align: center; /* Centraliza as métricas */
        }
        [data-testid="metric-container"]:hover {
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            transform: translateY(-3px);
            border: 1px solid rgba(227, 0, 15, 0.3); /* Destaque vermelho ao passar o mouse */
        }
        [data-testid="metric-container"] label {
            color: #555555 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            justify-content: center;
        }
        [data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #001439 !important;
            font-weight: 900 !important;
            font-size: 2.5rem !important; /* Números maiores e mais visíveis */
        }

        /* Botão Exportar */
        div.stButton > button {
            background-color: #e3000f !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.6rem 1.5rem !important;
            box-shadow: 0 4px 6px rgba(227, 0, 15, 0.2);
            transition: all 0.2s;
            width: 100%; /* Botão largo para destaque */
        }
        div.stButton > button:hover {
            background-color: #b3000b !important;
            box-shadow: 0 6px 10px rgba(227, 0, 15, 0.3);
            transform: translateY(-2px);
        }
        
        /* Animação Multimodal */
        @keyframes drive {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100vw); }
        }
        .transport-animation {
            animation: drive 25s linear infinite;
            display: flex;
            align-items: flex-end;
            gap: 120px;
            width: max-content;
        }

        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.markdown("""
    <div style="background-color: transparent; border: 1.5px solid rgba(227, 0, 15, 0.3); padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 25px; margin-top: -15px; display: flex; flex-direction: column; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 8px;">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
            <path d="M16.5 14.5 12 17l-4.5-2.5" stroke="#e3000f" stroke-width="2.5"></path>
            <path d="M16.5 9.5 12 12 7.5 9.5" stroke="#e3000f" stroke-width="2.5"></path>
        </svg>
        <span style="color: #ffffff !important; font-weight: 800; font-size: 0.85em; letter-spacing: 1px;">GESTÃO DE ESTOQUE</span>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Filtros da Curva ABC")
qtd_a = st.sidebar.number_input("Qtd. SKUs Curva A", min_value=0, value=10, step=1)
filtro_curva_a = st.sidebar.radio(
    "Filtrar Curva A por ciclo:",
    options=["Todas", "1ª contagem", "2ª contagem", "3ª contagem"]
)
qtd_b = st.sidebar.number_input("Qtd. SKUs Curva B", min_value=0, value=5, step=1)
qtd_c = st.sidebar.number_input("Qtd. SKUs Curva C", min_value=0, value=2, step=1)

st.sidebar.markdown("---")
st.sidebar.header("📦 Capacidade Operacional")
min_loc = st.sidebar.number_input("Mínimo de Locações", min_value=0, value=150, step=10)
max_loc = st.sidebar.number_input("Máximo de Locações", min_value=0, value=200, step=10)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Importação de Dados")
file_plan = st.sidebar.file_uploader("1. Planilha de Planejamento", type=["xlsx"])
file_sap = st.sidebar.file_uploader("2. Relatório SAP", type=["xlsx"])


# --- CABEÇALHO PRINCIPAL ---
st.markdown("""
    <div style="width: 100%; overflow: hidden; height: 45px; margin-top: -30px; margin-bottom: 0px;">
        <div class="transport-animation">
            <svg width="60" height="30" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 12px;">
                <path d="M10,20 L45,20 C50,20 55,18 55,15 C55,12 50,15 45,15 L20,15 L10,5 L5,5 L12,15 L5,15 L2,10 L0,10 L2,20 Z" fill="#001439"/>
                <path d="M25,17 L15,28 L22,28 L32,17 Z" fill="#e3000f"/>
            </svg>
            <svg width="60" height="30" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="5" width="20" height="22" rx="2" fill="#001439"/>
                <rect x="12" y="10" width="8" height="6" fill="#f4f6f9"/>
                <rect x="25" y="12" width="25" height="15" rx="2" fill="#e3000f"/>
                <rect x="38" y="4" width="6" height="8" fill="#001439"/>
                <circle cx="12" cy="26" r="4" fill="#e3000f"/>
                <circle cx="22" cy="26" r="4" fill="#e3000f"/>
                <circle cx="35" cy="26" r="3" fill="#001439"/>
                <circle cx="45" cy="26" r="3" fill="#001439"/>
                <polygon points="50,20 50,27 57,27" fill="#001439"/>
            </svg>
            <svg width="60" height="30" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="8" width="38" height="18" rx="2" fill="#e3000f"/>
                <path d="M 42 15 L 48 15 L 53 20 L 53 26 L 42 26 Z" fill="#001439"/>
                <rect x="42" y="10" width="8" height="16" fill="#001439"/>
                <circle cx="10" cy="26" r="3" fill="#001439"/>
                <circle cx="20" cy="26" r="3" fill="#001439"/>
                <circle cx="32" cy="26" r="3" fill="#001439"/>
                <circle cx="48" cy="26" r="3" fill="#e3000f"/>
            </svg>
            <svg width="50" height="30" viewBox="0 0 40 30" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="10" width="15" height="15" rx="2" fill="#e3000f"/>
                <rect x="8" y="2" width="10" height="10" rx="1" fill="none" stroke="#001439" stroke-width="2.5"/>
                <path d="M 20 25 L 32 25 L 32 15 L 32 8" fill="none" stroke="#001439" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="20" y1="10" x2="20" y2="25" stroke="#001439" stroke-width="2.5"/>
                <rect x="23" y="15" width="8" height="9" fill="#d2a679" stroke="#8b5a2b" stroke-width="1"/>
                <line x1="23" y1="19" x2="31" y2="19" stroke="#8b5a2b" stroke-width="1" stroke-dasharray="2,1"/>
                <circle cx="9" cy="26" r="3" fill="#001439"/>
                <circle cx="18" cy="26" r="3" fill="#001439"/>
            </svg>
        </div>
    </div>
    
    <div style="background-color: transparent; display: flex; align-items: center; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: center; margin-right: 15px;">
            <span style="font-size: 2.2em; font-weight: 900; color: #001439; margin-right: 5px; letter-spacing: -1.5px;">ceva</span>
            <span style="color: #e3000f; font-size: 1.9em;">▲</span>
        </div>
        <h1 style="color: #001439 !important; margin: 0; font-size: 2.1em; padding-top: 5px; border-left: 2px solid rgba(0,20,57,0.2); padding-left: 15px;">Sistema de Planejamento de Inventário Cíclico</h1>
    </div>
""", unsafe_allow_html=True)


# --- TELA DE BOAS-VINDAS (Quando não há planilhas) ---
if file_plan is None or file_sap is None:
    st.markdown("""
        <div style="background-color: white; padding: 50px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; border: 1px solid rgba(0,20,57,0.1); margin-top: 20px;">
            <h2 style="color: #001439; font-size: 1.8em; margin-bottom: 10px;">Bem-vindo ao Workspace de Inventário</h2>
            <p style="color: #555555; font-size: 1.1em; margin-bottom: 40px;">Para iniciar a análise automatizada e gerar os lotes, siga os passos abaixo:</p>
            
            <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
                <div style="background: #f8fafc; padding: 25px; border-radius: 10px; width: 300px; border: 2px dashed #cbd5e1;">
                    <div style="font-size: 2.5em; margin-bottom: 10px;">📄</div>
                    <h3 style="color: #e3000f; font-size: 1.3em;">Passo 1</h3>
                    <p style="color: #333333;">Arraste a <b>Planilha de Planejamento</b> para a primeira área no menu lateral.</p>
                </div>
                <div style="background: #f8fafc; padding: 25px; border-radius: 10px; width: 300px; border: 2px dashed #cbd5e1;">
                    <div style="font-size: 2.5em; margin-bottom: 10px;">📊</div>
                    <h3 style="color: #e3000f; font-size: 1.3em;">Passo 2</h3>
                    <p style="color: #333333;">Arraste o <b>Relatório SAP</b> exportado para a segunda área no menu lateral.</p>
                </div>
                <div style="background: #f8fafc; padding: 25px; border-radius: 10px; width: 300px; border: 2px dashed #cbd5e1;">
                    <div style="font-size: 2.5em; margin-bottom: 10px;">⚙️</div>
                    <h3 style="color: #e3000f; font-size: 1.3em;">Passo 3</h3>
                    <p style="color: #333333;">Ajuste as <b>Capacidades e Metas</b> e deixe o sistema calcular o lote ideal.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- LÓGICA PRINCIPAL DO SISTEMA ---
    try:
        df_plan_raw = pd.read_excel(file_plan, sheet_name="PLANEJAMENTO")
        df_plan = df_plan_raw.copy()
        
        cabecalhos = df_plan.iloc[1]
        df_plan.columns = [str(c) if pd.notna(c) else f"coluna_{i}" for i, c in enumerate(cabecalhos)]
        
        df_plan = df_plan.iloc[2:].reset_index(drop=True)
        df_plan = df_plan.dropna(subset=['SKU'])

        df_sap = pd.read_excel(file_sap)
        df_sap['SKU'] = df_sap['Produto'].astype(str).str.strip()
        df_sap['Prefix'] = df_sap['Posição no depósito'].astype(str).str.strip().apply(
            lambda x: x.split('-')[0].upper() if '-' in str(x) else str(x).upper()
        )

        sap_locs = df_sap.groupby('SKU')['Prefix'].apply(lambda x: set(x)).to_dict()

        def verificar_pendencia(row):
            for col in ['1ª contagem', '2ª contagem', '3ª contagem']:
                if 'PENDENTE' in str(row[col]).upper():
                    return True
            return False

        df_plan['PENDENTE'] = df_plan.apply(verificar_pendencia, axis=1)
        loc_cols = ['LN', 'PC', 'PK', 'PP', 'PR', 'PD']

        def validar_locacoes(row):
            sku = str(row['SKU']).strip()
            expected = set()
            for col in loc_cols:
                try:
                    if float(row[col]) > 0:
                        expected.add(col)
                except:
                    pass
            actual = sap_locs.get(sku, set())
            is_valid = (expected == actual) and (len(expected) > 0)
            return is_valid, expected, actual

        val_results = df_plan.apply(validar_locacoes, axis=1)
        df_plan['IS_VALID'] = [r[0] for r in val_results]
        df_plan['EXPECTED'] = [r[1] for r in val_results]
        df_plan['ACTUAL'] = [r[2] for r in val_results]

        def classificar_status(row):
            if not row['PENDENTE']: return "Já Contado"
            elif row['IS_VALID']: return "Disponível para Contar"
            else: return "Bloqueado (Divergência de Posição)"

        df_plan['STATUS_GERAL'] = df_plan.apply(classificar_status, axis=1)
        df_plan['TOTAL POSIÇÕES'] = pd.to_numeric(df_plan['TOTAL POSIÇÕES'], errors='coerce').fillna(0).astype(int)

        st.divider() # Adiciona uma linha sutil para separar o cabeçalho do conteúdo
        
        tab1, tab2 = st.tabs(["📋 Planejamento Diário (Lote)", "📊 Dashboard Gerencial"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            
            mask_a = (df_plan['STATUS_GERAL'] == "Disponível para Contar") & (df_plan['Curva ABC'] == 'A')
            if filtro_curva_a != "Todas":
                mask_a = mask_a & df_plan[filtro_curva_a].astype(str).str.upper().str.contains('PENDENTE')
            
            df_disp_a = df_plan[mask_a]
            df_disp_b = df_plan[(df_plan['STATUS_GERAL'] == "Disponível para Contar") & (df_plan['Curva ABC'] == 'B')]
            df_disp_c = df_plan[(df_plan['STATUS_GERAL'] == "Disponível para Contar") & (df_plan['Curva ABC'] == 'C')]

            def otimizar_lote(df_a, df_b, df_c, q_a, q_b, q_c, min_l, max_l):
                melhor_lote = pd.concat([df_a.head(q_a), df_b.head(q_b), df_c.head(q_c)])
                if melhor_lote.empty: return melhor_lote
                soma_inicial = melhor_lote['TOTAL POSIÇÕES'].sum()
                if min_l <= soma_inicial <= max_l: return melhor_lote 
                menor_distancia = min(abs(soma_inicial - min_l), abs(soma_inicial - max_l))
                for _ in range(2000):
                    s_a = df_a.sample(n=min(q_a, len(df_a))) if q_a > 0 and not df_a.empty else pd.DataFrame()
                    s_b = df_b.sample(n=min(q_b, len(df_b))) if q_b > 0 and not df_b.empty else pd.DataFrame()
                    s_c = df_c.sample(n=min(q_c, len(df_c))) if q_c > 0 and not df_c.empty else pd.DataFrame()
                    lote_temp = pd.concat([s_a, s_b, s_c])
                    soma_temp = lote_temp['TOTAL POSIÇÕES'].sum()
                    if min_l <= soma_temp <= max_l: return lote_temp 
                    dist = min(abs(soma_temp - min_l), abs(soma_temp - max_l))
                    if dist < menor_distancia:
                        menor_distancia = dist
                        melhor_lote = lote_temp
                return melhor_lote

            lote_sugerido = otimizar_lote(df_disp_a, df_disp_b, df_disp_c, qtd_a, qtd_b, qtd_c, min_loc, max_loc)
            total_locacoes_lote = lote_sugerido['TOTAL POSIÇÕES'].sum()

            # Métricas Centralizadas com Design de Cartão
            col_blank1, col_m1, col_m2, col_m3, col_blank2 = st.columns([1, 2, 2, 2, 1])
            with col_m1: st.metric("SKUs Selecionados", len(lote_sugerido))
            with col_m2: st.metric("Total de Locações", total_locacoes_lote)
            with col_m3: st.metric("Meta Operacional", f"{min_loc} a {max_loc}")
            
            st.markdown("<br>", unsafe_allow_html=True)

            if min_loc <= total_locacoes_lote <= max_loc:
                st.success("✅ **Sucesso:** O lote selecionado está DENTRO da média de locações planejada!")
            elif total_locacoes_lote < min_loc:
                st.warning("⚠️ **Atenção:** O total de locações ficou ABAIXO da meta. Tente aumentar a quantidade de SKUs no menu lateral.")
            else:
                st.error("🚨 **Atenção:** O total de locações EXCEDE a capacidade estipulada.")

            st.markdown("<br>", unsafe_allow_html=True)
            df_display = lote_sugerido[['SKU', 'Curva ABC', 'TOTAL POSIÇÕES', '1ª contagem', '2ª contagem', '3ª contagem', 'LN', 'PC', 'PK', 'PP', 'PR', 'PD']].reset_index(drop=True)
            
            # Container estilizado para a tabela e o botão
            with st.container():
                st.dataframe(df_display, use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # O botão exportar agora fica contido em colunas para não esticar na tela toda
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    @st.cache_data
                    def convert_df(df):
                        return df.to_csv(index=False, sep=';').encode('utf-8')
                    csv = convert_df(df_display)
                    st.download_button(
                        label="📥 EXPORTAR LOTE PARA O EXCEL (CSV)",
                        data=csv,
                        file_name='lote_inventario_planejado.csv',
                        mime='text/csv',
                    )

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                fig_status = px.histogram(
                    df_plan, x="Curva ABC", color="STATUS_GERAL", 
                    title="Status dos SKUs por Curva ABC", barmode="group",
                    color_discrete_map={
                        "Já Contado": "#8a8d91", "Disponível para Contar": "#001439", "Bloqueado (Divergência de Posição)": "#e3000f"
                    }
                )
                fig_status.update_layout(yaxis_title="Quantidade de SKUs")
                st.plotly_chart(fig_status, use_container_width=True)

            with col_g2:
                df_disp_only = df_plan[df_plan['STATUS_GERAL'] == "Disponível para Contar"]
                if not df_disp_only.empty:
                    fig_loc = px.pie(
                        df_disp_only, names="Curva ABC", values="TOTAL POSIÇÕES", 
                        title="Distribuição de Locações Disponíveis por Curva", color="Curva ABC",
                        color_discrete_map={"A": "#001439", "B": "#e3000f", "C": "#8a8d91"}
                    )
                    st.plotly_chart(fig_loc, use_container_width=True)
                else:
                    st.info("Nenhum item disponível para exibir no gráfico de pizza.")

            st.markdown("---")
            st.markdown("### 🔍 Detalhamento dos Itens Bloqueados")
            df_bloq = df_plan[df_plan['STATUS_GERAL'] == "Bloqueado (Divergência de Posição)"][['SKU', 'Curva ABC', 'EXPECTED', 'ACTUAL']].reset_index(drop=True)
            df_bloq.columns = ['SKU', 'Curva', 'Esperado (Planilha)', 'Encontrado no SAP']
            st.dataframe(df_bloq, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os arquivos. Por favor, verifique se as planilhas estão no formato correto. Detalhe do erro: {e}")
