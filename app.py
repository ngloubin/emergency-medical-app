# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from datetime import datetime
# import pytz
# import os
# import pandas as pd
# import json

# # Configuração da página
# st.set_page_config(
#     page_title="Emergências Médicas Pirassununga",
#     layout="wide",
# )

# # CSS para estilizar os popups do mapa
# st.markdown("""
# <style>
# .popup-content h3 {
#     margin: 0;
#     font-size: 16px;
# }
# .popup-content p {
#     margin: 5px 0;
# }
# .status-green {
#     color: green;
#     font-weight: bold;
# }
# .status-red {
#     color: red;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

# # Inicialização dos arquivos de dados
# def init_data_files():
#     if not os.path.exists('data'):
#         os.makedirs('data')
#     if not os.path.exists('data/avaliacoes.csv'):
#         pd.DataFrame(columns=['hospital_id', 'estrelas', 'comentario', 'data']).to_csv('data/avaliacoes.csv', index=False)
#     if not os.path.exists('data/denuncias.csv'):
#         pd.DataFrame(columns=['hospital_id', 'descricao', 'data', 'status']).to_csv('data/denuncias.csv', index=False)

# # Funções de dados
# def ja_avaliou(hospital_id):
#     df = pd.read_csv('data/avaliacoes.csv')
#     return hospital_id in df['hospital_id'].values

# def save_avaliacao(hospital_id, estrelas, comentario):
#     if not ja_avaliou(hospital_id):
#         df = pd.read_csv('data/avaliacoes.csv')
#         nova_avaliacao = pd.DataFrame([{
#             'hospital_id': hospital_id,
#             'estrelas': estrelas,
#             'comentario': comentario,
#             'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         }])
#         df = pd.concat([df, nova_avaliacao], ignore_index=True)
#         df.to_csv('data/avaliacoes.csv', index=False)
#         return True
#     return False

# def save_denuncia(hospital_id, descricao):
#     df = pd.read_csv('data/denuncias.csv')
#     nova_denuncia = pd.DataFrame([{
#         'hospital_id': hospital_id,
#         'descricao': descricao,
#         'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'status': 'Pendente'
#     }])
#     df = pd.concat([df, nova_denuncia], ignore_index=True)
#     df.to_csv('data/denuncias.csv', index=False)

# def export_to_json():
#     avaliacoes = pd.read_csv('data/avaliacoes.csv')
#     denuncias = pd.read_csv('data/denuncias.csv')
#     relatorio = {
#         "data_geracao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         "hospitais": {}
#     }
#     for hospital in hospitals:
#         hosp_id = hospital['id']
#         hosp_avaliacoes = avaliacoes[avaliacoes['hospital_id'] == hosp_id]
#         hosp_denuncias = denuncias[denuncias['hospital_id'] == hosp_id]
#         relatorio["hospitais"][hospital['name']] = {
#             "informacoes": {
#                 "endereco": hospital['address'],
#                 "telefone": hospital['phone'],
#                 "tipo": "Público" if hospital['tipo'] == "publico" else "Privado"
#             },
#             "avaliacoes": {
#                 "media_estrelas": round(hosp_avaliacoes['estrelas'].mean(), 2) if len(hosp_avaliacoes) > 0 else 0,
#                 "total_avaliacoes": len(hosp_avaliacoes),
#                 "comentarios": hosp_avaliacoes[['data', 'estrelas', 'comentario']].to_dict('records')
#             },
#             "denuncias": hosp_denuncias[['data', 'descricao', 'status']].to_dict('records')
#         }
#     with open('data/relatorio.json', 'w', encoding='utf-8') as f:
#         json.dump(relatorio, f, ensure_ascii=False, indent=4)

# # Dados dos hospitais (atualizados com PAM)
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
#         "address": "R. Joaquim Procópio de Araújo, 3178 - Centro, Pirassununga - SP, 13631-020",
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
#         "name": "(PAM) Dr.Rubens Luiz Costa, ZONA NORTE - Centro de Especialidades Médicas",
#         "location": [-21.967872223919944, -47.43100153976281],
#         "address": "Usf Dr Rubens Luis Costa, Rua Paulo Moreira, s/n – Parque Clayton Malaman - Jardim Ferrari II, Pirassununga - SP, 13635-240",
#         "cep": "13635-240",
#         "phone": "Não disponível",
#         "hours": "07:00 às 22:00",
#         "emergency": True,
#         "tipo": "publico",
#         "open24h": False,
#         "especialidades": ["Emergência", "Centro de Especialidades Médicas"]
#     }
# ]

