import arxiv
import time
import requests
import PyPDF2
import io
import logging
from features.llm import LLM

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

llm_agent=LLM()

def search_arxiv(query, num_results):
    print(f"\nSearching arXiv for '{query}' with {num_results} results...\n")
    search = arxiv.Search(
        query=query,
        max_results=num_results * 3,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    initial_results = []
    times_taken = []
    
    print("Fetching results from arXiv...")
    for i, result in enumerate(search.results(), start=1):
        start_time = time.time()
        print(f"Processing paper {i}: {result.title}")
        
        full_text = download_full_text(result.pdf_url)
        end_time = time.time()

        if full_text is None:
            print(f"Skipping {result.title} due to download or extraction error.\n")
            continue

        retrieval_time = end_time - start_time
        times_taken.append(retrieval_time)
        print(f"Time taken for document {i}: {retrieval_time:.2f} seconds\n")

        paper = {
            'title': result.title,
            'authors': ', '.join([author.name for author in result.authors]),
            'abstract': result.summary,
            'pdf_url': result.pdf_url,
            'full_text': full_text,
            'year': str(result.published.year)
        }
        initial_results.append(paper)

        if len(initial_results) >= num_results * 3:
            break

    print(f"Initial pool of {len(initial_results)} documents fetched.\n")

    if times_taken:
        avg_retrieval_time = sum(times_taken) / len(times_taken)
        print(f"Average time to retrieve each document: {avg_retrieval_time:.2f} seconds\n")
    else:
        print("No documents were retrieved successfully.\n")

    print(f"Ranking and selecting the top {num_results} most relevant documents...")
    top_documents = llm_agent.get_top_n_relevant_documents(query, initial_results, n=num_results)

    output_file = "full_text.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for i, doc in enumerate(top_documents, start=1):
            f.write(f"Document {i}\n")
            f.write(f"Title: {doc['title']}\n")
            f.write(f"Authors: {doc['authors']}\n")
            f.write(f"Abstract: {doc['abstract']}\n\n")
    
    print(f"Final {num_results} documents written to '{output_file}'.\n")
    return top_documents

def download_full_text(pdf_url):
    try:
        print(f"Downloading PDF from: {pdf_url}")
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        print("Extracting text from PDF...")
        pdf_content = response.content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        full_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text() or ""
        
        print("Text extraction successful.\n")
        return full_text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}\n")
        return None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}\n")
        return None