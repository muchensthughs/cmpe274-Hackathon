from utils import load_credentials
import PyPDF2
import os
import langchain
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
# from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain

class file_reader():
    def __init__(self, file_path):
        load_credentials()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.file = file_path
        self.load_file()
        self.setup_retriever()
        self.set_qa_interface()


    def chat_completion(self, prompt, model="gpt-3.5-turbo", temperature=0):
        res = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return res.choices[0].message.content
    
    def load_file(self):
        pdf_file = open(self.file, 'rb')

        # Create a PDF object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize a variable to store the text from the PDF
        self.detected_text = ''

        # Loop through all the pages and extract text
        for page_num in range(len(pdf_reader.pages)):
            # print(page_num)
            page = pdf_reader.pages[page_num]
            # print(page.extract_text())
            self.detected_text += page.extract_text() + '\n\n'

        # Close the PDF file
        print("File Loaded: " + self.file)
        pdf_file.close()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([self.detected_text]) 
        self.directory = 'index_store' + os.path.basename(self.file).replace(".", "_")
        vector_index = FAISS.from_documents(texts, OpenAIEmbeddings())
        vector_index.save_local(self.directory)   
        
    def setup_retriever(self):
        vector_index = FAISS.load_local(self.directory, OpenAIEmbeddings())
        self.retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k":6})
        print("Retriver setup finished")
        # qa_interface = RetrievalQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)

    def set_qa_interface(self):
        self.qa_interface = RetrievalQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", retriever=self.retriever, return_source_documents=True)

    def ask_doc(self, prompt):
        res = self.qa_interface(prompt)
        return res["result"]