# # Funções auxiliares
# def is_hospital_open(hospital):
#     sp_timezone = pytz.timezone('America/Sao_Paulo')
#     now = datetime.now(sp_timezone)
#     hour = now.hour
#     day = now.weekday()
#     if hospital["open24h"]:
#         return True
#     if not hospital["open24h"] and (day >= 5):  # Fins de semana
#         return False
#     return 7 <= hour < 22  # Ajustado para o PAM

# def create_map(hospitals_to_show):
#     m = folium.Map(location=[-21.997, -47.425], zoom_start=14)
#     for hospital in hospitals_to_show:
#         status = "Aberto Agora" if is_hospital_open(hospital) else "Fechado"
#         color = "green" if is_hospital_open(hospital) else "red"
#         popup_html = f"""
#         <div class="popup-content">
#             <h3>{hospital['name']}</h3>
#             <p><span class="status-{color}">{status}</span></p>
#             <p><strong>Telefone:</strong> {hospital['phone']}</p>
#         </div>
#         """
#         folium.Marker(
#             hospital["location"],
#             popup=popup_html,
#             icon=folium.Icon(color=color, icon="info-sign")
#         ).add_to(m)
#     return m

# # Easter Egg
# def show_capy():
#     st.markdown("""
#     <h3>Você encontrou o segredo! 🎉</h3>
#     <p>Jogue Capybara Clicker abaixo:</p>
#     <iframe src="https://capybara-game.com/" width="800" height="600"></iframe>
#     """, unsafe_allow_html=True)

# # Leitor Automático
# def auto_reader(content):
#     if st.button("Ativar Leitor Automático 📢", key="auto_reader"):
#         st.markdown(f'<audio controls autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={content}&tl=pt-br&client=tw-ob" type="audio/mpeg"></audio>', unsafe_allow_html=True)

# # Inicialização
# init_data_files()

# # Sidebar (apenas seleção e exportação)
# with st.sidebar:
#     st.title("🏥 Menu")
#     tipo_atendimento = st.radio(
#         "Tipo de Atendimento",
#         ["Saúde Pública", "Plano de Saúde"],
#         format_func=lambda x: "Saúde Pública (SUS)" if x == "Saúde Pública" else "Plano de Saúde (Unimed)"
#     )
#     selected_type = "publico" if tipo_atendimento == "Saúde Pública" else "privado"
    
#     filtered_hospitals = [h for h in hospitals if h["tipo"] == selected_type and h["emergency"]]
#     if not filtered_hospitals:
#         st.error("Nenhum hospital disponível para este tipo de atendimento.")
#     elif len(filtered_hospitals) > 1:
#         hospital_options = {h["name"]: h for h in filtered_hospitals}
#         selected_name = st.selectbox("Selecione um hospital:", list(hospital_options.keys()), key="select_hospital")
#         hospital = hospital_options[selected_name]
#     else:
#         hospital = filtered_hospitals[0]
    
#     st.markdown("---")
#     if st.button("📊 Exportar Relatório"):
#         export_to_json()
#         st.success("Relatório exportado com sucesso!")

# # Conteúdo Principal
# st.title("Emergências Médicas Pirassununga")

# # Mapa e Informações
# col1, col2 = st.columns([2, 1])
# with col1:
#     map_data = create_map([hospital])
#     st_folium(map_data, width=700, height=400)
# with col2:
#     is_open = is_hospital_open(hospital)
#     status = "Aberto Agora" if is_open else "Fechado"
#     st.markdown(f"### {hospital['name']}")
#     st.markdown(f"**Status:** {status}")
#     st.markdown(f"**Endereço:** {hospital['address']}")
#     st.markdown(f"**Telefone:** {hospital['phone']}")
#     st.markdown(f"**Horário:** {hospital['hours']}")
#     st.markdown("**Especialidades:**")
#     for esp in hospital['especialidades']:
#         st.markdown(f"- {esp}")

