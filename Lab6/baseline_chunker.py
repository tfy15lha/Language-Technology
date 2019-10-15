"""
Baseline chunker for CoNLL 2000
"""
__author__ = "Pierre Nugues"

import conll_reader
#EDITED BY LUDVIG HASBRING AND JESPER GUNNARSSON

def count_pos(corpus):
    """
    Computes the part-of-speech distribution
    in a CoNLL 2000 file
    :param corpus:
    :return:
    """

    pos_cnt = {}
    for sentence in corpus:
        for row in sentence:
            if row['pos'] in pos_cnt:
                pos_cnt[row['pos']] += 1
            else:
                pos_cnt[row['pos']] = 1

    return pos_cnt


def train(corpus):
    """
    Computes the chunk distribution by pos
    The result is stored in a dictionary
    :param corpus:
    :return:
    """
    pos_cnt = count_pos(corpus)
    # We compute the chunk distribution by POS
    chunk_dist = {key: {} for key in pos_cnt.keys()}

    """
    Fill in code to compute the chunk distribution for each part of speech
    """
    print(corpus)
    indexi = {}
    chunk_dictionary = {}
    for sentence in corpus:
        for row in sentence:
            chunk_category = row['pos']
            key = row['chunk']
            if key in chunk_dist[chunk_category]:
                chunk_dist[chunk_category][key] = chunk_dist[chunk_category][key] +1
            else:
                chunk_dist[chunk_category][key] = 1

    most_used = {}
    for category in chunk_dist:

        most_freq = 0
        word = ""
        for things in chunk_dist[category]:
            number = chunk_dist[category][things]
            if number > most_freq:
                most_freq = number
                word = things
        most_used[category] = word
    print(most_used)
    pos_chunk = {}
    """
    Fill in code so that for each part of speech, you select the most frequent chunk.
    You will build a dictionary with key values:
    pos_chunk[pos] = most frequent chunk for pos
    """
    return most_used


def predict(model, corpus):
    """
    Predicts the chunk from the part of speech
    Adds a pchunk column
    :param model:
    :param corpus:
    :return:
    """
    """
    We add a predicted chunk column: pchunk
    """
    append_list = []
   #file = open('testfile.txt','w')
    file = open('outputfile.txt', 'w')


    for sentence in corpus:
        for row in sentence:
            row['pchunk'] = model[row['pos']]
            append_list.append(model[row['pos']])
            file.write(row['form'])
            file.write(' ')
            file.write(row['pos'])
            file.write(' ')
            file.write(row['chunk'])
            file.write(' ')
            file.write(row['pchunk'])
            file.write('\n')
    file.close()
    return corpus


def eval(predicted):
    """
    Evaluates the predicted chunk accuracy
    :param predicted:
    :return:
    """
    word_cnt = 0
    correct = 0
    for sentence in predicted:
        for row in sentence:
            word_cnt += 1
            if row['chunk'] == row['pchunk']:
                correct += 1
    return correct / word_cnt


if __name__ == '__main__':
    column_names = ['form', 'pos', 'chunk']
    train_file = 'train.txt'
    test_file = 'test.txt'

    train_corpus = conll_reader.read_sentences(train_file)
    train_corpus = conll_reader.split_rows(train_corpus, column_names)
    test_corpus = conll_reader.read_sentences(test_file)
    test_corpus = conll_reader.split_rows(test_corpus, column_names)

    model = train(train_corpus)

    predicted = predict(model, test_corpus)
    accuracy = eval(predicted)
    print("Accuracy", accuracy)
    f_out = open('out', 'w')
    # We write the word (form), part of speech (pos),
    # gold-standard chunk (chunk), and predicted chunk (pchunk)
    for sentence in predicted:
        for row in sentence:
            f_out.write(row['form'] + ' ' + row['pos'] + ' ' +
                        row['chunk'] + ' ' + row['pchunk'] + '\n')
        f_out.write('\n')
    f_out.close()