from collections import Counter
from itertools import combinations, dropwhile
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from typing import List, Dict
import unicodedata


def preprocess_texts(text:str,
                     split_sentence_word:str = '。') -> str:

    replaced_text = unicodedata.normalize("NFKC", text)
    replaced_text = replaced_text.upper()
    replaced_text = re.sub(r'[\r\n]', '', replaced_text)  # 改行
    replaced_text = re.sub(r'\u3000', ' ', replaced_text) # 全角コード
    replaced_text = re.sub(r'\u200b', ' ', replaced_text) # 半角コード
    replaced_text = re.sub(r'\、', ' ', replaced_text)    # 句読点除去
    replaced_text = re.sub(r'\, ', ' ', replaced_text)    # 句読点除去
    # 記号の除去
    replaced_text = re.sub("[^0-9a-zA-Zぁ-んーァ-ンヴー@＠.,。、']",  ' ' ,replaced_text)
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text) # メンション除去
    # 数字を除去
    replaced_text = re.sub(r'\d+\.*\d*', '', replaced_text)
    # # split用
    replaced_text = re.sub(r'\.', split_sentence_word, replaced_text)

    return replaced_text

def text_split2words(sentence:str,
                     split_word:str = ' ',
                     split_sentence_word:str = '。',
                     stopwords:List[str]     = [],) -> List[str]:
    words = sentence.replace(split_sentence_word, split_word).split()
    words = [ word for word in words if not word.lower() in list(set(stopwords+nltk_stopwords_english+slothlib_stopwords_japanese)) ]
    return words

def text_split2sentences(text:str,
                         split_sentence_word:str = '。') -> List[str]:
    sentences = text.split(split_sentence_word)
    return sentences

def create_sentence_in_words(text:str,
                             split_word:str = ' ',
                             split_sentence_word:str = '。') -> List[List[str]]:
    sentence_in_words =[]
    sentences = text_split2sentences(text, split_sentence_word)
    for sentence in sentences:
        words = text_split2words(sentence, split_word, split_sentence_word)
        sentence_in_words.append(words)
    return sentence_in_words
    
def calculation_jaccard(sentence_in_words:List[List[str]],
                        min_coef:float = 0,
                        min_cnt:int    = 1,) -> Dict[str, float]:
    pair_all     = []
    jaccard_coef = []
    jaccard_dict = {}
    
    for sentence_in_word in sentence_in_words:
        pair_temp = list(combinations(set(sentence_in_word), 2))
        for i, pair in enumerate(pair_temp):
            pair_temp[i] = tuple(sorted(pair))
        pair_all += pair_temp
    
    pair_count = Counter(pair_all)
    for key, count in dropwhile(lambda key_count: key_count[1] >= min_cnt, pair_count.most_common()):
        del pair_count[key]
    
    word_count = Counter()
    for sentence_in_word in sentence_in_words:
        word_count += Counter(set(sentence_in_word))
    
    for pair, cnt in pair_count.items():
        jaccard_coef.append(cnt / (word_count[pair[0]] + word_count[pair[1]] - cnt))
    
    for (pair, cnt), coef in zip(pair_count.items(), jaccard_coef):
        if coef >= min_coef:
            jaccard_dict[pair] = {
                'jaccard_coef': coef,
                'pair_cnt':     cnt,
            }
    return jaccard_dict


def calculation_word_frequency(sentence_in_words:List[List[str]],
                               token_length:str ='{2,}',
                               min_cnt:int      = 1) -> Dict[str, int]:
    freq_dict = {}
    
    token_pattern = f'\\b\\w{token_length}\\b'
    count_model   = CountVectorizer(token_pattern=token_pattern, analyzer=lambda x: x, lowercase=False)

    X            = count_model.fit_transform(sentence_in_words)
    words_list   = count_model.get_feature_names_out()
    words_counts = np.asarray(X.sum(axis=0)).reshape(-1)
    
    for word, cnt in zip(words_list, words_counts):
        if cnt >= min_cnt:
            freq_dict[word] = cnt

    return freq_dict

nltk_stopwords_english = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
    'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
    'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
    'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
    'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
    'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",]
# http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt
slothlib_stopwords_japanese = [
    'あそこ', 'あたり', 'あちら', 'あっち', 'あと', 'あな', 'あなた', 'あれ', 'いくつ', 'いつ',
    'いま', 'いや', 'いろいろ', 'うち', 'おおまか', 'おまえ', 'おれ', 'がい', 'かく', 'かたち',
    'かやの', 'から', 'がら', 'きた', 'くせ', 'ここ', 'こっち', 'こと', 'ごと', 'こちら',
    'ごっちゃ', 'これ', 'これら', 'ごろ', 'さまざま', 'さらい', 'さん', 'しかた', 'しよう', 'すか',
    'ずつ', 'すね', 'すべて', 'ぜんぶ', 'そう', 'そこ', 'そちら', 'そっち', 'そで', 'それ',
    'それぞれ', 'それなり', 'たくさん', 'たち', 'たび', 'ため', 'だめ', 'ちゃ', 'ちゃん', 'てん',
    'とおり', 'とき', 'どこ', 'どこか', 'ところ', 'どちら', 'どっか', 'どっち', 'どれ', 'なか',
    'なかば', 'なに', 'など', 'なん', 'はじめ', 'はず', 'はるか', 'ひと', 'ひとつ', 'ふく',
    'ぶり', 'べつ', 'へん', 'ぺん', 'ほう', 'ほか', 'まさ', 'まし', 'まとも', 'まま', 'みたい',
    'みつ', 'みなさん', 'みんな', 'もと', 'もの', 'もん', 'やつ', 'よう', 'よそ', 'わけ',
    'わたし', 'ハイ', '上', '中', '下', '字', '年', '月', '日', '時', '分', '秒', '週',
    '火', '水', '木', '金', '土', '国', '都', '道', '府', '県', '市', '区', '町',
    '村', '各', '第', '方', '何', '的', '度', '文', '者', '性', '体', '人', '他',
    '今', '部', '課', '係', '外', '類', '達', '気', '室', '口', '誰', '用', '界',
    '会', '首', '男', '女', '別', '話', '私', '屋', '店', '家', '場', '等', '見',
    '際', '観', '段', '略', '例', '系', '論', '形', '間', '地', '員', '線', '点',
    '書', '品', '力', '法', '感', '作', '元', '手', '数', '彼', '彼女', '子', '内',
    '楽', '喜', '怒', '哀', '輪', '頃', '化', '境', '俺', '奴', '高', '校', '婦',
    '伸', '紀', '誌', 'レ', '行', '列', '事', '士', '台', '集', '様', '所', '歴',
    '器', '名', '情', '連', '毎', '式', '簿', '回', '匹', '個', '席', '束', '歳',
    '目', '通', '面', '円', '玉', '枚', '前', '後', '左', '右', '次', '先', '春',
    '夏', '秋', '冬', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
    '百', '千', '万', '億', '兆', '下記', '上記', '時間', '今回', '前回', '場合', '一つ',
    '年生', '自分', 'ヶ所', 'ヵ所', 'カ所', '箇所', 'ヶ月', 'ヵ月', 'カ月', '箇月', '名前',
    '本当', '確か', '時点', '全部', '関係', '近く', '方法', '我々', '違い', '多く', '扱い',
    '新た', 'その後', '半ば', '結局', '様々', '以前', '以後', '以降', '未満', '以上', '以下',
    '幾つ', '毎日', '自体', '向こう', '何人', '手段', '同じ', '感じ',]