# # Avaliação e Denúncia
# st.markdown("---")
# tabs = st.tabs(["⭐ Avaliação", "📝 Denúncia"])
# with tabs[0]:
#     if ja_avaliou(hospital['id']):
#         st.warning("Você já avaliou este hospital.")
#     else:
#         col_av1, col_av2 = st.columns([1, 2])
#         with col_av1:
#             estrelas = st.slider("Avaliação", 1, 5, 3, key=f"estrelas_{hospital['id']}")
#         with col_av2:
#             comentario = st.text_input("Comentário (opcional)", key=f"comentario_{hospital['id']}")
#         if st.button("Enviar Avaliação", key=f"avaliar_{hospital['id']}"):
#             if save_avaliacao(hospital['id'], estrelas, comentario):
#                 st.success("Avaliação enviada com sucesso!")
#             else:
#                 st.error("Erro ao enviar avaliação.")
# with tabs[1]:
#     denuncia = st.text_area("Descreva o ocorrido (opcional)", key=f"denuncia_{hospital['id']}")
#     if denuncia and st.button("Enviar Denúncia", key=f"denunciar_{hospital['id']}"):
#         save_denuncia(hospital['id'], denuncia)
#         st.success("Denúncia registrada com sucesso!")

# # Traçar Rota
# st.markdown("---")
# st.markdown("### 📍 Traçar Rota")
# col_route1, col_route2 = st.columns([3, 1])
# with col_route1:
#     endereco_usuario = st.text_input("Digite seu endereço:", key="endereco_usuario")
# with col_route2:
#     if endereco_usuario:
#         url = f"https://www.google.com/maps/dir/?api=1&origin={endereco_usuario}&destination={hospital['address']}"
#         st.markdown(f'<a href="{url}" target="_blank">Como Chegar</a>', unsafe_allow_html=True)

# # Emergência e Easter Egg
# st.markdown("---")
# st.markdown("### ⚡ Emergência")
# st.markdown("**SAMU:** 192")
# st.markdown("**Bombeiros:** 193")

# st.markdown("---")
# st.markdown("### 🔍 Busca Secreta")
# easter_egg_search = st.text_input("Digite o código secreto:", key="easter_egg_search")
# if easter_egg_search.strip() == "111":
#     show_capy()
#     st.stop()

# # Leitor Automático
# st.markdown("---")
# auto_reader(f"Informações do hospital: {hospital['name']}, Endereço: {hospital['address']}, Telefone: {hospital['phone']}")
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
    if not os.path.exists('data/avaliacoes.csv'):
        pd.DataFrame(columns=['hospital_id', 'estrelas', 'comentario', 'data']).to_csv('data/avaliacoes.csv', index=False)
    if not os.path.exists('data/denuncias.csv'):
        pd.DataFrame(columns=['hospital_id', 'descricao', 'data', 'status']).to_csv('data/denuncias.csv', index=False)

# Funções de dados
def ja_avaliou(hospital_id):
    df = pd.read_csv('data/avaliacoes.csv')
    return hospital_id in df['hospital_id'].values

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

# Dados dos hospitais
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
        "name": "(PAM) Dr.Rubens Luiz Costa (ZONA NORTE)",
        "location": [-21.967872223919944, -47.43100153976281],
        "address": "Rua Paulo Moreira, s/n – Parque Clayton Malaman - Jardim Ferrari II, Pirassununga - SP, 13635-240",
        "cep": "13635-240",
        "phone": "Não disponível",
        "hours": "07:00 às 22:00",
        "emergency": True,
        "tipo": "publico",
        "open24h": False,
        "especialidades": ["Emergência", "Especialidades Médicas"]
    }
]

# Funções auxiliares
def is_hospital_open(hospital):
    sp_timezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(sp_timezone)
    hour = now.hour
    day = now.weekday()
    if hospital["open24h"]:
        return True
    if not hospital["open24h"] and (day >= 5):
        return False
    return 7 <= hour < 22

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

# Easter Egg
def show_capy():
    st.markdown("""
    <h3>Você encontrou o segredo! 🎉</h3>
    <p>Jogue Capybara clicker abaixo:</p>
    <iframe src="https://capybara-game.com/" width="800" height="600"></iframe>
    """, unsafe_allow_html=True)

# Leitor Automático
def auto_reader(content):
    if st.button("Ativar Leitor Automático 📢", key="auto_reader"):
        st.markdown(f'<audio controls autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={content}&tl=pt-br&client=tw-ob" type="audio/mpeg"></audio>', unsafe_allow_html=True)

# Inicialização
init_data_files()

