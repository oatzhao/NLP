__author__ = 'yan.zhao'


from collections import Counter
from operator import itemgetter as _itemgetter
import jieba
import File_Interface as FI

class WordCounter():
    # can calculate the freq of words in a text list

    # for example
    # >>> data = ['Merge multiple sorted inputs into a single sorted output',
    #           'The API below differs from textbook heap algorithms in two aspects']
    # >>> wc = WordCounter(data)
    # >>> print(wc.count_res)

    # >>> MulCounter({' ': 18, 'sorted': 2, 'single': 1, 'below': 1, 'inputs': 1, 'The': 1, 'into': 1, 'textbook': 1,
    #                'API': 1, 'algorithms': 1, 'in': 1, 'output': 1, 'heap': 1, 'differs': 1, 'two': 1, 'from': 1,
    #                'aspects': 1, 'multiple': 1, 'a': 1, 'Merge': 1})

    def __init__(self, text_list):
        self.text_list = text_list
        self.stop_word = self.Get_Stop_Words()
        self.count_res = None

        self.Word_Count(self.text_list)

    def Get_Stop_Words(self):
        ret = []
        ret = FI.load_pickle('./static/stop_words.pkl')
        return ret

    def Word_Count(self,text_list,cut_all=False):
        cutls = []
        filtered_word_list = []
        count = 0
        for line in text_list:
            res = jieba.cut(line,cut_all=cut_all)
            res = list(res)
            for i in range(0, len(res)):
                if res[i] != ' ':
                    cutls.append(res[i])
                else:
                    pass
            text_list[count] = cutls
            count += 1
            filtered_word_list += cutls

        self.count_res = MulCounter(filtered_word_list)
        for word in self.stop_word:
            try:
                self.count_res.pop(word)
            except:
                pass

class MulCounter(Counter):
    # a class extends from collections.Counter
    # add some methods, larger_than and less_than
    def __init__(self,element_list):
        super().__init__(element_list)

    def larger_than(self,minvalue,ret='list'):
        temp = sorted(self.items(),key=_itemgetter(1),reverse=True)
        low = 0
        high = temp.__len__()
        while(high - low > 1):
            mid = (low+high) >> 1
            if temp[mid][1] >= minvalue:
                low = mid
            else:
                high = mid
        if temp[low][1]<minvalue:
            if ret=='dict':
                return {}
            else:
                return []
        if ret=='dict':
            ret_data = {}
            for ele,count in temp[:high]:
                ret_data[ele]=count
            return ret_data
        else:
            return temp[:high]

    def less_than(self,maxvalue,ret='list'):
        temp = sorted(self.items(),key=_itemgetter(1))
        low = 0
        high = temp.__len__()
        while ((high-low) > 1):
            mid = (low+high) >> 1
            if temp[mid][1] <= maxvalue:
                low = mid
            else:
                high = mid
        if temp[low][1]>maxvalue:
            if ret=='dict':
                return {}
            else:
                return []
        if ret=='dict':
            ret_data = {}
            for ele,count in temp[:high]:
                ret_data[ele]=count
            return ret_data
        else:
            return temp[:high]

def readfile(filename):
    inf = open(filename, 'r', encoding='utf-8')
    linestr = inf.read().strip()
    linestrlist = linestr.split("\t")
    return linestrlist

if __name__ == '__main__':
    text = readfile('./static/text8')
    wc = WordCounter(text)
    print(wc.count_res.larger_than(5))