from dotenv import load_dotenv
import os

from langchain import text_splitter

load_dotenv()
from consts import INDEX_NAME
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from firecrawl import FirecrawlApp
from langchain.schema import Document

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs2() -> None:
    app = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])

    # Lista de URLs que deseas procesar
    urls = [
        #"https://www.usa.gov/job-discrimination-harassment",
       # "https://www.eeoc.gov/laws/guidance/enforcement-guidance-harassment-workplace",  # Agrega más URLs aquí
      #  "https://www.ilo.org/media/406901/download",
        "https://normlex.ilo.org/dyn/normlex/en/f?p=NORMLEXPUB:12100:0::NO::P12100_ILO_CODE:C190",
        # ... añade más URLs según sea necesario
    ]

    all_docs = []  # Lista para almacenar todos los documentos generados

    for url in urls:
        page_content = app.scrape_url(url=url, params={"onlyMainContent": True})
        print(f"Scraped content from {url}")

        # Crea el documento
        doc = Document(page_content=str(page_content), metadata={"source": url})

        # Divide el documento en fragmentos
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        docs = text_splitter.split_documents([doc])

        all_docs.extend(docs)  # Agrega los documentos a la lista general

    # Almacena todos los documentos en Pinecone
    PineconeVectorStore.from_documents(
        all_docs, embeddings, index_name="kim-index"
    )


if __name__ == "__main__":
    ingest_docs2()
