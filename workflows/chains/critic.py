import datetime
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from workflows.schemas import critique_parser
load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "human",
            """You are export researcher.
Current time: {time}

user's question: {query}
first answer: {answer}

1. Critique [first answer]. Be severe to maximize improvement.
2. Point out missing and superflous information of [first answer].
3. Output your reflection in given format.

{format_instructions}

YOUR RESPONSE:
""",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
    format_instructions=critique_parser.get_format_instructions() 
)

critic_chain: RunnableSequence = prompt | chat | critique_parser