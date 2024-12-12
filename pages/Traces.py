import streamlit as st
import streamlit_mermaid as stmd
from typing import Dict, List
from utils import (
    fetch_execution_ids,
    load_chat_history,
    label_id_map,
    load_state_visibility,
    load_message_attributes_visibility,
    load_state_snapshots,
    load_mermaid
)
from components import (
    message_container_template,
    tags_template,
    chat_container_style,
    tag_style,
    tags_area_style,
)

# Page config
st.set_page_config(
    page_title="Traces",
    page_icon="🤖",
    layout="wide"
)

if "tracer_execution_id" not in st.session_state:
    st.session_state["tracer_execution_id"] = ""
if "tracer_execution_label" not in st.session_state:
    st.session_state["tracer_execution_label"] = ""
if "tracer_chat_history" not in st.session_state:
    st.session_state["tracer_chat_history"] = []
if "tracer_state_visibility" not in st.session_state:
    st.session_state["tracer_state_visibility"] = {}
if "tracer_msg_attr_visibility" not in st.session_state:
    st.session_state["tracer_msg_attr_visibility"] = {}
if "tracer_state_snapshots" not in st.session_state:
    st.session_state["tracer_state_snapshots"] = []
if "tracer_mermaid" not in st.session_state:
    st.session_state["tracer_mermaid"] = ""

st.markdown("""<style>img{border-radius:15px;}</style>""", unsafe_allow_html=True)

ids = fetch_execution_ids()

if not ids:
    st.header(':mag: Hmm... There is no execution yet.')
    st.image('./assets/images/notfound.jpg', width=800)
    st.warning("There don't seem to be your langgraph execution. Please execute some lanngraph at ChatInterface Page.", icon="⚠️")
else:
    LABEL_ID_MAP: Dict[str, Dict[str, str]] = label_id_map(ids)

    st.markdown(chat_container_style, unsafe_allow_html=True)
    st.markdown(tag_style, unsafe_allow_html=True)
    st.markdown(tags_area_style, unsafe_allow_html=True)

    st.header("Chat Interface")

    with st.form(
            key="select_execution",
            clear_on_submit=False,
            enter_to_submit=False,
            border=True
        ):
        
        execution_label = st.selectbox(
            'Which number do you like best?',
            [label for label in LABEL_ID_MAP.keys()],
            index = (
                [label for label in LABEL_ID_MAP.keys()].index(st.session_state["tracer_execution_label"])
                if st.session_state["tracer_execution_label"] != "" else 0
            )
        )
        submit = st.form_submit_button('Search')

    chat_history = st.container()
    mermaid_view = st.container()
    visible_state_list = st.container()
    state_snapshots_area = st.container()

    with chat_history:
        messages_component = ""
        for message in st.session_state["tracer_chat_history"]:
            st.write(message_container_template(message), unsafe_allow_html=True) 

    with mermaid_view:
        if st.session_state["tracer_mermaid"] != "":
            st.subheader(f"	:robot_face: Graph Structure", divider="violet")
            stmd.st_mermaid(st.session_state["tracer_mermaid"], height="400px")

    with visible_state_list:
        if len(st.session_state["tracer_state_visibility"]) > 0 and len(st.session_state["tracer_msg_attr_visibility"]) > 0:
            st.subheader(f":dog2: Visualized States", divider="violet")
            st.markdown(tags_template(st.session_state["tracer_state_visibility"]), unsafe_allow_html=True)
            st.markdown(tags_template(st.session_state["tracer_msg_attr_visibility"]), unsafe_allow_html=True)

    with state_snapshots_area:
        counter = 0
        for snapshot in st.session_state["tracer_state_snapshots"]:
            st.subheader(f":feet: Execution Step {counter}", divider="violet")
            st.json(snapshot, expanded=1)
            counter += 1

    if submit:
        # Set session states
        st.session_state["tracer_execution_label"] = execution_label
        st.session_state["tracer_execution_id"] = LABEL_ID_MAP[execution_label]
        history = []
        for message in reversed(load_chat_history(st.session_state["tracer_execution_id"])):
            role, content = message
            history.append((role, content))
        st.session_state["tracer_chat_history"] = history
        st.session_state["tracer_state_visibility"] = load_state_visibility(st.session_state["tracer_execution_id"])
        st.session_state["tracer_msg_attr_visibility"] = load_message_attributes_visibility(st.session_state["tracer_execution_id"])
        st.session_state["tracer_state_snapshots"] = load_state_snapshots(st.session_state["tracer_execution_id"])
        st.session_state["tracer_mermaid"] = load_mermaid(st.session_state["tracer_execution_id"])
        st.rerun()