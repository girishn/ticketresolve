from __future__ import annotations

from .config import load_config
from .embeddings import embed_texts
from .s3vectors_client import put_vectors


def main() -> None:
    cfg = load_config()

    # Simple sample texts – one could represent a doc, the other a past ticket.
    texts = [
        "How do I reset my account password when I have lost access to my email?",
        "Customer reports 500 error when submitting a support ticket via the web form.",
    ]

    print("Embedding sample texts with Bedrock...")
    embeddings = embed_texts(cfg, texts)

    vectors = []
    for i, (text, emb) in enumerate(zip(texts, embeddings), start=1):
        key = f"sample-{i}"
        metadata = {
            "source": "sample",
            "text": text[:200],  # truncate long text for metadata
        }
        vectors.append((key, emb, metadata))

    print(f"Writing {len(vectors)} vectors to S3 Vectors index '{cfg.vector_index_name}'...")
    put_vectors(cfg, vectors)
    print("Done.")


if __name__ == "__main__":
    main()
