from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

template = """Answer the following question as best as you can:
Question: {query}
Answer:"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

chain = prompt | llm

def get_answer(query):
    result = chain.run(query=query)
    return result.strip()