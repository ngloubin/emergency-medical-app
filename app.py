
# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from datetime import datetime
# import pytz
# import os
# import pandas as pd
# import json
# from statistics import mean

# # Configuração da página
# st.set_page_config(
#     page_title="Emergências Médicas Pirassununga",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Inicialização dos arquivos de dados
# def init_data_files():
#     if not os.path.exists('data'):
#         os.makedirs('data')
    
#     # Arquivo de avaliações
#     if not os.path.exists('data/avaliacoes.csv'):
#         pd.DataFrame(columns=['hospital_id', 'estrelas', 'comentario', 'data']).to_csv('data/avaliacoes.csv', index=False)
    
#     # Arquivo de denúncias
#     if not os.path.exists('data/denuncias.csv'):
#         pd.DataFrame(columns=['hospital_id', 'descricao', 'data', 'status']).to_csv('data/denuncias.csv', index=False)

# # Carregar e salvar avaliações
# def load_avaliacoes():
#     return pd.read_csv('data/avaliacoes.csv')

# def save_avaliacao(hospital_id, estrelas, comentario):
#     df = load_avaliacoes()
#     nova_avaliacao = pd.DataFrame([{
#         'hospital_id': hospital_id,
#         'estrelas': estrelas,
#         'comentario': comentario,
#         'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     }])
#     df = pd.concat([df, nova_avaliacao], ignore_index=True)
#     df.to_csv('data/avaliacoes.csv', index=False)

# # Carregar e salvar denúncias
# def load_denuncias():
#     return pd.read_csv('data/denuncias.csv')

# def save_denuncia(hospital_id, descricao):
#     df = load_denuncias()
#     nova_denuncia = pd.DataFrame([{
#         'hospital_id': hospital_id,
#         'descricao': descricao,
#         'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'status': 'Pendente'
#     }])
#     df = pd.concat([df, nova_denuncia], ignore_index=True)
#     df.to_csv('data/denuncias.csv', index=False)

# # Calcular média de estrelas
# def calcular_media_estrelas(hospital_id):
#     df = load_avaliacoes()
#     avaliacoes = df[df['hospital_id'] == hospital_id]['estrelas']
#     if len(avaliacoes) > 0:
#         return round(mean(avaliacoes), 1)
#     return 0

# # Carregar CSS
# def load_css():
#     css_path = os.path.join("static", "style.css")
#     if os.path.exists(css_path):
#         with open(css_path) as f:
#             st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#     else:
#         st.warning("Arquivo CSS não encontrado.")

# # Dados dos hospitais
# hospitals = [
#     {
#         "id": 1,
#         "name": "Santa Casa de Misericórdia de Pirassununga",
#         "location": [-21.9964289, -47.4222628],
#         "address": "Av. Newton Prado, 1883 - Centro",
#         "cep": "13631-045",
#         "phone": "(19) 3565-8100",
#         "hours": "24 horas",
#         "emergency": True,
#         "tipo": "publico",
#         "open24h": True,
#         "especialidades": ["Emergência", "Cirurgia", "Maternidade"]
#     },
#     {
#         "id": 2,
#         "name": "Hospital Unimed Pirassununga",
#         "location": [-22.01030255, -47.42363229721573],
#         "address": "R. Joaquim Procópio de Araújo, 3178 - Centro",
#         "cep": "13631-020",
#         "phone": "(19) 3565-8700",
#         "hours": "24 horas",
#         "emergency": True,
#         "tipo": "privado",
#         "open24h": True,
#         "especialidades": ["Emergência", "Cirurgia", "Clínica Médica"]
#     },
#     {
#         "id": 3,
#         "name": "CEM - Centro de Especialidades Médicas",
#         "location": [-22.012212172100142, -47.43061244487763],
#         "address": "Av. Antônio Joaquim Mendes, 1001 - Jardim Europa",
#         "cep": "13631-110",
#         "phone": "(19) 3563-5050",
#         "hours": "07:00 às 19:00",
#         "emergency": False,
#         "tipo": "publico",
#         "open24h": False,
#         "especialidades": ["Consultas", "Exames"]
#     }
# ]

