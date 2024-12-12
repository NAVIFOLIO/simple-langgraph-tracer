# :dog2: Simple LangGraph Tracer

Simple LangGraph Tracer is mini tool for developers and LangGraph beginners.

LangGraph is well implemented library enables us to build production ready LLM-powered applications by its robust features.
But due to somewhat complex structure of LLM output, some people feel hard when their first build or attempt to build like:

[Mistral AI Cookbook](https://github.com/mistralai/cookbook/tree/main/third_party/langchain)

Simple LangGraph Tracer enables you to: 

1. See your graph state in much simpler form than [LangGraph Studio](https://studio.langchain.com/) or [LangSmith](https://www.langchain.com/langsmith).
2. Try your workflow immediately in mocked Chat Interface. The interface supports streaming output.
3. Store your graph execution data automatically in local database. 

You can also see details in `Document` Page of streamlit frontend.

## :pencil2: Usage

1. Install dependencies to your environment.

```
pip install -r requirements.txt
```

2. Run Streamlit application. Entrypoint is `ChatInterface.py`

```
streamlit run ChatInterface.py
```

- [Basic Concepts of Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts)

3. Access to your app. Default streamlit port is `8501`.

## :snake: Dependencies

Please refer to `requirements.txt`.

## :rocket: Supplement: What is LangGraph?

LangGraph is an library in langchain ecosystem to build LLM-Powered workflows composed of "multiple" node in which langchain works, that enabled us to construct "pipelined" workflow by Agents, RAGs and other chains.

LangGraph regards workflow as state machine and trace its state transition, including "state streaming".

You can create more controllable system than single [ReAct Agent](https://arxiv.org/abs/2210.03629) by Shunyu Yao, et. al., by LangGraph, which is very important thing for production ready application.

- [LangGraph Start Guide](https://langchain-ai.github.io/langgraph/tutorials/introduction/)