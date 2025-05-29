import re
import jieba
from collections import defaultdict, Counter
from typing import List, Optional, Tuple

def clean_sentence(sentence):
    # 去除网址
    cleaned = re.sub(r'http\S+|www\S+|https\S+', '', sentence)
    # 使用正则表达式匹配合法字符：中英文、数字、空格
    cleaned = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5\s]', ',', cleaned)
    # 可选：去除首尾空白
    cleaned = cleaned.strip()
    return cleaned


def get_cropus(file_path):
    corpus = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            raw_sentence = clean_sentence(line)
            sentence_array = raw_sentence.split(',')
            for sentence in sentence_array:
                if sentence:
                    corpus.append(sentence)
    return corpus


def get_tokens(corpus):
    tokens = []
    for sentence in corpus:
        tokens.extend(jieba.cut(sentence))
    return tokens


class Ngram:
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n must be at least 1")
        self.n = n
        # 使用 prefix -> next_word frequency 的结构
        self.model = defaultdict(Counter)

    def train(self, tokens: List[str]):
        """
        根据 token 序列训练 n-gram 模型
        """
        for i in range(len(tokens) - self.n + 1):
            context = tuple(tokens[i:i + self.n - 1])  # 前 n-1 个词作为上下文
            next_word = tokens[i + self.n - 1]         # 第 n 个词是目标词
            self.model[context][next_word] += 1

    def predict_next_word(self, context: List[str]) -> Optional[str]:
        """
        给定前 n-1 个词，预测下一个最可能的词
        """
        if len(context) < self.n - 1:
            print(f"上下文长度不足，至少需要 {self.n - 1} 个词")
            return None

        context_tuple = tuple(context[-(self.n - 1):])
        if context_tuple not in self.model:
            print("未见过的上下文，无法预测")
            return None

        # 返回频率最高的词
        most_common = self.model[context_tuple].most_common(1)
        return most_common[0][0]

    def get_probability(self, next_word: str, context: List[str]) -> float:
        """
        计算 P(next_word | context)，即给定上下文出现某个词的概率（带拉普拉斯平滑）
        """
        context_tuple = tuple(context[-(self.n - 1):])
        counter = self.model[context_tuple]
        total_count = sum(counter.values())
        word_count = counter.get(next_word, 0)
        vocab_size = len(set(word for c in self.model.values() for word in c.keys()))

        # 拉普拉斯平滑（Add-one smoothing）
        return (word_count + 1) / (total_count + vocab_size + 1e-6)

if __name__ == '__main__':
    corpus = get_cropus('ngram_txt')
    tokens = get_tokens(corpus)
    model = Ngram(2)
    model.train(tokens)
    print(model.predict_next_word(['心理']))
    # print(model.get_probability('两类', ['如何', '选']))