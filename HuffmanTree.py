__author__='zhaoyan'

import numpy as np

class HuffmanTreeNode():
    def __init__(self, value, possibility):
        self.possibility = possibility
        self.left = None
        self.right = None
        self.value = value
        self.Huffman = ""

    def __str__(self):
        return 'HuffmanTreeNode object, value:{v}, possibility:{p}, Huffman:{h}'\
            .format(v=self.value, p=self.possibility, h=self.Huffman)

class HuffmanTree():
    def __init__(self, word_dict, vec_len):
        self.vec_len = vec_len
        self.root = None

        word_dict_list = list(word_dict.values())
        node_list = [HuffmanTreeNode (x['word'], x['possibility']) for x in word_dict_list]
        self.build_tree(node_list)
        self.generate_huffman_code(self.root, word_dict)

    def build_tree(self, node_list):
        while node_list.__len__() > 1:
            i1 = 0;
            i2 = 1;
            if node_list[i2].possibility < node_list[i1].possibility:
                [i1, i2] = [i2, i1]
            for i in range(2, node_list.__len__()):
                if node_list[i].possibility < node_list[i2].possibility:
                    i2 = i
                    if node_list[i2].possibility < node_list[i1].possibility:
                        [i1, i2] = [i2, i1]
            top_node = self.merge(node_list[i1], node_list[i2])
            if i1 < i2:
                node_list.pop(i2)
                node_list.pop(i1)
            elif i1 > i2:
                node_list.pop(i1)
                node_list.pop(i2)
            else:
                raise RuntimeError('i1 should not be equal i2')
            node_list.insert(0, top_node)
        self.root = node_list[0]

    def generate_huffman_code(self, node, word_dict):
        stack = [self.root]
        while(stack.__len__()>0):
            node = stack.pop()
            while node.left or node.right:
                code =  node.Huffman
                node.left.Huffman = code + "1"
                node.right.Huffman = code + "0"
                stack.append(node.right)
                node = node.left
            word = node.value
            code = node.Huffman
            word_dict[word]['Huffman'] = code

    def merge(self, node1, node2):
        top_pos = node1.possibility + node2.possibility
        top_node = HuffmanTreeNode(np.zeros([1, self.vec_len]), top_pos)
        if node1.possibility >= node2.possibility:
            top_node.left = node1
            top_node.right = node2
        else:
            top_node.left = node2
            top_node.right = node1
        return top_node















