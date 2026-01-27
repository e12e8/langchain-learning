import sys
sys.path.append(r'C:/Users/赵毅/Desktop/langchain-learning')
from agent_core.tools.knowledge import query_knowledge
if __name__ == '__main__':
    print(query_knowledge('请查询 赵毅第一周的任务'))
