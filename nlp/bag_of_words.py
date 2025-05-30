import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from tools import get_cropus, get_tokens, load_stopwords, remove_stopwords
from collections import Counter
from typing import List
import numpy as np

def create_vocabulary(dataset_dir) -> List[str]:
    """
    根据 token 序列创建词汇表
    """
    vocabulary = []
    for file_path in dataset_dir:
        corpus = get_cropus(file_path)
        tokens = get_tokens(corpus)
        vocabulary.extend(tokens)
    print("词汇表大小:", len(set(vocabulary)))
    return sorted(set(vocabulary))



class BagOfWords:
    def __init__(self, stopwords=None):
        self.vocab = None  # 词汇表
        self.tf = None     # 词频矩阵 (N, V)
        self.idf = None    # IDF 向量 (V,)
        self.tfidf = None  # TF-IDF 矩阵 (N, V)
        self.stopwords = stopwords

    def train(self, docs, vocab):
        """
        训练 TF-IDF 模型
        :param docs: 已分词的文档列表，如 [["word1", "word2"], ...]
        :param vocab: 词汇表，如 ["word1", "word2", ...]
        :return: 返回 TF-IDF 矩阵 (N, V)
        """
        if self.stopwords:
            docs = remove_stopwords(docs, self.stopwords)

        N = len(docs)
        V = len(vocab)
        self.vocab = vocab

        # 初始化 TF 矩阵和 doc_freq
        self.tf = np.zeros((N, V))
        doc_freq = np.zeros(V)

        # 构建 TF 并统计每个词出现在多少篇文档中
        print("开始训练 TF-IDF 模型...")
        for i in range(N):
            word_counts = Counter(docs[i])
            for j, word in enumerate(vocab):
                count = word_counts.get(word, 0)
                self.tf[i, j] = count
                if count > 0:
                    doc_freq[j] += 1

        # 计算 IDF（带平滑）
        self.idf = np.log((N + 1) / (1 + doc_freq)) + 1e-8  # 防止除零并微调
        # 计算 TF-IDF（向量化运算）
        self.tfidf = self.tf * self.idf
        return self.tfidf

    def extract_keywords(self, doc_index, top_k=5):
        """
        从训练好的模型中提取某篇文档的关键词
        :param doc_index: 文档索引
        :param top_k: 关键词数量
        :return: 排序后的关键词列表
        """
        if self.tfidf is None:
            raise ValueError("请先调用 train() 方法训练模型")

        if doc_index >= self.tfidf.shape[0]:
            raise IndexError("doc_index 超出范围")

        # 获取该文档的 TF-IDF 向量
        doc_tfidf = self.tfidf[doc_index]

        # 获取排序后的词索引（按 TF-IDF 降序）
        top_indices = np.argsort(doc_tfidf)[-top_k:][::-1]

        # 映射成实际词语
        keywords = [self.vocab[i] for i in top_indices]
        return keywords
        

if __name__ == "__main__":
    dataset_dir = [
        "dataset/1",
    ]
    corpus = get_cropus(dataset_dir[0])
    tokens = get_tokens(corpus)
    vocab = create_vocabulary(dataset_dir)
    stopwords = load_stopwords("stopwords")
    bow = BagOfWords(stopwords)
    bow.train(tokens, vocab)
    print(bow.extract_keywords(0))