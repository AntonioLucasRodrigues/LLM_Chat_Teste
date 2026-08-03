import streamlit as st
import ollama

# 1. Page Config using Material Icons
st.set_page_config(
    page_title="EcoLex - Compliance Ambiental",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to build a sleek corporate green dashboard
st.markdown("""
    <style>
    /* Dark Green Sidebar Styling */
    div[data-testid="stSidebar"] { 
        background-color: #0d2818; 
        color: #ffffff; 
    }
    div[data-testid="stSidebar"] button {
        text-align: left !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    /* Status Badge Styling */
    .status-badge {
        background-color: #e8f5e9;
        color: #1b5e20;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Left Sidebar Navigation
with st.sidebar:
    st.title("EcoLex")
    st.caption("Polo Industrial de Manaus")
    
    st.markdown("---")
    
    # Navigation Buttons with Native Material Icons
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
    st.info(
        "Agente de IA especialista em legislação ambiental e licenciamento "
        "para empresas do Polo Industrial de Manaus."
    )
    st.caption("v1.0.0 (offline)")

# 3. Main Dashboard Layout
col_chat, col_panel = st.columns([3, 1.2], gap="medium")

# --- CENTRAL CHAT COLUMN ---
with col_chat:
    # Header with Material Symbol
    st.markdown("### :material/nature_people: Assistente Ambiental")
    st.markdown('<span class="status-badge">:material/wifi_off: Sistema Operando Offline</span>', unsafe_allow_html=True)
    st.markdown("---")

    # Initialize Message History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o seu **Assistente Ambiental**.\n\nComo posso ajudar sua empresa hoje? Faça perguntas sobre normas, licenciamento, obrigações ambientais, prazos e documentos necessários!",
                "sources": []
            }
        ]

    # Render Chat Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption(":material/menu_book: **Fontes Utilizadas:** " + " | ".join(msg["sources"]))

    # User Input Field
    if prompt := st.chat_input("Digite sua pergunta sobre compliance ambiental..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Response Generation
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            system_instruction = {
                "role": "system",
                "content": (
                    "Você é o EcoLex, um agente especialista em legislação ambiental do Polo Industrial de Manaus (PIM). "
                    "Responda com clareza e precisão técnica, citando artigos de lei estaduais (IPAAM) e federais (CONAMA, PNMA) quando relevante."
                )
            }
            
            formatted_messages = [system_instruction] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            for chunk in ollama.chat(model='llama3', messages=formatted_messages, stream=True):
                full_response += chunk['message']['content']
                placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            sources = ["Resolução CONAMA 237/1997", "Resolução IPAAM 007/2015"]
            st.caption(":material/menu_book: **Fontes Utilizadas:** " + " | ".join(sources))

            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response, 
                "sources": sources
            })

# --- RIGHT SIDEBAR / QUICK ACCESS PANEL ---
with col_panel:
    st.markdown("#### :material/balance: Fontes e Legislação")
    
    st.markdown("""
    * :material/description: **Constituição Federal 1988**  
      *Art. 225*
    * :material/description: **Lei nº 6.938/1981**  
      *Política Nacional do Meio Ambiente*
    * :material/description: **Resolução CONAMA 237/1997**  
      *Licenciamento ambiental*
    * :material/description: **Lei nº 12.651/2012**  
      *Código Florestal*
    * :material/description: **Resolução IPAAM 007/2015**  
      *Procedimentos de licenciamento*
    """)
    
    st.markdown("---")
    st.markdown("#### :material/bolt: Ações Rápidas")
    
    st.button("Verificar obrigações", icon=":material/fact_check:", use_container_width=True)
    st.button("Checklist de compliance", icon=":material/checklist:", use_container_width=True)
    st.button("Consultar condicionantes", icon=":material/find_in_page:", use_container_width=True)
    st.button("Simular prazos", icon=":material/event_repeat:", use_container_width=True)
    st.button("Gerar relatório preliminar", icon=":material/picture_as_pdf:", use_container_width=True)

    st.markdown("---")
    st.markdown("#### :material/apartment: Resumo da Empresa")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="Licenças Ativas", value="3")
    with col_m2:
        st.metric(label="Pendências", value="2")
        
    st.error(":material/warning: **Próximo Vencimento:** 15/06/2026")