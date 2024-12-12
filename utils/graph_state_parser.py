import json
import pandas as pd
from pydantic import Json
from typing import List, Dict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage

def GraphStateDictParser(states, visible_state_props: List[str], visible_props_in_message: List[str]) -> Dict:
    if "messages" in states:
        parsed_messages = []
        for message in states["messages"]:
            parsed_message = {}
            for property in visible_props_in_message:
                if hasattr(message, property):
                    parsed_message[property] = getattr(message, property)
            parsed_messages.append(parsed_message)
        states["messages"] = parsed_messages
    return dict(filter(lambda dict_item: dict_item[0] in visible_state_props, states.items()))

def GraphStateJsonParser(states, visible_state_props: List[str], visible_props_in_message: List[str]) -> Json:
    states_dict = GraphStateDictParser(
        states=states,
        visible_state_props=visible_state_props,
        visible_props_in_message=visible_props_in_message
    )
    states_json = json.dumps(states_dict, ensure_ascii=False, indent=2)
    return states_json

def GraphStateDataFrameParser(states, visible_state_props: List[str], visible_props_in_message: List[str]):
    states_dict = GraphStateDictParser(
        states=states,
        visible_state_props=visible_state_props,
        visible_props_in_message=visible_props_in_message
    )
    df = pd.DataFrame(states_dict.values(), index=states_dict.keys()).T
    return df