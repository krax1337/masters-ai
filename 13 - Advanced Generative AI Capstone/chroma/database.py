import chromadb
from chromadb.utils import embedding_functions
import logging
import sys
import time
import os
from PyPDF2 import PdfReader
from typing import List, Dict

class ChromaPDFKnowledgeBase:
    def __init__(self, db_path: str = "chroma_database", collection_name: str = "car_manuals"):
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='[%(levelname)s - %(asctime)s] %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=db_path, 
            settings=chromadb.Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding function
        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.sentence_transformer_ef
        )

    def process_pdf(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
        self.logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract the manual name from the file path
        manual_name = os.path.basename(pdf_path)
        
        # Load PDF
        reader = PdfReader(pdf_path)
        chunks = []
        
        # Process each page
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            page_num = i + 1
            
            # Skip empty pages
            if not text.strip():
                continue
                
            # Create chunks for long pages
            if len(text) <= chunk_size:
                chunks.append({
                    "text": text,
                    "page": page_num,
                    "source": manual_name
                })
            else:
                # Split into overlapping chunks
                for j in range(0, len(text), chunk_size - chunk_overlap):
                    chunk = text[j:j + chunk_size]
                    if chunk.strip():  # Skip empty chunks
                        chunks.append({
                            "text": chunk,
                            "page": page_num,
                            "source": manual_name
                        })
        
        self.logger.info(f"Created {len(chunks)} chunks from {pdf_path}")
        return chunks
    
    def add_pdf_to_knowledge_base(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        chunks = self.process_pdf(pdf_path, chunk_size, chunk_overlap)
        
        # Add chunks to the collection
        self.collection.add(
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[{
                "page": chunk["page"], 
                "source": chunk["source"]
            } for chunk in chunks],
            ids=[f"{os.path.basename(pdf_path)}_{i}" for i in range(len(chunks))]
        )
        
        self.logger.info(f"Added {len(chunks)} chunks from {pdf_path} to knowledge base")
    
    def add_multiple_pdfs(self, pdf_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        if len(self.collection.get()['ids']) == 0:
            for filename in os.listdir(pdf_dir):
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(pdf_dir, filename)
                    self.add_pdf_to_knowledge_base(pdf_path, chunk_size, chunk_overlap)
        
            self.logger.info(f"Finished processing all PDFs in {pdf_dir}")
        else:
            self.logger.info("Using existing database")
        

    
    def search_knowledge(self, query: str, n_results: int = 3):
        self.logger.info(f"Searching for '{query}'")
        start_time = time.time()
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas"]
        )
        
        self.logger.info(f"Search took {time.time() - start_time:.2f} seconds")
        
        # Format results for easier consumption
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "page": results["metadatas"][0][i]["page"],
                "source": results["metadatas"][0][i]["source"]
            })
        print(formatted_results)
        return formatted_results

# Example usage
if __name__ == "__main__":
    PDF_DIR = "pdf/"
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s - %(asctime)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    kb = ChromaPDFKnowledgeBase()
    kb.add_multiple_pdfs(PDF_DIR)
    
    # Example search
    results = kb.search_knowledge("How do I adjust the headlights in Tahoe?")
    print(f"Found {len(results)} results:")
    
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Source: {result['source']} (Page {result['page']})")
        print(f"Text: {result['text'][:150]}...")