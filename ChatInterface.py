import copy
import json
import os
import time
import streamlit as st
import streamlit_mermaid as stmd
from typing import Dict, List
from streamlit_chat import message
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from components import (
    message_container_template,
    tags_template,
    chat_container_style,
    tags_area_style,
    tag_style
)
from settings import MERMAID, BOOT_GRAPH, YOUR_GRAPH_STATE
from utils import (
    GraphStateJsonParser,
    save_messages,
    save_states_options,
    save_message_props_options,
    save_state_snapshots,
    save_mermaid_view,
)

# Page config
st.set_page_config(
    page_title="LangGraph Simple Tracer",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    # App Title
    st.title("LangGraph Simple Tracer")
    
    # Author Profile Section
    st.markdown("### Author Profile")
    with st.expander("About the Author", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://img.icons8.com/fluency-systems-filled/96/gender-neutral-user.png", width=50)
        with col2:
            st.markdown("**NAVIFOLIO**")
            st.caption("AI Developer")
            
        st.markdown("""
            - 🚀 AI/ML Engineer
            - 💻 Japanese Tech Writer
        """)
    #    009688 
        # Social Links
        st.markdown("""
            [![GitHub](https://img.shields.io/badge/GitHub-F44336?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)
            """)
    
    # Documentation Links
    st.markdown("### Resources")
    st.markdown("""
        - [Source Code](https://github.com/username/project)
        - [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
        - [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
        - [LangGraph Guide](https://python.langchain.com/docs/langgraph)
    """)
    
    # App Description
    st.markdown("### About")
    st.markdown("""
        This is a chat interface powered by GPT-4. 
        Built with:
        - 🧠 GPT-4/GPT-4o-mini
        - 🎈 Streamlit
        - ⚡ LangChain
        - 📊 LangGraph
        
        Features:
        - Real-time chat responses
        - Message history
        - Stream output support
        - Graph execution visualization
        - State tracing
    """)
    
    # Version Info
    st.sidebar.markdown("---")
    st.sidebar.caption("v1.0.0 | Built with ❤️ using Streamlit")

# Load Component Styles
st.markdown(chat_container_style, unsafe_allow_html=True)
st.markdown(tag_style, unsafe_allow_html=True)
st.markdown(tags_area_style, unsafe_allow_html=True)

GRAPH_STATE: List[str] = [key for key in YOUR_GRAPH_STATE.__annotations__.keys()]
props = set()

for attr in list(HumanMessage.model_fields.keys()):
    props.add(attr)
for attr in list(AIMessage.model_fields.keys()):
    props.add(attr)
for attr in list(ToolMessage.model_fields.keys()):
    props.add(attr)
for attr in list(SystemMessage.model_fields.keys()):
    props.add(attr)

MESSAGE_PROPS: List[str] = props

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "execution_id" not in st.session_state:
    st.session_state["execution_id"] = ""
if "state_visibility" not in st.session_state:
    st.session_state["state_visibility"] = dict(list(
        map(lambda key: (key, True), GRAPH_STATE)
    ))
if "msg_attr_visibility" not in st.session_state:
    st.session_state["msg_attr_visibility"] = dict(list(
        map(lambda key: (key, (key == "content") or (key == "type")), MESSAGE_PROPS)
    ))
if "state_snapshots" not in st.session_state:
    st.session_state["state_snapshots"] = []
if "api_key_exists" not in st.session_state:
    st.session_state["api_key_exists"] = False

st.header("Chat Interface")

# Chat form
with st.form(
    key="prompt",
    clear_on_submit=True,
    enter_to_submit=True,
    border=True
):
    prompt = st.text_input('Prompt')
    visible_state_options = st.multiselect(
        'Select properties of graph state you want see.',
        GRAPH_STATE,
        default=list(
            filter(
                lambda key: st.session_state["state_visibility"][key] == True,
                st.session_state["state_visibility"].keys()
            )
        )
    )
    visible_props_in_message_options = st.multiselect(
        'Select attributes in messages (instance of BaseMessage interface) you want see.',
        MESSAGE_PROPS,
        default=list(
            filter(
                lambda key: st.session_state["msg_attr_visibility"][key] == True,
                st.session_state["msg_attr_visibility"].keys()
            )
        )
    )
    submit = st.form_submit_button('Ask to AI', disabled=not st.session_state["api_key_exists"])

progress_bar_area = st.container()
chat_history = st.container()
mermaid_view = st.container()
visible_state_list = st.container()
state_snapshots_area = st.container()

with chat_history:
    ai_placeholder = st.empty()
    intermediate_steps = st.container()
    human_placeholder = st.empty()
    
    if len(st.session_state["chat_history"]) > 0:
        for message in reversed(st.session_state["chat_history"]):
            st.markdown(message_container_template(message), unsafe_allow_html=True)

with mermaid_view:
    st.subheader(f":robot_face: Graph Structure", divider="violet")
    stmd.st_mermaid(MERMAID, height="400px")

with visible_state_list:
    st.subheader(f":dog2: Visualized States", divider="violet")
    st.markdown(tags_template(st.session_state["state_visibility"]), unsafe_allow_html=True)
    st.markdown(tags_template(st.session_state["msg_attr_visibility"]), unsafe_allow_html=True)

with state_snapshots_area:
    step = 0
    for snapshot in st.session_state["state_snapshots"]:
        st.subheader(f":feet: Execution Step {step}", divider="violet")
        st.json(snapshot)
        step += 1

if submit:
    # Update session states
    for state in st.session_state["state_visibility"].keys():
        if state in visible_state_options:
            st.session_state["state_visibility"][state] = True
        else:
            st.session_state["state_visibility"][state] = False
    
    for attr in st.session_state["msg_attr_visibility"].keys():
        if attr in visible_props_in_message_options:
            st.session_state["msg_attr_visibility"][attr] = True
        else:
            st.session_state["msg_attr_visibility"][attr] = False

    with chat_history:
        human_message_markdown = message_container_template(("human", prompt))
        human_placeholder.markdown(human_message_markdown, unsafe_allow_html=True)

    with progress_bar_area:
        progress_text = "Graph Execution in progress."
        percent_complete = 0
        progress_bar = progress_bar_area.progress(0, text=progress_text)
    
    with visible_state_list:
        st.markdown(tags_template(st.session_state["state_visibility"]), unsafe_allow_html=True)
        st.markdown(tags_template(st.session_state["msg_attr_visibility"]), unsafe_allow_html=True)

    execution_id, response_generator = BOOT_GRAPH(prompt=prompt, history=st.session_state["chat_history"])
            
    step_counter = 0
    original_messages: List[BaseMessage] = []
    state_outputs: List[Dict] = []

    for streaming in response_generator:
        with state_snapshots_area:
            st.subheader(f":feet: Execution Step {step_counter}", divider="violet")
            partial_state = streaming[1]
        
            if "messages" in partial_state:
                original_messages = partial_state["messages"]
                    
            partial_states_json = GraphStateJsonParser(
                states=copy.deepcopy(partial_state),
                visible_state_props=visible_state_options,
                visible_props_in_message=visible_props_in_message_options
            )
                
            states_dict = json.loads(copy.deepcopy(partial_states_json))
            state_outputs.append(states_dict)

            st.json(partial_states_json, expanded=1)

        with progress_bar_area:
            percent_complete += 5
            for i in range(5):
                percent_complete += 1
                progress_bar.progress(percent_complete, text=progress_text) 
                time.sleep(0.01) 
        step_counter += 1
    
    with progress_bar_area:      
        while percent_complete < 90:
            percent_complete += 1
            progress_bar.progress(percent_complete, text=progress_text)
            time.sleep(0.01)
        time.sleep(0.2)
             
        progress_text = "Response Generation Starting..."
        while percent_complete < 100:
            percent_complete += 1
            progress_bar.progress(percent_complete, text=progress_text)
            time.sleep(0.01)

    progress_bar.empty()

    full_response = "" 
    if len(original_messages) > 1:
        for chunk in original_messages[-1].content:
            full_response += chunk
            ai_message_markdown = message_container_template(("ai", full_response))
            ai_placeholder.markdown(ai_message_markdown, unsafe_allow_html=True)
            time.sleep(0.02)

    st.session_state['execution_id'] = execution_id
    st.session_state["chat_history"].append(("human", prompt))
    st.session_state["chat_history"].append(("ai", full_response))
    st.session_state["state_snapshots"] = state_outputs

    save_messages(thread_id=execution_id, messages=st.session_state['chat_history'])
    save_states_options(thread_id=execution_id, state_visibility_options=st.session_state["state_visibility"])
    save_message_props_options(thread_id=execution_id, attr_visibility_options=st.session_state["msg_attr_visibility"])
    save_state_snapshots(thread_id=execution_id, state_outputs=st.session_state["state_snapshots"])
    save_mermaid_view(thread_id=execution_id, mermaid=MERMAID)

    st.rerun()