import streamlit as st
import pandas as pd
import plotly.express as px

# Ícone da aba do navegador
st.set_page_config(page_title="Inventário Cíclico | CEVA", page_icon="🔺", layout="wide")

# --- INJEÇÃO DE CSS PREMIUM ---
st.markdown("""
    <style>
        /* 1. Tipografia Global Limpa */
        html, body, [class*="css"]  {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }

        /* 2. Fundo Dinâmico de Grid (Padrão de Dashboard de Logística) - Zero bloqueio de rede */
        .stApp {
            background-color: #f4f6f9 !important;
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px) !important;
            background-size: 25px 25px !important;
        }
        
        /* Remove a faixa branca central padrão do Streamlit */
        .block-container, [data-testid="stAppViewBlockContainer"] {
            background-color: transparent !important;
        }

        /* Títulos principais da TELA CENTRAL em Azul CEVA */
        .main h1, .main h2, .main h3, .main p, .main span {
            color: #001439 !important;
        }
        .main h1, .main h2, .main h3 {
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }

        /* 3. Menu Lateral Azul Marinho com LETRAS VERMELHAS FORTE */
        [data-testid="stSidebar"] {
            background-color: #001439 !important;
            border-right: 1px solid rgba(0,0,0,0.1);
        }
        
        /* Força todos os textos da barra lateral para VERMELHO */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
            color: #e3000f !important; 
        }

        /* Campos numéricos de input - Fundo branco para leitura */
        [data-testid="stSidebar"] div[data-baseweb="input"] > div {
            background-color: #ffffff !important;
            border-radius: 6px !important;
            border: 1px solid rgba(227, 0, 15, 0.3) !important;
        }
        /* Texto que o usuário digita fica em azul escuro */
        [data-testid="stSidebar"] input {
            color: #001439 !important;
            -webkit-text-fill-color: #001439 !important;
            font-weight: 600 !important;
        }

        /* 4. CAIXA DE UPLOAD (Arraste e Solte no Menu Lateral) */
        [data-testid="stFileUploadDropzone"] {
            background-color: #ffffff !important;
            border: 2px dashed #e3000f !important; 
            border-radius: 8px !important;
        }
        /* Textos de Upload em Vermelho */
        [data-testid="stFileUploadDropzone"] div, 
        [data-testid="stFileUploadDropzone"] span, 
        [data-testid="stFileUploadDropzone"] small,
        [data-testid="stFileUploadDropzone"] p {
            color: #e3000f !important;
        }
        /* Botão interno de procurar arquivo */
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

        /* 5. Cartões de Métricas (Tela Principal) */
        [data-testid="metric-container"] {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 15px 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
        }
        [data-testid="metric-container"]:hover {
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }
        [data-testid="metric-container"] label {
            color: #555555 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        [data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #001439 !important;
            font-weight: 800 !important;
        }

        /* 6. Botão Primário Exportar */
        div.stButton > button {
            background-color: #e3000f !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 4px 6px rgba(227, 0, 15, 0.2);
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            background-color: #b3000b !important;
            box-shadow: 0 6px 10px rgba(227, 0, 15, 0.3);
            transform: translateY(-1px);
        }
        
        /* 7. ANIMAÇÃO DA EMPILHADEIRA */
        @keyframes drive {
            0% { transform: translateX(-50px); }
            100% { transform: translateX(100vw); }
        }
        .forklift-animation {
            animation: drive 15s linear infinite;
            display: inline-block;
        }

        /* Limpeza do visual do Streamlit */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# 1. SIDEBAR / MENU LATERAL COM ÍCONE DE ESTOQUE (Sem fundo branco agora)
st.sidebar.markdown("""
    <div style="background-color: transparent; border: 1.5px solid rgba(227, 0, 15, 0.3); padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 25px; margin-top: -15px; display: flex; flex-direction: column; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="55" height="55" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 8px;">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
            <path d="M16.5 14.5 12 17l-4.5-2.5" stroke="#e3000f" stroke-width="2.5"></path>
            <path d="M16.5 9.5 12 12 7.5 9.5" stroke="#e3000f" stroke-width="2.5"></path>
        </svg>
        <span style="color: #ffffff !important; font-weight: 800; font-size: 0.90em; letter-spacing: 1px;">GESTÃO DE ESTOQUE</span>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.header("⚙️ Configurações do Lote")

st.sidebar.subheader("Meta de SKUs por Curva")
qtd_a = st.sidebar.number_input("Qtd. SKUs Curva A", min_value=0, value=10, step=1)

# FILTRO DA CURVA A
filtro_curva_a = st.sidebar.radio(
    "Filtrar Curva A por ciclo de contagem:",
    options=["Todas", "1ª contagem", "2ª contagem", "3ª contagem"],
    help="Define de qual coluna da planilha o sistema deve puxar os itens pendentes da Curva A."
)

qtd_b = st.sidebar.number_input("Qtd. SKUs Curva B", min_value=0, value=5, step=1)
qtd_c = st.sidebar.number_input("Qtd. SKUs Curva C", min_value=0, value=2, step=1)

st.sidebar.subheader("Capacidade de Locações")
min_loc = st.sidebar.number_input("Mínimo de Locações", min_value=0, value=150, step=10)
max_loc = st.sidebar.number_input("Máximo de Locações", min_value=0, value=200, step=10)

# UPLOAD DE ARQUIVOS
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Upload dos Arquivos")
file_plan = st.sidebar.file_uploader("Planilha de Planejamento (.xlsx)", type=["xlsx"])
file_sap = st.sidebar.file_uploader("Relatório SAP (.xlsx)", type=["xlsx"])

# TÍTULO DA PÁGINA PRINCIPAL COM A EMPILHADEIRA ANIMADA EM CIMA
st.markdown("""
    <div style="width: 100%; overflow: hidden; height: 35px; margin-top: -30px; margin-bottom: 5px;">
        <div class="forklift-animation">
            <svg width="50" height="30" viewBox="0 0 40 30" xmlns="http://www.w3.org/2000/svg">
                <!-- Corpo da empilhadeira vermelho -->
                <rect x="5" y="10" width="15" height="15" rx="2" fill="#e3000f"/>
                <!-- Cabine azul escura -->
                <rect x="8" y="2" width="10" height="10" rx="1" fill="none" stroke="#001439" stroke-width="2.5"/>
                <!-- Garfos e torre azuis escuros -->
                <path d="M 20 25 L 32 25 L 32 15 L 32 8" fill="none" stroke="#001439" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="20" y1="10" x2="20" y2="25" stroke="#001439" stroke-width="2.5"/>
                <!-- Caixa de papelão -->
                <rect x="23" y="15" width="8" height="9" fill="#d2a679" stroke="#8b5a2b" stroke-width="1"/>
                <!-- Detalhe da caixa -->
                <line x1="23" y1="19" x2="31" y2="19" stroke="#8b5a2b" stroke-width="1" stroke-dasharray="2,1"/>
                <!-- Rodas traseira e dianteira azuis escuros -->
                <circle cx="9" cy="26" r="3" fill="#001439"/>
                <circle cx="18" cy="26" r="3" fill="#001439"/>
            </svg>
        </div>
    </div>
    
    <div style="background-color: transparent; display: flex; align-items: center; margin-bottom: 30px;">
        <div style="display: flex; align-items: center; justify-content: center; margin-right: 15px;">
            <span style="font-size: 2.2em; font-weight: 900; color: #001439; margin-right: 5px; letter-spacing: -1.5px;">ceva</span>
            <span style="color: #e3000f; font-size: 1.9em;">▲</span>
        </div>
        <h1 style="color: #001439 !important; margin: 0; font-size: 2.1em; padding-top: 5px; border-left: 2px solid rgba(0,20,57,0.2); padding-left: 15px;">Sistema de Planejamento de Inventário Cíclico</h1>
    </div>
""", unsafe_allow_html=True)

if file_plan is None or file_sap is None:
    st.info("👈 Por favor, faça o upload das duas planilhas no menu lateral para iniciar a análise.")
else:
    try:
        # CARREGAR E TRATAR PLANILHA DE PLANEJAMENTO
        df_plan_raw = pd.read_excel(file_plan, sheet_name="PLANEJAMENTO")
        df_plan = df_plan_raw.copy()
        
        cabecalhos = df_plan.iloc[1]
        df_plan.columns = [str(c) if pd.notna(c) else f"coluna_{i}" for i, c in enumerate(cabecalhos)]
        
        df_plan = df_plan.iloc[2:].reset_index(drop=True)
        df_plan = df_plan.dropna(subset=['SKU'])

        # CARREGAR E TRATAR RELATÓRIO SAP
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
            if not row['PENDENTE']:
                return "Já Contado"
            elif row['IS_VALID']:
                return "Disponível para Contar"
            else:
                return "Bloqueado (Divergência de Posição)"

        df_plan['STATUS_GERAL'] = df_plan.apply(classificar_status, axis=1)
        df_plan['TOTAL POSIÇÕES'] = pd.to_numeric(df_plan['TOTAL POSIÇÕES'], errors='coerce').fillna(0).astype(int)

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
                if melhor_lote.empty:
                    return melhor_lote
                    
                soma_inicial = melhor_lote['TOTAL POSIÇÕES'].sum()
                if min_l <= soma_inicial <= max_l:
                    return melhor_lote 
                
                menor_distancia = min(abs(soma_inicial - min_l), abs(soma_inicial - max_l))
                
                for _ in range(2000):
                    s_a = df_a.sample(n=min(q_a, len(df_a))) if q_a > 0 and not df_a.empty else pd.DataFrame()
                    s_b = df_b.sample(n=min(q_b, len(df_b))) if q_b > 0 and not df_b.empty else pd.DataFrame()
                    s_c = df_c.sample(n=min(q_c, len(df_c))) if q_c > 0 and not df_c.empty else pd.DataFrame()
                    
                    lote_temp = pd.concat([s_a, s_b, s_c])
                    soma_temp = lote_temp['TOTAL POSIÇÕES'].sum()
                    
                    if min_l <= soma_temp <= max_l:
                        return lote_temp 
                    
                    dist = min(abs(soma_temp - min_l), abs(soma_temp - max_l))
                    if dist < menor_distancia:
                        menor_distancia = dist
                        melhor_lote = lote_temp
                        
                return melhor_lote

            lote_sugerido = otimizar_lote(df_disp_a, df_disp_b, df_disp_c, qtd_a, qtd_b, qtd_c, min_loc, max_loc)
            total_locacoes_lote = lote_sugerido['TOTAL POSIÇÕES'].sum()

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("SKUs Selecionados", len(lote_sugerido))
            col_m2.metric("Total de Locações do Lote", total_locacoes_lote)
            col_m3.metric("Meta de Locações", f"{min_loc} - {max_loc}")
            
            st.markdown("<br>", unsafe_allow_html=True)

            if min_loc <= total_locacoes_lote <= max_loc:
                st.success("✅ O lote selecionado está DENTRO da média de locações planejada!")
            elif total_locacoes_lote < min_loc:
                st.warning("⚠️ Atenção: Mesmo testando milhares de combinações, o total de locações ficou ABAIXO da meta. Tente aumentar a quantidade de SKUs.")
            else:
                st.error("🚨 Atenção: O total de locações EXCEDE a capacidade estipulada.")

            st.markdown("<br>", unsafe_allow_html=True)
            df_display = lote_sugerido[['SKU', 'Curva ABC', 'TOTAL POSIÇÕES', '1ª contagem', '2ª contagem', '3ª contagem', 'LN', 'PC', 'PK', 'PP', 'PR', 'PD']].reset_index(drop=True)
            st.dataframe(df_display, use_container_width=True)

            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False, sep=';').encode('utf-8')

            csv = convert_df(df_display)
            st.download_button(
                label="📥 Exportar Lote Planejado (CSV)",
                data=csv,
                file_name='lote_inventario_planejado.csv',
                mime='text/csv',
            )

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                fig_status = px.histogram(
                    df_plan, 
                    x="Curva ABC", 
                    color="STATUS_GERAL", 
                    title="Status dos SKUs por Curva ABC",
                    barmode="group",
                    color_discrete_map={
                        "Já Contado": "#8a8d91",
                        "Disponível para Contar": "#001439",
                        "Bloqueado (Divergência de Posição)": "#e3000f"
                    }
                )
                fig_status.update_layout(yaxis_title="Quantidade de SKUs")
                st.plotly_chart(fig_status, use_container_width=True)

            with col_g2:
                df_disp_only = df_plan[df_plan['STATUS_GERAL'] == "Disponível para Contar"]
                
                if not df_disp_only.empty:
                    fig_loc = px.pie(
                        df_disp_only, 
                        names="Curva ABC", 
                        values="TOTAL POSIÇÕES", 
                        title="Distribuição de Locações Disponíveis por Curva",
                        color="Curva ABC",
                        color_discrete_map={
                            "A": "#001439",
                            "B": "#e3000f",
                            "C": "#8a8d91"
                        }
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
