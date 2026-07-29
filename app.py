# --- INÍCIO: FILTRO DE VALOR PLANEJADO ---
st.sidebar.markdown("### 💰 Filtro de Valor Planejado")

# Certifique-se de que a coluna está no formato numérico (evita erros caso o pandas leia como texto)
df['VALOR TOTAL'] = pd.to_numeric(df['VALOR TOTAL'], errors='coerce').fillna(0)

# Pega o valor máximo encontrado na coluna S ("VALOR TOTAL") para definir o teto do slider
max_valor = float(df['VALOR TOTAL'].max())

# Cria o slider com intervalo (de 0 até o máximo)
valor_min, valor_max = st.sidebar.slider(
    "Intervalo de Valor Planejado:",
    min_value=0.0,
    max_value=max_valor,
    value=(0.0, max_valor),
    step=500.0, # Você pode ajustar os "pulos" do slider aqui
    format="R$ %.2f"
)
st.sidebar.markdown("---") # Linha divisória para separar do Filtro Curva ABC
# --- FIM: FILTRO DE VALOR PLANEJADO ---

# Seu código original continua aqui para baixo...
st.sidebar.markdown("### ⚙️ Filtros da Curva ABC")
