import gensim
import os

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname),  'r', encoding='utf-8'):
                yield line.split()

sentences = MySentences('./static/data')
model = gensim.models.Word2Vec(sentences)
model.save('./model/model_g')

model = gensim.models.Word2Vec.load('./model/model_g')

print(model.similarity('北京','深圳'))
print(model.similarity('亿', '女人'))
print(model['水'])