# def is_hospital_open(hospital):
#     sp_timezone = pytz.timezone('America/Sao_Paulo')
#     now = datetime.now(sp_timezone)
#     hour = now.hour
#     day = now.weekday()
    
#     if hospital["open24h"]:
#         return True
    
#     if not hospital["open24h"] and (day >= 5):
#         return False
#     return 7 <= hour < 19

# def create_map(hospitals_to_show, center_location=None):
#     if center_location:
#         m = folium.Map(location=center_location, zoom_start=14, min_zoom=13, max_zoom=16)
#     else:
#         m = folium.Map(location=[-21.997, -47.425], zoom_start=14, min_zoom=13, max_zoom=16)
    
#     for hospital in hospitals_to_show:
#         status = "Aberto Agora" if is_hospital_open(hospital) else "Fechado"
#         color = "green" if is_hospital_open(hospital) else "red"
#         media_estrelas = calcular_media_estrelas(hospital['id'])
        
#         popup_html = f"""
#         <div class="popup-content">
#             <h3>{hospital['name']}</h3>
#             <p><span class="status-{color}">{status}</span></p>
#             <p>⭐ {media_estrelas}/5</p>
#             <p><strong>Telefone:</strong> {hospital['phone']}</p>
#             <p><strong>Horário:</strong> {hospital['hours']}</p>
#         </div>
#         """
        
#         folium.Marker(
#             hospital["location"],
#             popup=popup_html,
#             icon=folium.Icon(color=color, icon="info-sign")
#         ).add_to(m)
    
#     return m

# def main():
#     # Inicializar arquivos de dados
#     init_data_files()
    
#     # Carregar CSS
#     load_css()
    
#     # Cabeçalho
#     st.title("🏥 Emergências Médicas Pirassununga")
    
#     # Filtros
#     col1, col2 = st.columns(2)
#     with col1:
#         tipo_atendimento = st.selectbox(
#             "Tipo de atendimento",
#             ["todos", "publico", "privado"],
#             format_func=lambda x: "Todos os Hospitais" if x == "todos" else 
#                                "Saúde Pública" if x == "publico" else "Hospitais Privados"
#         )
    
#     # Filtrar hospitais
#     filtered_hospitals = [h for h in hospitals if tipo_atendimento == "todos" or h["tipo"] == tipo_atendimento]
    
#     # Mapa e informações
#     col_map, col_info = st.columns([2, 1])
    
#     with col_map:
#         map_data = create_map(filtered_hospitals)
#         st_folium(map_data, width=800, height=500)
    
#     with col_info:
#         if filtered_hospitals:
#             for hospital in filtered_hospitals:
#                 with st.expander(f"ℹ️ Informações: {hospital['name']}", expanded=False):
#                     media = calcular_media_estrelas(hospital['id'])
#                     st.markdown(f"### {hospital['name']}")
#                     st.markdown(f"⭐ Avaliação média: {media}/5")
#                     st.markdown(f"**Endereço:** {hospital['address']}")
#                     st.markdown(f"**CEP:** {hospital['cep']}")
#                     st.markdown(f"**Telefone:** {hospital['phone']}")
#                     st.markdown(f"**Horário:** {hospital['hours']}")
#                     st.markdown("**Especialidades:**")
#                     for esp in hospital['especialidades']:
#                         st.markdown(f"- {esp}")
                    
#                     # Sistema de avaliação
#                     st.markdown("### Avaliar Atendimento")
#                     estrelas = st.slider("Quantas estrelas você dá?", 1, 5, 3, key=f"stars_{hospital['id']}")
#                     comentario = st.text_area("Comentário (opcional)", key=f"comment_{hospital['id']}")
#                     if st.button("Enviar Avaliação", key=f"btn_aval_{hospital['id']}"):
#                         save_avaliacao(hospital['id'], estrelas, comentario)
#                         st.success("Avaliação enviada com sucesso!")
                    
