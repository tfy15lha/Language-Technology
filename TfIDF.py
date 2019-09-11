import regex as re
import sys
import pickle
import os
import math


def tokenize(text):
    words = re.finditer('\p{L}+', text)
    return words


def text_to_idx(words):
    word_idx = {}
    for word in words:

        try:
            word_idx[word.group()].append(word.start())
        except:
            word_idx[word.group()] = [word.start()]
    return word_idx


def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


def toIDF(count, corpuslength, NumPage, NumTimes):
    IDF = (float(count) / corpuslength) * math.log10(NumPage / NumTimes)
    return IDF


def wordReader(corpus_files):
    master_index = {}
    idf_index = {}
    set_term = "nils"
    index = 0
    number_of_files = len(corpus_files)
    num_occ = 0
    textlength = {}
    tf_idf_matrix = {}
    for file in corpus_files:
        counter = 0

        text = open(file).read().lower().strip()
        wordcount = re.findall('\p{L}+', text)
        words = tokenize(text)

        textlength[file] = len(wordcount)
        idx = text_to_idx(words)
        for word in idx:
            if word in master_index:
                master_index[word][file] = idx[word]
            else:
                master_index[word] = {}
                master_index[word][file] = idx[word]
        try:
            master_index[set_term][file]
            num_occ = num_occ + 1

        except:
            num_occ = num_occ

    for file in corpus_files:
        try:

            counter = len(master_index[set_term][file])

            idf_index[index] = [file, set_term, toIDF(counter, textlength[file], number_of_files, num_occ)]
            index = index + 1

        except:
            counter = 0

    for file in corpus_files: #Loop through all files
        for word in master_index: #Loop through every word
            num_occ = 0
            for files in corpus_files: #Number of occurances of a single word in all files
                try:
                    master_index[word][files]
                    num_occ = num_occ + 1

                except:
                    num_occ = num_occ

            try:
                counter = len(master_index[word][file])
                tf_idf_matrix[file,word] = toIDF(counter, textlength[file], number_of_files, num_occ)
            except:
                tf_idf_matrix[file,word] = 0 #Put to zero if word does not exist in file

    #print(idf_index)
    tf_idf_sum = {}
    for file in corpus_files:
         tf_idf_sum[file] = 0
         for words in master_index:
             tf_idf_sum[file] += tf_idf_matrix[file,words]*tf_idf_matrix[file,words]

    print(tf_idf_matrix['bannlyst.txt','et'])
    scalarproduct = 0
    similarity_matrix = {}
    for file1 in corpus_files:
        for file2 in corpus_files:
            scalarproduct = 0
            for word in master_index:

                scalar1 = tf_idf_matrix[file1,word]
                scalar2 = tf_idf_matrix[file2, word]

                scalarproduct += CosineSim(scalar1,scalar2)
            similarity_matrix[file1,file2] = scalarproduct
    max_val = 0
    for file1 in corpus_files:
        for file2 in corpus_files:
            similarity_matrix[file1,file2] = similarity_matrix[file1,file2]/(math.sqrt(tf_idf_sum[file1]) * math.sqrt(tf_idf_sum[file2]))



    print(similarity_matrix)
    print(max_val)
#Create the TF-IDF Representation of all books

def CosineSim(num1,num2):
    return num1*num2

"""""
def wordReader(fileName):
    f = open(fileName, 'r')
    gosta_txt = f.read()
    f.close()
    gosta_txt = gosta_txt.lower()
    iter1 = tokenize(gosta_txt)
    index = text_to_idx(iter1)

    pickle.dump(index, open("save.p", "wb"))
    derp1 = pickle.load(open("save.p","rb"))
    print(derp1)
"""""


def main():
    inFile = sys.argv[1]
    fileName = get_files(inFile, "txt")
    os.chdir(inFile)
    wordReader(fileName)


if __name__ == '__main__':
    main()

