from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model_name="cyou-api",
    openai_api_base="http://127.0.0.1:20000/v1",
    openai_api_key="empty"
)

res = model.invoke("你是谁")
print(res)