#                     # Sistema de denúncias
#                     st.markdown("### Fazer Denúncia")
#                     denuncia = st.text_area("Descreva o ocorrido", key=f"denuncia_{hospital['id']}")
#                     if st.button("Enviar Denúncia", key=f"btn_den_{hospital['id']}"):
#                         save_denuncia(hospital['id'], denuncia)
#                         st.success("Denúncia registrada com sucesso!")

#     # Seção de rotas
#     st.markdown("### 🚗 Como Chegar")
#     endereco = st.text_input("Digite seu endereço para calcular a rota:")
#     if endereco:
#         for hospital in filtered_hospitals:
#             st.markdown(f"""
#             <a href="https://www.google.com/maps/dir/?api=1&origin={endereco}&destination={hospital['location'][0]},{hospital['location'][1]}" 
#                target="_blank" class="button">
#                 Rota para {hospital['name']}
#             </a>
#             """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import pytz
import os
import pandas as pd
import json

# Configuração da página
st.set_page_config(
    page_title="Emergências Médicas Pirassununga",
    layout="wide",
)

# Inicialização dos arquivos de dados
def init_data_files():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Arquivo de avaliações
    if not os.path.exists('data/avaliacoes.csv'):
        pd.DataFrame(columns=['hospital_id', 'estrelas', 'comentario', 'data']).to_csv('data/avaliacoes.csv', index=False)
    
    # Arquivo de denúncias
    if not os.path.exists('data/denuncias.csv'):
        pd.DataFrame(columns=['hospital_id', 'descricao', 'data', 'status']).to_csv('data/denuncias.csv', index=False)

# Função para verificar se já avaliou
def ja_avaliou(hospital_id):
    df = pd.read_csv('data/avaliacoes.csv')
    return hospital_id in df['hospital_id'].values

