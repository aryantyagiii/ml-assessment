import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Load dataset
df = pd.read_csv("games_dataset.csv")

# Combine text
df = pd.read_csv("games_dataset.csv")

# Fill missing values
df = df.fillna("")

# Combine safely
df["text"] = df["name"].astype(str) + " " + \
             df["description"].astype(str) + " " + \
             df["top_comments"].astype(str)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(df["text"].tolist())

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def search(query):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k=3)

    results = df.iloc[indices[0]]
    return results

def generate_pico8_code(context):
    return f"""
-- Pico-8 Game Template
-- Based on dataset context

function _init()
    player_x = 64
    player_y = 64
end

function _update()
    if btn(0) then player_x -= 1 end
    if btn(1) then player_x += 1 end
end

function _draw()
    cls()
    circfill(player_x, player_y, 5, 7)
    print("Inspired by: {context.iloc[0]['name']}", 10, 10, 7)
end
"""

# Query loop
while True:
    q = input("\nAsk game type (or exit): ")
    if q == "exit":
        break

    results = search(q)
    print("\nTop Matches:\n", results[["name", "author"]])

    code = generate_pico8_code(results)
    print("\nGenerated Code:\n", code)