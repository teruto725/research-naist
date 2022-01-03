

def is_relevant(comment, stopwords):
  comment_with_no_stopwords = [word for word in comment if word not in stopwords]
  comment_size = len(comment.split())
  
  is_relevant = True
  # Useless comments, no content after removing stopwords
  # 使えないコマンド: ストップワードを抜いた結果コンテンツが0になった
  if len(comment_with_no_stopwords) == 0:
      is_relevant = False

  # Useless comments, one word, no action required or unclear action
  # 使えないコメント: １単語で行動を促していないor明確なアクションを示していない
  elif comment_size == 1:
      if comment.__contains__('nice') or comment.__contains__('pleas') \
          or comment.__contains__('ditto') or comment.__contains__('thank') \
          or comment.__contains__('ditto2') or comment.__contains__('fine') \
          or comment.__contains__('agew') or comment.__contains__('hahaha') \
          or comment.__contains__('yeh') or comment.__contains__('lol'):
          is_relevant = False

  elif comment_size == 2:
      if comment.__contains__('ack'):
          is_relevant =False

  # Request to change formatting, no impact on code
  # コードのフォーマッティングはコードに影響しないので
  elif comment.__contains__('indent') and comment_size < 5:
      is_relevant = False

  # Likely a thank you message
  # ありがとうメッセージ
  elif (comment.__contains__('works for me') or comment.__contains__('sounds good') \
      or comment.__contains__('makes sense') or comment.__contains__('smile') \
      or comment.__contains__('approv')) and comment_size < 5:
      is_relevant = False

  # Request to add test code, no impact on the reviewed code
  # テストコードのリクエスト
  elif (comment.__contains__('test') and comment_size < 5) \
      or (comment.__contains__('add') and comment.__contains__('test')):
      is_relevant = False

  # Request for clarification
  # 質問文
  elif ((comment.__contains__('please explain') or comment.__contains__('explan') \
          or comment.__contains__('wat') or comment.__contains__('what')) and comment_size < 5) \
      or ((comment.__contains__('understand') or comment.__contains__('meant')) \
          and comment.__contains__('not sure')):
      is_relevant = False

  # Refers to previous comment or external resource with unclear action point
  # 事前のコメント
  elif (comment.__contains__('same as') or comment.__contains__('same remark') \
          or comment.__contains__('said above') or comment.__contains__('do the same')) \
      and comment_size < 5:
      is_relevant = False

  # Refers to web pages
  # webページの参照
  elif (comment.__contains__('like') or comment.__contains__('see')) \
      and comment.__contains__('http'):
      is_relevant = False

  # Request to add comment
  # コメントの要求
  elif comment.__contains__('document') or comment.__contains__('javadoc') \
          or comment.__contains__('comment'):
      is_relevant =  False

  # Feedback about reorganizing the PR
  # PRの整理
  elif comment.__contains__('pr') and comment_size < 5:
      is_relevant = False

  # Comment contains a +1 to support previous comment.
  # It may be accompanied by another word, like agree or a smile.
  # This is the reason for < 3

  elif comment.__contains__('+1') and comment_size < 3:
      is_relevant = False

  # The code is ok for now
  # 今すぐ？
  elif comment.__contains__('for now') and comment_size < 5:
      is_relevant = False

  # Answers
  # 回答メッセージ
  elif (comment.__contains__('fixed') or comment.__contains__('thank') \
          or comment.__contains__('youre right')) and comment_size < 3:
      is_relevant = False
      

  return is_relevant


import pandas as pd
import numpy as np
import is_relevant 
import pickle
import nltk
from nltk.corpus import stopwords
stopwords_nltk = stopwords.words("english")


if __name__ == '__main__':
  # import
  train_df = pd.read_csv("./original_data/prev/train.csv", index_col=0)
  test_df = pd.read_csv("./original_data/prev/test.csv", index_col=0)
  val_df = pd.read_csv("./original_data/prev/val.csv", index_col=0)

  # フィルタリング
  print("filtering_train")
  train_cleaned_df = train_df[train_df["comment"].apply(lambda x: is_relevant.is_relevant(x,stopwords_nltk) )]
  print("filtering_test")
  test_cleaned_df = test_df[test_df["comment"].apply(lambda x: is_relevant.is_relevant(x,stopwords_nltk) )]
  print("filtering_val")
  val_cleaned_df = val_df[val_df["comment"].apply(lambda x: is_relevant.is_relevant(x,stopwords_nltk) )]
  
  #pkl保存
  print("save")
  train_cleaned_df.to_pickle("./1.cleaned_prev_data/train.pkl")
  test_cleaned_df.to_pickle("./1.cleaned_prev_data/test.pkl")
  val_cleaned_df.to_pickle("./1.cleaned_prev_data/val.pkl")