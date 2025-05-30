import re
import jieba

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
                    corpus.append(sentence.lower())
    return corpus

def get_tokens(corpus):
    tokens = []
    for sentence in corpus:
        tokens.extend(jieba.cut(sentence))
    return tokens

def load_stopwords(filepath):
    """
    加载停用词表
    :param filepath: 停用词表文件路径
    :return: 包含所有停用词的集合
    """
    stopwords = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # 移除换行符并加入集合
            stopwords.add(line.strip())
    return stopwords

def remove_stopwords(docs, stopwords):
    """
    对已经分词的文档进行停用词过滤
    :param docs: 已分词的文档列表，如 ['可以', '领取', '舆情宝', '体验']
    :param stopwords: 停用词集合
    :return: 过滤后的 token 列表
    """
    if isinstance(docs[0], list):
        return [[w for w in doc if w not in stopwords] for doc in docs]
    else:
        return [w for w in docs if w not in stopwords]