__author__ = 'yan.zhao'

import math

from WordCount import WordCounter,MulCounter
import File_Interface as FI
from HuffmanTree import HuffmanTree

import numpy as np
import jieba
from sklearn import preprocessing

class Word2Vec():
    def __init__(self, vec_len=15000, learn_rate=0.025, win_len=5, model='cbow'):
        self.cutted_text_list = None
        self.vec_len = vec_len
        self.learn_rate = learn_rate
        self.win_len = win_len
        self.model = model
        self.word_dict = None  # each element is a dict, including: word,possibility,vector,huffmancode
        self.huffman = None    # the object of HuffmanTree

    def __Gnerate_Word_Dict(self,word_freq):
        # generate a word dict
        # which containing the word, freq, possibility, a random initial vector and Huffman value
        if not isinstance(word_freq,dict) and not isinstance(word_freq,list):
            raise ValueError('the word freq info should be a dict or list')

        word_dict = {}
        if isinstance(word_freq,dict):
            # if word_freq is in type of dictionary
            sum_count = sum(word_freq.values())
            for word in word_freq:
                temp_dict = dict(
                    word = word,
                    freq = word_freq[word],
                    possibility = word_freq[word]/sum_count,
                    vector = np.random.random([1,self.vec_len]),
                    Huffman = None
                )
                word_dict[word] = temp_dict
        else:
            # if word_freq is in type of list
            freq_list = [x[1] for x in word_freq]
            sum_count = sum(freq_list)

            for item in word_freq:
                temp_dict = dict(
                    word = item[0],
                    freq = item[1],
                    possibility = item[1]/sum_count,
                    vector = np.random.random([1,self.vec_len]),
                    Huffman = None
                )
                word_dict[item[0]] = temp_dict
        self.word_dict = word_dict

    def Train_Model(self,text_list):

        # generate the word_dict and huffman tree
        if self.huffman==None:
            # if the dict is not loaded, it will generate a new dict
            if self.word_dict==None :
                wc = WordCounter(text_list)
                self.__Gnerate_Word_Dict(wc.count_res.larger_than(5))
                self.cutted_text_list = wc.text_list

            # generate a huffman tree according to the possibility of words
            self.huffman = HuffmanTree(self.word_dict,self.vec_len)
        print('word_dict and huffman tree already generated, ready to train vector')

        # start to train word vector
        before = (self.win_len-1) >> 1
        after = self.win_len-1-before

        if self.model=='cbow':
            method = self.__Deal_Gram_CBOW
        else:
            method = self.__Deal_Gram_SkipGram

        if self.cutted_text_list:
            # if the text has been cutted
            total = self.cutted_text_list.__len__()
            count = 0
            for line in self.cutted_text_list:
                line_len = line.__len__()
                for i in range(line_len):
                    method(line[i],line[max(0,i-before):i]+line[i+1:min(line_len,i+after+1)])
                count += 1
                print('{c} of {d}'.format(c=count,d=total))

        else:
            # if the text has note been cutted
            for line in text_list:
                line = list(jieba.cut(line,cut_all=False))
                line_len = line.__len__()
                for i in range(line_len):
                    method(line[i],line[max(0,i-before):i]+line[i+1:min(line_len,i+after+1)])
        print('word vector has been generated')

    def __Deal_Gram_CBOW(self,word,gram_word_list):

        if not self.word_dict.__contains__(word):
            return

        word_huffman = self.word_dict[word]['Huffman']
        gram_vector_sum = np.zeros([1,self.vec_len])
        for i in range(gram_word_list.__len__())[::-1]:
            item = gram_word_list[i]
            if self.word_dict.__contains__(item):
                gram_vector_sum += self.word_dict[item]['vector']
            else:
                gram_word_list.pop(i)

        if gram_word_list.__len__()==0:
            return

        e = self.__GoAlong_Huffman(word_huffman,gram_vector_sum,self.huffman.root)

        for item in gram_word_list:
            self.word_dict[item]['vector'] += e
            self.word_dict[item]['vector'] = preprocessing.normalize(self.word_dict[item]['vector'])

    def __Deal_Gram_SkipGram(self,word,gram_word_list):

        if not self.word_dict.__contains__(word):
            return

        word_vector = self.word_dict[word]['vector']
        for i in range(gram_word_list.__len__())[::-1]:
            if not self.word_dict.__contains__(gram_word_list[i]):
                gram_word_list.pop(i)

        if gram_word_list.__len__()==0:
            return

        for u in gram_word_list:
            u_huffman = self.word_dict[u]['Huffman']
            e = self.__GoAlong_Huffman(u_huffman,word_vector,self.huffman.root)
            self.word_dict[word]['vector'] += e
            self.word_dict[word]['vector'] = preprocessing.normalize(self.word_dict[word]['vector'])

    def __GoAlong_Huffman(self,word_huffman,input_vector,root):

        node = root
        e = np.zeros([1,self.vec_len])
        for level in range(word_huffman.__len__()):
            huffman_charat = word_huffman[level]
            q = self.__Sigmoid(input_vector.dot(node.value.T))
            grad = self.learn_rate * (1-int(huffman_charat)-q)
            e += grad * node.value
            node.value += grad * input_vector
            node.value = preprocessing.normalize(node.value)
            if huffman_charat=='0':
                node = node.right
            else:
                node = node.left
        return e

    def __Sigmoid(self,value):
        return 1/(1+math.exp(-value))

if __name__ == '__main__':
    import WordCount

    # text = WordCount.readfile('./static/text8_mini')
    # text = WordCount.readfile('./static/text8')
    # mv = Word2Vec(vec_len=500)
    # mv.Train_Model(text)
    # FI.save_picle(mv.word_dict, './model/model_h.pkl')

    model_h = FI.load_pickle('./model/model_h.pkl')
    keys = list(model_h.keys())
    print(keys.__len__())
    print(keys[0])


