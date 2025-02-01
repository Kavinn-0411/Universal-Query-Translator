from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
openai_llm = OpenAI(
                    model_name="gpt-3.5-turbo-instruct",
                    temperature=0,
                    max_tokens=1800
                )

def llm_model(prompttemplate,dbschema,input):
    input_var=["database_info","user_query"]
    prompt_template=PromptTemplate(template=prompttemplate, input_variables=input_var)
    llm_chain_openai = LLMChain(prompt=prompt_template, llm=openai_llm)
    result=llm_chain_openai.invoke({"database_info":dbschema,"user_query":input})
    return result
