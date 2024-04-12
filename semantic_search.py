"""
This script performs semantic search using a combination of Universal Sentence Encoder (USE) and BERT embeddings.

Dependencies:
    - TensorFlow (https://www.tensorflow.org/)
    - TensorFlow Hub (https://www.tensorflow.org/hub)
    - Hugging Face Transformers (https://huggingface.co/transformers)
    - NumPy (https://numpy.org/)
    - PyTorch (https://pytorch.org/)

Usage:
    - Ensure the required dependencies are installed.
    - Prepare a JSON file containing data with titles.
    - Update the `json_file_path` variable with the path to your JSON file.
    - Run the script and enter a query when prompted.

"""

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from transformers import BertTokenizer, BertModel
import json
import torch

# Load Universal Sentence Encoder
embed_use = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

# Load pre-trained BERT model and tokenizer
tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
model_bert = BertModel.from_pretrained('bert-base-uncased')

# Specify the path to your JSON file
json_file_path = '/content/sample_data/data.json'

# Open the JSON file and load its contents using UTF-8 encoding
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Extract titles and corresponding indices from the JSON object
titles = [entry["title"] for entry in data]

# Encode titles using BERT tokenizer and get embeddings
encoded_titles_bert = tokenizer_bert(titles, padding=True, truncation=True, return_tensors='pt')
with torch.no_grad():
    output_bert = model_bert(**encoded_titles_bert)
title_embeddings_bert = output_bert.last_hidden_state[:, 0, :].numpy()

# Encode titles into embeddings using Universal Sentence Encoder
title_embeddings_use = embed_use(titles)

def jaccard_similarity(a, b):
    """
    Calculate Jaccard similarity between two sets.

    Args:
        a (set): Set A.
        b (set): Set B.

    Returns:
        float: Jaccard similarity coefficient.
    """
    intersection = len(set(a).intersection(set(b)))
    union = len(set(a).union(set(b)))
    return intersection / union if union != 0 else 0

def semantic_search_combined(query, titles, title_embeddings_use, title_embeddings_bert, data, top_n=15, similarity_threshold_use=0.1, similarity_threshold_bert=0.1):
    """
    Perform semantic search combining Universal Sentence Encoder and BERT embeddings.

    Args:
        query (str): The query string for semantic search.
        titles (list): List of titles.
        title_embeddings_use (numpy.ndarray): Embeddings of titles using Universal Sentence Encoder.
        title_embeddings_bert (numpy.ndarray): Embeddings of titles using BERT.
        data (list): List of JSON objects containing data.
        top_n (int, optional): Number of top results to return. Defaults to 15.
        similarity_threshold_use (float, optional): Similarity threshold for Universal Sentence Encoder. Defaults to 0.1.
        similarity_threshold_bert (float, optional): Similarity threshold for BERT. Defaults to 0.1.

    Returns:
        list: List of JSON objects containing top entries.
    """
    # Split query into words
    query_words = set(query.lower().split())

    # Calculate Jaccard similarity between query and titles
    similarities_jaccard = [jaccard_similarity(query_words, set(title.lower().split())) for title in titles]

    # Initialize lists to store semantic and non-semantic matches
    semantic_matches = []
    non_semantic_matches = []

    # Sort titles based on Jaccard similarity
    for title, similarity in zip(titles, similarities_jaccard):
        if similarity > 0:
            non_semantic_matches.append((title, similarity))
        else:
            semantic_matches.append((title, 0))  # Initialize with 0 similarity for semantic matches

    # Sort non-semantic matches by similarity
    non_semantic_matches.sort(key=lambda x: x[1], reverse=True)

    # Filter out semantic matches that are already in non-semantic matches
    semantic_matches = [(title, similarity) for title, similarity in semantic_matches if title not in [t[0] for t in non_semantic_matches]]

    # Encode query using Universal Sentence Encoder
    query_embedding_use = embed_use([query])[0]

    # Calculate cosine similarity between query and titles using Universal Sentence Encoder
    similarities_use = [np.inner(query_embedding_use, emb) for emb in title_embeddings_use]

    # Filter titles with similarity above threshold for Universal Sentence Encoder
    semantic_matches.extend([(titles[i], similarity) for i, similarity in enumerate(similarities_use) if similarity > similarity_threshold_use])

    # Sort semantic matches by similarity
    semantic_matches.sort(key=lambda x: x[1], reverse=True)

    # Merge non-semantic and semantic matches
    merged_results = non_semantic_matches + semantic_matches

    # Initialize set to store seen titles
    seen_titles = set()

    # Get top similar titles, ignoring duplicates
    top_titles = []
    for title, score in merged_results:
        if title not in seen_titles:
            top_titles.append(title)
            seen_titles.add(title)
            if len(top_titles) >= top_n:
                break

    # Collect entire entries for top titles
    top_entries = [entry for entry in data if entry["title"] in top_titles]

    return top_entries

# Example usage with user input
if __name__ == "__main__":
    user_query = input("Enter your query: ")
    top_entries_combined = semantic_search_combined(user_query, titles, title_embeddings_use, title_embeddings_bert, data)

    print("Top Entries:")
    for entry in top_entries_combined:
        print(f"Title: {entry['title']}")
        print(f"Month: {entry['month']}")
        print(f"Page: {entry['page']}" )
        print()  # Empty line for readability between entries
