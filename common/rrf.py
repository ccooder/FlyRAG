#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/8 15:09
from langchain_core.load import loads, dumps

def reciprocal_rank_fusion(results: list[list], k=30):
    fused_scores = {}
    for docs in results:
        # Assumes the docs are returned in sorted order of relevance
        for rank, doc in enumerate(docs):
            print(rank, doc)
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            previous_score = fused_scores[doc_str]
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_results