# Funções de dados
def save_avaliacao(hospital_id, estrelas, comentario):
    if not ja_avaliou(hospital_id):
        df = pd.read_csv('data/avaliacoes.csv')
        nova_avaliacao = pd.DataFrame([{
            'hospital_id': hospital_id,
            'estrelas': estrelas,
            'comentario': comentario,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])
        df = pd.concat([df, nova_avaliacao], ignore_index=True)
        df.to_csv('data/avaliacoes.csv', index=False)
        return True
    return False

def save_denuncia(hospital_id, descricao):
    df = pd.read_csv('data/denuncias.csv')
    nova_denuncia = pd.DataFrame([{
        'hospital_id': hospital_id,
        'descricao': descricao,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Pendente'
    }])
    df = pd.concat([df, nova_denuncia], ignore_index=True)
    df.to_csv('data/denuncias.csv', index=False)

def export_to_json():
    avaliacoes = pd.read_csv('data/avaliacoes.csv')
    denuncias = pd.read_csv('data/denuncias.csv')
    
    relatorio = {
        "data_geracao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "hospitais": {}
    }
    
    for hospital in hospitals:
        hosp_id = hospital['id']
        hosp_avaliacoes = avaliacoes[avaliacoes['hospital_id'] == hosp_id]
        hosp_denuncias = denuncias[denuncias['hospital_id'] == hosp_id]
        
        relatorio["hospitais"][hospital['name']] = {
            "informacoes": {
                "endereco": hospital['address'],
                "telefone": hospital['phone'],
                "tipo": "Público" if hospital['tipo'] == "publico" else "Privado"
            },
            "avaliacoes": {
                "media_estrelas": round(hosp_avaliacoes['estrelas'].mean(), 2) if len(hosp_avaliacoes) > 0 else 0,
                "total_avaliacoes": len(hosp_avaliacoes),
                "comentarios": hosp_avaliacoes[['data', 'estrelas', 'comentario']].to_dict('records')
            },
            "denuncias": hosp_denuncias[['data', 'descricao', 'status']].to_dict('records')
        }
    
    with open('data/relatorio.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=4)

# Dados dos hospitais (mantido o mesmo)
hospitals = [
    {
        "id": 1,
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
        "id": 2,
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
        "id": 3,
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
    day = now.weekday()
    
    if hospital["open24h"]:
        return True
    
    if not hospital["open24h"] and (day >= 5):
        return False
    return 7 <= hour < 19

def create_map(hospitals_to_show):
    m = folium.Map(location=[-21.997, -47.425], zoom_start=14)
    
    for hospital in hospitals_to_show:
        status = "Aberto Agora" if is_hospital_open(hospital) else "Fechado"
        color = "green" if is_hospital_open(hospital) else "red"
        
        popup_html = f"""
        <div class="popup-content">
            <h3>{hospital['name']}</h3>
            <p><span class="status-{color}">{status}</span></p>
            <p><strong>Telefone:</strong> {hospital['phone']}</p>
        </div>
        """
        
        folium.Marker(
            hospital["location"],
            popup=popup_html,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)
    
    return m

def main():
    init_data_files()
    
    # Sidebar
    with st.sidebar:
        st.title("🏥 Menu")
        tipo_atendimento = st.radio(
            "Tipo de Atendimento",
            ["Saúde Pública", "Plano de Saúde"],
            format_func=lambda x: "Saúde Pública (SUS)" if x == "Saúde Pública" else "Plano de Saúde (Unimed)"
        )
        
        st.markdown("---")
        
        if st.button("📊 Exportar Relatório"):
            export_to_json()
            st.success("Relatório exportado em data/relatorio.json")
        
        st.markdown("---")
        st.markdown("### ⚡ Emergência")
        st.markdown("**SAMU:** 192")
        st.markdown("**Bombeiros:** 193")
    
    # Conteúdo principal
    st.title("Emergências Médicas Pirassununga")
    
    # Filtrar hospital baseado na seleção
    selected_type = "publico" if tipo_atendimento == "Saúde Pública" else "privado"
    hospital = next(h for h in hospitals if h["tipo"] == selected_type and h["emergency"])
    
    # Mapa e informações principais
    col1, col2 = st.columns([2, 1])
    
    with col1:
        map_data = create_map([hospital])
        st_folium(map_data, width=700, height=400)
    
    with col2:
        st.markdown(f"### {hospital['name']}")
        st.markdown(f"**Endereço:** {hospital['address']}")
        st.markdown(f"**Telefone:** {hospital['phone']}")
        st.markdown(f"**Horário:** {hospital['hours']}")
        st.markdown("**Especialidades:**")
        for esp in hospital['especialidades']:
            st.markdown(f"- {esp}")
    
    # Sistema de avaliação
    st.markdown("---")
    tabs = st.tabs(["⭐ Avaliação", "📝 Denúncia"])
    
    with tabs[0]:
        if ja_avaliou(hospital['id']):
            st.warning("Você já avaliou este hospital.")
        else:
            col1, col2 = st.columns([1, 2])
            with col1:
                estrelas = st.slider("Avaliação", 1, 5, 3)
            with col2:
                comentario = st.text_input("Comentário (opcional)")
            
            if st.button("Enviar Avaliação"):
                if save_avaliacao(hospital['id'], estrelas, comentario):
                    st.success("Avaliação enviada com sucesso!")
                else:
                    st.error("Você já avaliou este hospital anteriormente.")
    
    with tabs[1]:
        denuncia = st.text_area("Descreva o ocorrido (opcional)")
        if denuncia and st.button("Enviar Denúncia"):
            save_denuncia(hospital['id'], denuncia)
            st.success("Denúncia registrada com sucesso!")
    
    # Rota
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        endereco = st.text_input("Digite seu endereço para calcular a rota:")
    with col2:
        if endereco:
            st.markdown(f"""
            <a href="https://www.google.com/maps/dir/?api=1&origin={endereco}&destination={hospital['location'][0]},{hospital['location'][1]}" 
               target="_blank" class="button">
                Como Chegar
            </a>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()