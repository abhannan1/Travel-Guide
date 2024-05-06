import streamlit as st
# import plotly.graph_objects as go
import leafmap.foliumap as leafmap
import random
from functions_json import function_json
from openai import OpenAI
# import leafmap.plotlymap as leafmap
import streamlit.components.v1 as components
from model import on_text_input 


st.set_page_config(
    page_title="Wanderlust",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Wanderlust")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state.to_dict())

# client : OpenAI = OpenAI()

if "map" not in st.session_state:
    st.session_state["map"] = {
        "longitude":67.023468,
        "latitude":24.854821,
        "zoom":16,
    }

if "conversation" not in st.session_state:
    st.session_state["conversation"] = [
        {
            "role":"assistant", 
            "message":random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
            )
        }
    ]


if "assistant" not in st.session_state:
    st.session_state["assistant"] = [] #client.beta.assistants.retrieve(assistant_id="asst_4038WBrX3kb0GAWdt3ehSvu6")
    # st.session_state["assistant"] = client.beta.assistants.create(
    #     name="Travel Guide",
    #     model="gpt-4-turbo-1106",
    #     tool=[{"type":"function", "function":function_json}, {"type": "code_interpreter"}],
    #     instructions="You are a travel guid to the people exploring world, finding the best travel or destination plan and update and mark the map with locations of the plan"
    # )
    st.session_state["thread"] = [] # client.beta.threads.create()
    st.session_state["run"] = None



left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Conversation")
    for message in st.session_state["conversation"]:
    #     st.chat_message(message["role"],avatar= "🤖" if message["role"] == "assistant" else "👦🏻")
    #     st.markdown(message["message"])
        with st.chat_message(message["role"],avatar= "🤖" if message["role"] == "assistant" else "👦🏻"):
            st.write(message["message"])

with right_col:
    st.subheader("Map")
    # fig = go.Figure(go.Scattermapbox())
    # fig.update_layout(
    #     mapbox=dict(
    #         # accesstoken="Write_access_token",
    #         # style="open-street-map",  # Specify OpenStreetMap as the style
    #         style="stamen-toner",  # Specify OpenStreetMap as the style
    #         center=go.layout.mapbox.Center(
    #             lat=st.session_state["map"]["latitude"],
    #             lon=st.session_state["map"]["longitude"]
    #         ),
    #       zoom = st.session_state["map"]["zoom"]
    #     ),
    #     margin=dict(l=0,r=0,t=0,b=0),
    # )

    # st.plotly_chart(
    #     fig,
    #     config={"displayModeBar": False},
    #     use_container_width=True,
    #     key="plotly",
    # )
  
    # Create a Leafmap instance
    m = leafmap.Map()
    # Add markers or other Leaflet elements as needed
    # (Example: Adding a marker)
    m.add_marker(
        location=[st.session_state["map"]["latitude"], 
                  st.session_state["map"]["longitude"]], 
        zoom=st.session_state["map"]["zoom"]
    )
    
    m.set_center(
        st.session_state["map"]["longitude"], 
        st.session_state["map"]["latitude"], 
        zoom=st.session_state["map"]["zoom"])
    
    m.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
    name="Google Satellite",
    attribution="Google",
    )

    if st.button("add more layers"):
        # m.add_basemap("Esri.NatGeoWorldMap")
        m.add_basemap("TERRAIN")
        # m.add_basemap("OpenTopoMap")

        
    # m.add_legend(builtin_legend="NWI")

    components.html(m.to_html(), height=600)



st.chat_input(
    placeholder="Ask your question",
    key="input_user_msg",
    on_submit=on_text_input,
)
