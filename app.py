import streamlit as st
import ollama

# 1. Configuração da Página
st.set_page_config(
    page_title="EcoLex - Compliance Ambiental",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Gerenciamento de Estado para o Tema (Claro/Escuro)
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# 3. Definição de Cores Dinâmicas via CSS
if st.session_state.theme == "light":
    bg_color = "#f4f7f6"
    card_bg = "#ffffff"
    text_color = "#333333"
    border_color = "#e0e0e0"
    btn_icon = ":material/dark_mode:"
else:
    bg_color = "#1e1e1e"
    card_bg = "#2d2d2d"
    text_color = "#ffffff"
    border_color = "#444444"
    btn_icon = ":material/light_mode:"

# Injeção do CSS Personalizado
st.markdown(f"""
    <style>
    /* Fundo da tela principal */
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    
    /* Barra Lateral Verde Escura */
    div[data-testid="stSidebar"] {{ background-color: #0d2818; color: white; }}
    
    /* Cards da coluna direita */
    .custom-card {{
        background-color: {card_bg};
        padding: 20px;
        border-radius: 10px;
        border: 1px solid {border_color};
        margin-bottom: 20px;
        color: {text_color};
    }}
    
    /* Badges de Status no Topo */
    .top-badge {{
        background-color: #e8f5e9;
        color: #1b5e20;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #c8e6c9;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. Barra Lateral (Esquerda)
with st.sidebar:
    st.markdown("## :material/eco: EcoLex")
    st.caption("Polo Industrial de Manaus")
    st.markdown("---")
    
    st.button("Novo Chat", icon=":material/add:", use_container_width=True)
    st.button("Histórico", icon=":material/history:", use_container_width=True)
    st.button("Legislação", icon=":material/gavel:", use_container_width=True)
    st.button("Guias e procedimentos", icon=":material/menu_book:", use_container_width=True)
    st.button("Licenciamento", icon=":material/verified:", use_container_width=True)
    st.button("Atualizações normativas", icon=":material/notifications:", use_container_width=True)
    st.button("Painel da empresa", icon=":material/dashboard:", use_container_width=True)
    st.button("Configurações", icon=":material/settings:", use_container_width=True)
    
    st.markdown("---")
    st.subheader("Sobre o Agente")
    st.info("Agente de IA especialista em legislação ambiental e licenciamento para empresas do Polo Industrial de Manaus.")

# 5. Layout Principal (Cabeçalho Superior)
header_left, header_right = st.columns([3, 1.5])
with header_left:
    st.markdown("### :material/eco: Assistente ambiental")
    st.caption("Agente de IA para Compliance Ambiental")
with header_right:
    # Simulando a barra de ferramentas superior da sua imagem
    col_badge, col_theme, col_user = st.columns([1.5, 1, 1.5])
    with col_badge:
        st.markdown('<div class="top-badge">:material/wifi_off: Offline</div>', unsafe_allow_html=True)
    with col_theme:
        st.button(btn_icon, on_click=toggle_theme, help="Alternar tema")
    with col_user:
        st.markdown("**Usuário** :material/expand_more:")

st.markdown("---")

# 6. Grid Principal (Chat e Painel)
col_chat, col_panel = st.columns([3, 1.2], gap="large")

# --- COLUNA DO CHAT ---
with col_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o seu **Assistente Ambiental**.\n\nComo posso ajudar sua empresa hoje? Faça perguntas sobre normas, licenciamento, obrigações ambientais, prazos e documentos necessários!"
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua pergunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            system_instruction = {"role": "system", "content": "Você é o EcoLex, especialista ambiental."}
            formatted_messages = [system_instruction] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

            for chunk in ollama.chat(model='llama3', messages=formatted_messages, stream=True):
                full_response += chunk['message']['content']
                placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            st.caption(":material/menu_book: **Fontes Utilizadas:** Resolução CONAMA 237/1997 | Resolução IPAAM 007/2015")
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- COLUNA DIREITA (CARDS) ---
with col_panel:
    # Card 1: Fontes
    st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("#### Fontes e Legislação")
    st.markdown("""
    * :material/description: **CF 1988** - Art. 225
    * :material/description: **Lei nº 6.938/1981** - PNMA
    * :material/description: **Res. CONAMA 237/1997**
    * :material/description: **Res. IPAAM 007/2015**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 2: Ações
    st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("#### Ações rápidas")
    st.button("Verificar obrigações", icon=":material/check_box:", use_container_width=True)
    st.button("Checklist de compliance", icon=":material/check_box:", use_container_width=True)
    st.button("Consultar condicionantes", icon=":material/check_box:", use_container_width=True)
    st.button("Simular prazos", icon=":material/check_box:", use_container_width=True)
    st.button("Gerar relatório", icon=":material/check_box:", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 3: Resumo
    st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("#### Resumo da empresa")
    st.metric(label="Licenças ativas", value="3")
    st.metric(label="Condicionantes pendentes", value="2")
    st.error(":material/schedule: **Próximos vencimentos:** 15/06/2026")
    st.markdown('</div>', unsafe_allow_html=True)