# Sidebar
with st.sidebar:
    st.title("🏥 Menu")
    tipo_atendimento = st.radio(
        "Tipo de Atendimento",
        ["Saúde Pública", "Plano de Saúde"],
        format_func=lambda x: "Saúde Pública (SUS)" if x == "Saúde Pública" else "Plano de Saúde (Unimed)"
    )
    selected_type = "publico" if tipo_atendimento == "Saúde Pública" else "privado"

    st.markdown("---")
    st.markdown("### ⚡ Emergência")
    st.markdown("**SAMU:** 192")
    st.markdown("**Bombeiros:** 193")

    st.markdown("---")
    st.markdown("### 🔍 Busca Secreta")
    easter_egg_search = st.text_input("Digite o código secreto:", key="easter_egg_search")
    if easter_egg_search.strip() == "111":
        show_capy()
        st.stop()

    st.markdown("---")
    if st.button("📊 Exportar Relatório"):
        export_to_json()
        st.success("Relatório exportado com sucesso!")

# Conteúdo Principal
st.title("Emergências Médicas Pirassununga")

# Filtrar hospitais com base no tipo de atendimento
filtered_hospitals = [h for h in hospitals if h["tipo"] == selected_type and h["emergency"]]

if not filtered_hospitals:
    st.error("Nenhum hospital disponível para este tipo de atendimento.")
else:
    # Selecione um hospital (só para Saúde Pública)
    if selected_type == "publico":
        hospital_options = {h["name"]: h for h in filtered_hospitals}
        selected_name = st.selectbox("Selecione um hospital:", list(hospital_options.keys()), key="select_hospital")
        hospital = hospital_options[selected_name]
    else:
        hospital = filtered_hospitals[0]  # Unimed para Plano de Saúde

    # Mapa e informações principais
    col1, col2 = st.columns([2, 1])
    with col1:
        map_data = create_map([hospital])
        st_folium(map_data, width=700, height=400)
    with col2:
        is_open = is_hospital_open(hospital)
        status = "Aberto Agora" if is_open else "Fechado"
        st.markdown(f"### {hospital['name']}")
        st.markdown(f"**Status:** {status}")
        st.markdown(f"**Endereço:** {hospital['address']}")
        st.markdown(f"**Telefone:** {hospital['phone']}")
        st.markdown(f"**Horário:** {hospital['hours']}")
        st.markdown("**Especialidades:**")
        for esp in hospital['especialidades']:
            st.markdown(f"- {esp}")

    # Sistema de avaliação e denúncia
    st.markdown("---")
    tabs = st.tabs(["⭐ Avaliação", "📝 Denúncia"])
    with tabs[0]:
        if ja_avaliou(hospital['id']):
            st.warning("Você já avaliou este hospital.")
        else:
            col_av1, col_av2 = st.columns([1, 2])
            with col_av1:
                estrelas = st.slider("Avaliação", 1, 5, 3, key=f"estrelas_{hospital['id']}")
            with col_av2:
                comentario = st.text_input("Comentário (opcional)", key=f"comentario_{hospital['id']}")
            if st.button("Enviar Avaliação", key=f"avaliar_{hospital['id']}"):
                if save_avaliacao(hospital['id'], estrelas, comentario):
                    st.success("Avaliação enviada com sucesso!")
                else:
                    st.error("Erro ao enviar avaliação.")
    with tabs[1]:
        denuncia = st.text_area("Descreva o ocorrido (opcional)", key=f"denuncia_{hospital['id']}")
        if denuncia and st.button("Enviar Denúncia", key=f"denunciar_{hospital['id']}"):
            save_denuncia(hospital['id'], denuncia)
            st.success("Denúncia registrada com sucesso!")

    # Leitor Automático
    st.markdown("---")
    auto_reader(f"Informações do hospital: {hospital['name']}, Endereço: {hospital['address']}, Telefone: {hospital['phone']}")

    # Traçar Rota
    st.markdown("---")
    st.markdown("### 📍 Traçar Rota")
    col_route1, col_route2 = st.columns([3, 1])
    with col_route1:
        endereco_usuario = st.text_input("Digite seu endereço:", key="endereco_usuario")
    with col_route2:
        if endereco_usuario:
            url = f"https://www.google.com/maps/dir/?api=1&origin={endereco_usuario}&destination={hospital['address']}"
            st.markdown(f'<a href="{url}" target="_blank">Como Chegar</a>', unsafe_allow_html=True)