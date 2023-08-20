import requests
import tiktoken
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.mapreduce import MapReduceChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

def html_to_text(url):
    r = requests.get(url)
    return r.text

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def clean_text(text):
    return BeautifulSoup(text, "lxml").text

def split_text(text):

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
    )

    return text_splitter.split_text(text)

def generate_summary(openai_api_key,url):
    # Instantiate the LLM model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    text = clean_text(html_to_text(url))

    texts = split_text(text)

    docs = [Document(page_content=t) for t in texts]

    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)