"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split('\t'))) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


def find_ss():
    train_file = 'training.conll'
    train_file = "spanish.txt"
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    index = 0
    subject_verb_dict = {}
    for i in range(len(formatted_corpus)):
        for word in formatted_corpus[i]:
            if word['deprel'] == 'nsubj':
                index = index + 1
                id = word['head']
                subject_word = word['form'].lower()
                for words in formatted_corpus[i]:

                    if id == words['id']:
                        verb = words['form'].lower()

                try:
                    tuple = (subject_word,verb)
                    subject_verb_dict[tuple] = subject_verb_dict[tuple] + 1
                except:
                    tuple = (subject_word, verb)
                    subject_verb_dict[tuple] = 1
    number = 0
    for key, value in sorted(subject_verb_dict.items(), key=lambda kv: kv[1], reverse=False):
        print("%s: %s" % (key, value))
    print(number)
    print(subject_verb_dict)
    print(index)

def find_triples():
    train_file = 'training.conll'
    train_file = 'spanish.txt'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    index = 0
    tripleindex = 0
    objectnumber = 0
    oo_index = 0
    subject_verb_obj = {}
    for i in range(len(formatted_corpus)):

        for word in formatted_corpus[i]:
            if word['deprel'] == 'obj': #00 for old

                already = True
                last_ready = True
                index = word['head']
                object_word = word['form'].lower()
                for wording in formatted_corpus[i]:
                    if wording['deprel'] == 'nsubj': #ss for old
                        if index == wording['head']:
                            last_index = wording['head']
                            subject_word = wording['form']
                            if last_index != "0":
                                for words in formatted_corpus[i]:
                                    if last_index == words['id']:
                                        triple = (subject_word.lower()  , words['form'].lower(), object_word.lower())
                                        oo_index = oo_index+1
                                        try:
                                            subject_verb_obj[triple] = subject_verb_obj[triple] + 1
                                        except:
                                            subject_verb_obj[triple] = 1




    number = 0

    for key, value in sorted(subject_verb_obj.items(), key=lambda kv: kv[1], reverse=False):
      print("%s: %s" % (key, value))
    print(number)

    print(tripleindex)
    print(objectnumber)
    print(oo_index)
if __name__ == '__main__':



    # train_file = 'test_x'
    test_file = 'test.conll'
    find_triples()
    #find_ss()


    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    files = get_files('ud-treebanks-v2.4/', 'de_gsd-ud-train.conllu')
    for train_file in files:

        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        for i in range(len(formatted_corpus)):
            for items in formatted_corpus[i]:
                if len(items['id']) > 2:

                    items.pop('id')
                    items.pop('form')
                    items.pop('lemma')
                    items.pop('upostag')
                    items.pop('xpostag')
                    items.pop('feats')
                    items.pop('head')
                    items.pop('deprel')
                    items.pop('deps')
                    items.pop('misc')
        print(train_file, len(formatted_corpus))
       # print(formatted_corpus)
        save("spanish.txt",formatted_corpus,column_names_u)