import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import pytz

# Configuração da página
st.set_page_config(
    page_title="Emergências Médicas Pirassununga",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Carrega o CSS customizado
def load_css():
    with open("static/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Dados dos hospitais
hospitals = [
    {
        "name": "Santa Casa de Misericórdia de Pirassununga",
        "location": [-21.9964289, -47.4222628],
        "address": "Av. Newton Prado, 1883 - Centro",
        "cep": "13631-045",
        "phone": "(19) 3565-8100",
        "hours": "24 horas",
        "emergency": True,
        "tipo": "publico",
        "open24h": True,
        "especialidades": ["Emergência", "Cirurgia", "Maternidade"]
    },
    {
        "name": "Hospital Unimed Pirassununga",
        "location": [-22.01030255, -47.42363229721573],
        "address": "R. Joaquim Procópio de Araújo, 3178 - Centro",
        "cep": "13631-020",
        "phone": "(19) 3565-8700",
        "hours": "24 horas",
        "emergency": True,
        "tipo": "privado",
        "open24h": True,
        "especialidades": ["Emergência", "Cirurgia", "Clínica Médica"]
    },
    {
        "name": "CEM - Centro de Especialidades Médicas",
        "location": [-22.012212172100142, -47.43061244487763],
        "address": "Av. Antônio Joaquim Mendes, 1001 - Jardim Europa",
        "cep": "13631-110",
        "phone": "(19) 3563-5050",
        "hours": "07:00 às 19:00",
        "emergency": False,
        "tipo": "publico",
        "open24h": False,
        "especialidades": ["Consultas", "Exames"]
    }
]

def is_hospital_open(hospital):
    sp_timezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(sp_timezone)
    hour = now.hour
    day = now.weekday()  # 0-6 (Segunda-Domingo)
    
    if hospital["open24h"]:
        return True
    
    # Para o CEM: aberto de segunda a sexta, das 7h às 19h
    if not hospital["open24h"] and (day >= 5):  # Sábado e Domingo
        return False
    return 7 <= hour < 19

def create_map(hospitals_to_show, center_location=None):
    if center_location:
        m = folium.Map(location=center_location, zoom_start=14, min_zoom=13, max_zoom=16)
    else:
        m = folium.Map(location=[-21.997, -47.425], zoom_start=14, min_zoom=13, max_zoom=16)
    
    for hospital in hospitals_to_show:
        status = "Aberto Agora" if is_hospital_open(hospital) else "Fechado"
        color = "green" if is_hospital_open(hospital) else "red"
        
        popup_html = f"""
        <div class="popup-content">
            <h3>{hospital['name']}</h3>
            <p><span class="status-{color}" aria-label="{status}">{status}</span></p>
            <p><strong>Telefone:</strong> {hospital['phone']}</p>
            <p><strong>Horário:</strong> {hospital['hours']}</p>
        </div>
        """
        
        folium.Marker(
            hospital["location"],
            popup=popup_html,
            icon=folium.Icon(color=color, icon="info-sign"),
            alt=f"{hospital['name']} - {status}"
        ).add_to(m)
    
    return m

def main():
    # Carregar CSS
    load_css()
    
    # Título e subtítulo
    st.title("Emergências Médicas Pirassununga")
    st.markdown("<p class='subtitle'>Encontre hospitais abertos agora</p>", unsafe_allow_html=True)
    
    # Filtros
    with st.expander("Filtrar Hospitais", expanded=False):
        tipo_atendimento = st.selectbox(
            "Selecione o tipo de atendimento",
            ["todos", "publico", "privado"],
            format_func=lambda x: "Todos os Hospitais" if x == "todos" else 
                               "Saúde Pública" if x == "publico" else "Hospitais Privados"
        )
    
    # Filtrar hospitais baseado na seleção e status de abertura
    filtered_hospitals = [
        h for h in hospitals 
        if (tipo_atendimento == "todos" or h["tipo"] == tipo_atendimento) 
        and is_hospital_open(h)
    ]
    
    # Criar e exibir o mapa
    map_data = create_map(filtered_hospitals)
    st_folium(map_data, width=800, height=600)
    
    # Barra recolhível para informações dos hospitais
    with st.expander("Ver Informações dos Hospitais", expanded=False):
        for hospital in filtered_hospitals:
            status = "Aberto Agora" if is_hospital_open(hospital) else "Fechado"
            status_class = "status-open" if is_hospital_open(hospital) else "status-closed"
            
            st.markdown(f"""
            <div style="margin-bottom: 20px; padding: 10px; border: 1px solid #444; border-radius: 5px;">
                <h3>{hospital['name']}</h3>
                <p class="{status_class}" aria-label="{status}">{status}</p>
                <p><strong>Endereço:</strong> {hospital['address']}</p>
                <p><strong>CEP:</strong> {hospital['cep']}</p>
                <p><strong>Telefone:</strong> {hospital['phone']}</p>
                <p><strong>Horário:</strong> {hospital['hours']}</p>
                <p><strong>Tipo:</strong> {'Público' if hospital['tipo'] == 'publico' else 'Privado'}</p>
                <p><strong>Especialidades:</strong></p>
                <ul>
                    {''.join([f'<li>{esp}</li>' for esp in hospital['especialidades']])}
                </ul>
                <button onclick="window.open('https://www.google.com/maps/dir/?api=1&destination={hospital['location'][0]},{hospital['location'][1]}', '_blank')">
                    Como Chegar
                </button>
            </div>
            """, unsafe_allow_html=True)
    
    # Formulário para calcular rotas
    with st.expander("Calcular Rota", expanded=False):
        endereco_usuario = st.text_input("Digite seu endereço:")
        if endereco_usuario:
            st.markdown(f"""
            <a href="https://www.google.com/maps/dir/?api=1&origin={endereco_usuario}&destination={filtered_hospitals[0]['location'][0]},{filtered_hospitals[0]['location'][1]}" 
               target="_blank" class="direction-button">
                Rastrear Rota
            </a>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()