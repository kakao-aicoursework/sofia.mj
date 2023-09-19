import pynecone as pc
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from langchain.prompts.chat import ChatPromptTemplate

import os

os.environ["OPENAI_API_KEY"] = "에이피아이키"


def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template


chat = ChatOpenAI(temperature=0.8)
system_message = "assistant는 카카오 싱크를 설명해주는 봇이다. user의 내용을 참고하여 사용법을 작성하라"
system_message_prompt = SystemMessage(content=system_message)

# documents = read_prompt_template('/tmp/datas/project_data_카카오싱크.txt')
human_template = (
    "유저의 질문은 다음과 같습니다 {user_question}\n"
    "아래는 카카오싱크의 설명입니다 \n"
    "{documents}\n"
    "사용법을 목차로 요약해"
)

message_prompt = HumanMessagePromptTemplate.from_template(human_template)
# chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
# chain = LLMChain(llm=chat, prompt=chat_prompt)


class State(pc.State):
    """The app state."""

    user_question: str = ""
    content: str = ""
    is_working: bool = False

    async def handle_submit(self, form_data):
        self.is_working = True
        # "카카오싱크 기능이 무엇이 있는지 설명해주세요"
        self.user_question = form_data["user_question"]
        self.documents = read_prompt_template("../tmp/datas/project_data_카카오싱크.txt")

        human_message_prompt = message_prompt.format(
            user_question=self.user_question, documents=self.documents
        )

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt, output_key="output")
        result = chain(dict())

        self.content = "\n".join([result["output"]])

        self.is_working = False


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.form(
                pc.vstack(
                    pc.heading("카카오 싱크를 설명해주는 챗봇입니다", font_size="2em"),
                    pc.text("유저의 질문"),
                    pc.input(placeholder="유저의 질문", id="user_question"),
                    pc.button("Submit", type_="submit"),
                ),
                on_submit=State.handle_submit,
                width="100%",
            ),
            pc.cond(
                State.is_working,
                pc.spinner(
                    color="lightgreen",
                    thickness=5,
                    speed="1.5s",
                    size="xl",
                ),
            ),
            pc.box(pc.markdown(State.content)),
            spacing="1em",
            font_size="1em",
            width="80%",
            padding_top="10%",
        )
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
