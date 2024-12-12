import datetime
import json
import os
import sqlite3
import uuid
from dotenv import load_dotenv
from typing import List, Tuple, Dict

load_dotenv()

CREATE_STATES_OPTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS state_options(
    id TEXT RPIMARY KEY,
    thread_id TEXT,
    name TEXT,
    visible INTEGER
)
"""

CREATE_MESSAGE_PROPS_OPTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS message_props_options(
    id TEXT PRIMARY KEY,
    thread_id TEXT,
    name TEXT,
    visible INTEGER
)
"""

CREATE_CHAT_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS chat_history(
    id TEXT PRIMARY KEY,
    thread_id TEXT, 
    message_index INTEGER,
    type TEXT, 
    content TEXT,
    time TEXT
)"""

CREATE_STATE_OUTPUT_TABLE = """
CREATE TABLE IF NOT EXISTS state_output(
    id TEXT PRIMARY KEY,
    thread_id TEXT,
    execution_step INTEGER,
    snapshot JSON
)"""

CREATE_MERMAID_VIEW_TABLE = """
CREATE TABLE IF NOT EXISTS mermaid_views(
    thread_id TEXT PRIMARY KEY,
    mermaid BLOB
)"""

def save_states_options(thread_id: str, state_visibility_options: Dict[str, bool], mock: bool = False) -> None:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    conn.execute(CREATE_STATES_OPTIONS_TABLE)

    for name, visible in state_visibility_options.items():
        if visible:
            conn.execute("INSERT INTO state_options VALUES(:id, :thread_id, :name, :visible)",
                    {"id": str(uuid.uuid4()), "thread_id": thread_id, "name": name, "visible": 1})
        else:
            conn.execute("INSERT INTO state_options VALUES(:id, :thread_id, :name, :visible)",
                    {"id": str(uuid.uuid4()), "thread_id": thread_id, "name": name, "visible": 0})
    conn.commit()
    conn.close()

def save_message_props_options(thread_id: str, attr_visibility_options: Dict[str, bool], mock: bool = False) -> None:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    conn.execute(CREATE_MESSAGE_PROPS_OPTIONS_TABLE)

    for name, visible in attr_visibility_options.items():
        if visible:
            conn.execute("INSERT INTO message_props_options VALUES(:id, :thread_id, :name, :visible)",
                         {"id": str(uuid.uuid4()), "thread_id": thread_id, "name": name, "visible": 1})
        else:
            conn.execute("INSERT INTO message_props_options VALUES(:id, :thread_id, :name, :visible)",
                         {"id": str(uuid.uuid4()), "thread_id": thread_id, "name": name, "visible": 0})
    conn.commit()
    conn.close()

def save_messages(thread_id: str, messages: List[Tuple[str, str]], mock: bool = False) -> None:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    conn.execute(CREATE_CHAT_MESSAGES_TABLE)
    
    for index, message in enumerate(messages):
        role, content = message
        conn.execute("INSERT INTO chat_history VALUES(:id, :thread_id, :message_index, :type, :content, :time)",
                     {"id": str(uuid.uuid4()), "thread_id": thread_id, "message_index": index, "type": role, "content": content, "time": datetime.datetime.now().isoformat()})
    conn.commit()
    conn.close()

def save_state_snapshots(thread_id: str, state_outputs: List[Dict], mock: bool = False) -> None:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    conn.execute(CREATE_STATE_OUTPUT_TABLE)
    
    for index, snapshot_dict in enumerate(state_outputs):
        snapshot = json.dumps(snapshot_dict, ensure_ascii=False, indent=2)
        conn.execute("INSERT INTO state_output VALUES(:id, :thread_id, :execution_step, json(:snapshot))",
                     {"id": str(uuid.uuid4()), "thread_id": thread_id, "execution_step": index, "snapshot": snapshot})
    conn.commit()
    conn.close()

def save_mermaid_view(thread_id: str, mermaid: str, mock: bool = False) -> None:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    binary = mermaid.encode(encoding="utf-8", errors="strict")
    conn.execute(CREATE_MERMAID_VIEW_TABLE)
    conn.execute("INSERT INTO mermaid_views VALUES(:thread_id, :mermaid)",
                 {"thread_id": thread_id, "mermaid": binary})
    conn.commit()
    conn.close()