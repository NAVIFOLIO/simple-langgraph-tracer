import sqlite3
import os
from dotenv import load_dotenv
from typing import List, Tuple, Dict, Any, Union

load_dotenv()

def fetch_execution_ids(mock: bool = False) -> Union[List[str], bool]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND name = 'checkpoints'")
    count = -1
    for row in cursor:
        count, = row
    if count == 0:
        conn.close()
        return False

    cursor.execute("SELECT DISTINCT thread_id from checkpoints")
    
    ids:List[str] = []
    for row in cursor:
        id, = row
        ids.append(id)
    
    conn.close()

    return ids

def label_id_map(ids:List[str], mock: bool = False) -> Dict[str, str]:
    label_map = {}
    
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    
    for id in ids:
        cursor.execute("SELECT content, time FROM chat_history WHERE thread_id = :thread_id AND message_index = 0",
                     {"thread_id": id})
        label: str
        for row in cursor:
            content, time = row
            label = f"{content} : {time}"
        label_map[label] = id

    conn.close()
    return label_map

def load_chat_history(execution_id: str, mock: bool = False) -> List[Tuple[str, str]]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute("SELECT type, content FROM chat_history WHERE thread_id = :thread_id ORDER BY message_index ASC",
                   {"thread_id": execution_id})
    
    chat_messages: List[Tuple[str, str]] = [row for row in cursor]
    conn.close()
    return chat_messages

def load_state_visibility(execution_id: str, mock: bool = False) -> Dict[str, str]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, visible FROM state_options WHERE thread_id = :thread_id",
                   {"thread_id": execution_id})
    is_visible = {}
    for row in cursor:
        state, visible = row
        is_visible[state] = visible
    conn.close()
    
    return is_visible

def load_message_attributes_visibility(execution_id: str, mock: bool = False) -> Dict[str, str]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, visible FROM message_props_options WHERE thread_id = :thread_id",
                   {"thread_id": execution_id})
    is_visible = {}
    for row in cursor:
        attribute, visible = row
        is_visible[attribute] = visible
    conn.close()
    
    return is_visible

def load_state_snapshots(execution_id: str, mock: bool = False) -> List[str]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute("SELECT snapshot FROM state_output WHERE thread_id = :thread_id ORDER BY execution_step ASC",
                   {"thread_id": execution_id})
    snapshots = []
    for row in cursor:
        json, = row
        snapshots.append(json)
    
    return snapshots

def load_mermaid(execution_id: str, mock: bool = False) -> str:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_MOCK_PATH"] if mock else os.environ["DATABASE_PATH"], 
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute("SELECT mermaid FROM mermaid_views WHERE thread_id = :thread_id",
                   {"thread_id": execution_id})
    mermaid:str = ""
    for row in cursor:
        mermaid_binary, = row
        mermaid_string = mermaid_binary.decode(encoding="utf-8", errors="strict")
        mermaid = mermaid_string 

    conn.close()
    return mermaid
    