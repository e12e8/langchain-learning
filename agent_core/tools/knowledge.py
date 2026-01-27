import os
import jieba
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from sentence_transformers import CrossEncoder # 引入交叉编码器做重排

def query_knowledge(query: str):
    # 1. 向量检索 (粗排：捞出 10 条)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Milvus(
        embedding_function=embeddings,
        connection_args={"host": "127.0.0.1", "port": "19530"},
        collection_name="zhaoyi_learning_plan",
    )
    docs = vector_db.similarity_search(query, k=10) # 这里的 k 设大一点

    # 2. 准备重排模型 (Cross-Encoder)
    # BGE-Reranker 是目前中文领域非常强力的轻量级重排模型
    reranker = CrossEncoder('BAAI/bge-reranker-base')

    # 3. 计算相关性评分
    # 将问题和每一个搜出来的文档配对，让模型打分
    pairs = [[query, doc.page_content] for doc in docs]
    scores = reranker.predict(pairs)

    # 4. 根据分数排序并取 Top 3
    # 将文档和分数组合，按分数从高到低排列
    scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_3_docs = [doc.page_content for doc, score in scored_docs[:3]]

    context = "\n---\n".join(top_3_docs)
    return {"ok": True, "result": context}