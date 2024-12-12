import streamlit as st

st.header(':closed_book: Document')
overview = st.container()
detail = st.container()
licence = st.container()

with overview:
    st.subheader(':thumbsup: Overview')
    st.markdown("""Simple Langgraph Tracer is mini tool for developer and langgraph beginner.

You can trace state transition of each step and demonstrate your workflow in form of stream supported chat interface.""")
    st.markdown("""#### Usage""")
    st.markdown("""See repo.""")
    st.link_button("Go to Repo", "https://google.com", icon=':material/code:')
    st.markdown("""- **Summary**: You modify `settings.py` to register

1. Your graph builder (not compiled graph).

2. Class which define your graph state.""")
    
    st.markdown("""#### About sample workflow""")
    st.markdown("""I chose Reflexion as sample workflow.
Reflexion by Shinn, et. al.,is one of first introduced by LangChain team as example of langgraph practical use case.
In Reflexion flow, LLM improves own response by self-reflect method which needs external info (tool calling), but more controllable than naive ReAct Agent.""")
    st.image(
        './assets/images/reflexion.png',
        width=800,
        caption="Source: https://blog.langchain.dev/reflection-agents/"
    )

    """- LangChain team blog: [Reflection Agents](https://blog.langchain.dev/reflection-agents/)
- Source code: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb)
    """
with detail:
    raw_llm_output="""{"generations": [[{"text": "I'm called Assistant. How can I help you today?","generation_info": {"finish_reason": "stop","logprobs": null},"type": "ChatGeneration","message": {"lc": 1,"type": "constructor","id": ["langchain","schema","messages","AIMessage"],"kwargs": {"content": "I'm called Assistant. How can I help you today?","additional_kwargs": {"refusal": null},"response_metadata": {"token_usage": {"completion_tokens": 12,"prompt_tokens": 22,"total_tokens": 34,"completion_tokens_details": {"accepted_prediction_tokens": 0,"audio_tokens": 0,"reasoning_tokens": 0,"rejected_prediction_tokens": 0},"prompt_tokens_details": {"audio_tokens": 0,"cached_tokens": 0}},"model_name": "gpt-4o-mini-2024-07-18","system_fingerprint": "fp_bba3c8e70b","finish_reason": "stop","logprobs": null},"type": "ai","id": "run-660a9847-1706-45bd-b3dd-bdc03ae1514b-0","usage_metadata": {"input_tokens": 22,"output_tokens": 12,"total_tokens": 34,"input_token_details": {"audio": 0,"cache_read": 0},"output_token_details": {"audio": 0,"reasoning": 0}},"tool_calls": [],"invalid_tool_calls": []}}}]],"llm_output": {"token_usage": {"completion_tokens": 12,"prompt_tokens": 22,"total_tokens": 34,"completion_tokens_details": {"accepted_prediction_tokens": 0,"audio_tokens": 0,"reasoning_tokens": 0,"rejected_prediction_tokens": 0},"prompt_tokens_details": {"audio_tokens": 0,"cached_tokens": 0}},"model_name": "gpt-4o-mini-2024-07-18","system_fingerprint": "fp_bba3c8e70b"},"run": null,"type": "LLMResult"}"""
    parsed_json="""{"messages":[{"content":"what is your name?","type":"human"},{"content":"I’m called Assistant. How can I help you today?","type":"ai"}],"query":"what is your name?"}"""
    important_part_of_raw_output="""{"kwargs": {"content": "I'm called Assistant. How can I help you today","additional_kwargs": {"refusal": null},"response_metadata": {"token_usage": {"completion_tokens": 12,"prompt_tokens": 22,"total_tokens": 34,"completion_tokens_details": {"accepted_prediction_tokens": 0,"audio_tokens": 0,"reasoning_tokens": 0,"rejected_prediction_tokens": 0},"prompt_tokens_details": {"audio_tokens": 0,"cached_tokens": 0}},"model_name": "gpt-4o-mini-2024-07-18","system_fingerprint": "fp_bba3c8e70b","finish_reason": "stop","logprobs": null},"type": "ai","id": "run-660a9847-1706-45bd-b3dd-bdc03ae1514b-0","usage_metadata": {"input_tokens": 22,"output_tokens": 12,"total_tokens": 34,"input_token_details": {"audio": 0,"cache_read": 0},"output_token_details": {"audio": 0,"reasoning": 0}},"tool_calls": [],"invalid_tool_calls": []}}""" 

    st.subheader(":pencil: Specification Details")
    st.markdown("""#### What is attibutes setting?""")
    st.image('./assets/images/attribute_setting.png')
    st.markdown("""
        Chat messages given to LLM and it's response are any instance of `HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage` which are subclass of
        [BaseMessage](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.base.BaseMessage.html#basemessage) Class.
        When you build complex workflow with Langgraph, you will need to see attibutes of these message interface especially multi Agent system or advanced RAG flow
        so that you can make sure messages conveyed from upstream node to another has intented form.
        
        The original structure of these message interface is somewhat complex like deep nested json, so I parsed it and converted it to relatively simple json output.
        In many cases, at least as of now, you will manipulate values tied to `generations.message.kwargs` key of raw LLM output.
        So I simply output only that values.
    """)
    st.markdown("""
                **Example**: As in the image at the beginning of this chapter, you did select `content` and `type` (default setting I made).
                
                - **Raw response to query, *What is your name?*, is below:**
                """)
    st.json(raw_llm_output, expanded=2)
    st.markdown("""
                - **Parsed output json**
                """)
    st.json(parsed_json)
    
    st.markdown("""
        When you choose `content` and `type` attributes,
        that means **you fetch 2 values tied to `content` property and `type` property
        from object below:**
    """)
    st.json(important_part_of_raw_output, expanded=2)

    st.markdown("""#### Langgraph Checkpoint is persist in here.""")
    
    checkpoints_location="""simple_langgraph_tracer/
└── db/
    └── sqlite/
        └── langgraph_tracer.sqlite"""
    
    st.code(checkpoints_location, None)
    st.markdown("""You can trace your state in `Traces` Page.
Besides, execution checkpoints are automatically saved in `checkpoints` table in `langgraph_tracer.sqlite` SQLite database.
You can use it to resume execution from any checkpoint at graph in your own program.
    
- See official guide: [Checkpointing](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpoints)
                """)
    

with licence:
    st.subheader(":hatching_chick: Apache 2.0 Licence")
    st.write("""Copyright 2024 NAVIFOLIO

Licensed under the Apache License, Version 2.0 (the “License”);

You may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.")""")