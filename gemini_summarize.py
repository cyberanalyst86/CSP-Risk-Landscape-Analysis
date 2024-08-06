#Import dependencies
#---------------------------------------------------------------
import os
import io

from langchain import PromptTemplate
#from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain_google_genai import ChatGoogleGenerativeAI

#Get credentials
#---------------------------------------------------------------
GEMINI_API_KEY = "AIzaSyCMYaDZ49J5UMYYXmrihGn9Sjc8iTOFF1U"
#AIzaSyCMYaDZ49J5UMYYXmrihGn9Sjc8iTOFF1U
#AIzaSyAbIgixv5mecc9dMhf7-_Z6ciNGIiWdUmk
os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY


def write_docs_to_file(docs):

  filename = "docs.txt"
  text_to_append = str(docs)

  try:
    with open(filename, "a") as file:
      print(text_to_append, file=file)
    print(f"Text successfully appended to {filename}")
  except FileNotFoundError:
    print(f"File {filename} not found.")
  except PermissionError:
    print(f"You don't have permission to write to {filename}.")

  return


#---------------------------------------------------------------
def get_article_text(url):

  loader = WebBaseLoader(url)

  docs = loader.load()

  #print(docs)

  return docs

#---------------------------------------------------------------
def configure_model(mod, tempt, topp):

  llm = ChatGoogleGenerativeAI(model=mod, temperature=tempt, top_p=topp)

  return llm

#---------------------------------------------------------------
def execute_prompt(llm_prompt_template):

  # To extract data from WebBaseLoader
  doc_prompt = PromptTemplate.from_template("{page_content}")

  # To query Gemini
  llm_prompt = PromptTemplate.from_template(llm_prompt_template)

  return doc_prompt, llm_prompt

#---------------------------------------------------------------
def create_chain(llm, llm_prompt, doc_prompt, docs):

  stuff_chain = (
    # Extract data from the documents and add to the key `text`.
    {
        "text": lambda docs: "\n\n".join(
            format_document(doc, doc_prompt) for doc in docs
        )
    }
    | llm_prompt         # Prompt for Gemini
    | llm                # Gemini function
    | StrOutputParser()  # output parser
  )

  return stuff_chain

#---------------------------------------------------------------

def gemini_process(article_url, llm_prompt_template):

  mod="gemini-pro"
  tempt=0.7
  topp=0.85

  docs = get_article_text(article_url)

  #write_docs_to_file(docs)

  llm = configure_model(mod, tempt, topp)
  doc_prompt, llm_prompt = execute_prompt(llm_prompt_template)
  create_chain(llm, llm_prompt, doc_prompt, docs)
  stuff_chain = create_chain(llm, llm_prompt, doc_prompt, docs)

  stuff_chain.invoke(docs)

  return str(stuff_chain.invoke(docs))

def gemini_data_collection(article_url):

  llm_prompt_template = """for the following article, help me try to gather the information and put them into json with these keys "affected country", "affected organization", "affected industry", "attack type", "attacker", "attacker country", "attacker type", "attacker motivation", "impact of the cyber incident", "impacted system", "lesson learn", "mitigation" : 
  "{text}"
  JSON:"""

  jsonString = gemini_process(article_url, llm_prompt_template)


  return jsonString


def gemini_summarize(article_url):

  llm_prompt_template = """for the following article, help me to summarize to point form : 
  "{text}"
  SUMMARY:"""

  summary = gemini_process(article_url, llm_prompt_template)


  return summary