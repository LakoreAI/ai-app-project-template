from openai import OpenAIError

from src.services.chat import ChatService


class FakeLLM:
    def __init__(self, error=None):
        self.error = error
        self.messages = None

    def complete(self, messages):
        if self.error:
            raise self.error
        self.messages = messages
        return "hi"


def use_llm(client, llm):
    client.app.state.chat = ChatService(llm=llm)


def test_chat_ok(client):
    llm = FakeLLM()
    use_llm(client, llm)
    r = client.post("/chat", json={"prompt": "hello"})
    assert r.status_code == 200
    assert r.json() == {"answer": "hi"}
    assert llm.messages[-1] == {"role": "user", "content": "hello"}


def test_chat_with_skill_uses_skill_prompt(client):
    llm = FakeLLM()
    use_llm(client, llm)
    client.post("/chat", json={"prompt": "x", "skill": "summarize"})
    assert "Summarize" in llm.messages[0]["content"]


def test_chat_unknown_skill_is_404(client):
    use_llm(client, FakeLLM())
    assert client.post("/chat", json={"prompt": "x", "skill": "nope"}).status_code == 404


def test_chat_provider_error_is_502(client):
    use_llm(client, FakeLLM(error=OpenAIError("bad key")))
    assert client.post("/chat", json={"prompt": "x"}).status_code == 502
