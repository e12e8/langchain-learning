import os
# 修改后的导入路径
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 1. 加载文档 (第一周的产出)
file_path = "赵毅的学习计划.txt"
if not os.path.exists(file_path):
    # 兼容性处理：如果找不到中文名，尝试找 my_notes.txt
    file_path = "my_notes.txt"

loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

# 2. 文本切分 (Chunking) - 第 1 周核心技能
# 将长文档切分成 300 字的小块，方便精准检索
# 使用更智能的递归切分器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", " ", ""]
)
docs = text_splitter.split_documents(documents)

# 3. 初始化 Embedding 模型 (使用 HuggingFace 本地模型)
# 第一次运行会自动下载模型（约 80MB），请保持网络畅通
print("正在初始化 Embedding 模型，请稍候...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. 存入昨天用 Docker 部署好的 Milvus
print("正在连接 Milvus 并存入数据...")
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
    collection_name="zhaoyi_learning_plan",
    drop_old=True  # 调试阶段：每次运行都会清空旧数据重新导入
)

print(f"✅ 成功！已将 {len(docs)} 条知识切片存入 Milvus 向量库。")
