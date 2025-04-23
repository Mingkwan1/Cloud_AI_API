from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = """Answer the following question as best as you can:
Question: {query}
Answer:"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

chain = LLMChain(llm=llm, prompt=prompt)

def get_answer(query):
    result = chain.run(query=query)
    return result.strip()