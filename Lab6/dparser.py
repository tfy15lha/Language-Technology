"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import features2
import conll
import features3
from sklearn.feature_extraction import DictVectorizer
import features
import numpy as np
import array
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
import pickle
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'



def parse_ml(stack, queue, graph, trans):
    #print(trans)
    if stack and transition.can_rightarc(stack) and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    elif stack and transition.can_leftarc(stack,graph) and trans[:2]  == 'la': #VARFÖR :2
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    elif stack and transition.can_reduce(stack,graph) and trans[:2] == 're':
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    else:
        stack,queue,graph = transition.shift(stack,queue,graph)
        return stack,queue,graph,"sh"
if __name__ == '__main__':
    feature_names = ["stack_0_postag", "stack_0_form", "stack_1_postag", "stack_1_form", "queue_0_postag",
                     "queue_0_form", "queue_1_postag", "queue_1_form", "forward_word_postag",
                     "forward_word_form", "backward_word_postag", "backward_word_form", "can_ra", "can_la"]
    feature_names = ["stack_0_postag", "stack_0_form", "stack_1_postag", "stack_1_form", "queue_0_postag",
                     "queue_0_form", "queue_1_postag", "queue_1_form", "can_ra", "can_la"]
    feature_names = ["stack_0_postag", "stack_0_form", "queue_0_postag",
                     "queue_0_form", "can_ra", "can_la"]
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    sent_cnt = 0
    f = open("goldstandardf3.txt", "w+")
    y_vector = []
    x_matrix = []
    X = list()
    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}  
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []

        #feature_names = ["stack_pos", "stack_word", "queue_pos", "queue_word", "can_ra", "can_la"]


        while queue:
           # print(queue)

            x = features.extract(stack, queue, graph, feature_names, sentence)
            X.append(dict(zip(feature_names, x))) #Nu producerar denna en lång lista, där varje element är en mening. Ändra till att vare ord är ett eget element
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            y = trans

            y_vector.append(y)



        stack, graph = transition.empty_stack(stack, graph)
      #  print('Equal graphs:', transition.equal_graphs(sentence, graph))


        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
            for things in word:
                f.write(word[things])
                f.write(" ")
            f.write("\n")
    #Train
    vec = DictVectorizer(sparse=True)
    print(vec)
    X_vec = vec.fit_transform(X)
    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
    classifier.fit(X_vec, y_vector)
    filename = 'model1.sav'
    pickle.dump(classifier, open(filename, 'wb'))
    pickle.dump(vec, open("vec1.pickle", "wb"))
    ##
    sentences_test = conll.read_sentences(test_file)
    loaded_model = pickle.load(open('model1.sav', 'rb'))
    vec = pickle.load((open("vec1.pickle",'rb')))
    formatted_corpus_test = conll.split_rows(sentences_test, column_names_2006)
    x_predict = []
    g = open("testf3.txt", "w+")
    y_predict = []
    X_test_predict = []
    classifier = loaded_model

    for sentence in formatted_corpus_test:
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        word_names = ["form","trans"]
        stack = []
        while queue:
            y_predict = []
            x_predict = features.extract(stack, queue, graph, feature_names, sentence)
            x_predict_fitted = vec.transform((dict(zip(feature_names, x_predict))))
            y_predict = classifier.predict(x_predict_fitted)
            stack, queue, graph, trans = parse_ml(stack, queue, graph, y_predict[-1])



        #print(transition.equal_graphs(words,graph))

        stack, graph = transition.empty_stack(stack, graph)
        for word in sentence:

            #print(words['id'])

            word['head'] = graph['heads'][word['id']]
            word['deprel'] = graph['deprels'][word["id"]]

    conll.save("testf3.txt",formatted_corpus_test,column_names_2006)