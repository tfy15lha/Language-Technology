import regex as re
import string
import math

def splitSentences():
    text = open('Selma.txt').read()
    pat = re.compile(r'([A-ZÅÄÖ][^\.!?]*[\.!?])', re.M)
    sentences = pat.findall(text.replace('\n', ' '))

    for element in range(0,len(sentences)):
        exclude = set(string.punctuation)
        sentences[element] = ''.join(ch for ch in sentences[element] if ch not in exclude)

        sentences[element] = '<s> ' + sentences[element] + ' </s>'
        sentences[element] = sentences[element].lower()

        #print(sentences[element])

    return sentences


def tokenize(text):
    words = re.findall('\p{L}+', text)
    return words

def unigrams(sentences):


    test_sentance_1 = sentences[333]
    test_sentance_2 = sentences[120]
    test_sentance_3 = sentences[233]
    test_sentance_4 = sentences[12111]
    test_sentance_5 = sentences[44211]

    print(test_sentance_5)
    sample_text = " det var en gång en katt som hette nils </s> "
    searchable = sample_text.split()

    sample_text_2 = "<s> det var en gång en katt som hette nils </s> "
    searchable_2 = sample_text_2.split()
    print(searchable_2)
    words = []
   # text = open("Selma.txt").read().lower().strip()
   # print(tokenize(text))


    for i in range(0,len(sentences)):
        temp = sentences[i].split()
        for j in range(0,len(temp)):
            words.append(temp[j])

    wordcount = len(words)
    print(wordcount)
    frequnecy = count_unigrams(words) #Gives a list with number of words
    list_of_bigrams = count_bigrams(words)


    unigram_prog = {} #Saknas typ 40000 ord så blir lite skevt OM DEN BRYTER I EN RAD RÄKNAS DET SOM ETT ORD
    print(frequnecy['det'])
    for word in words:
        unigram_prog[word] = frequnecy[word]/wordcount
    print(unigram_prog["</s>"])
    entropy_sum = 0
    unigram_prob = 1
    printable_words = {}
    geometric = 0
    for items in searchable:
        printable_words[items] = [items,frequnecy[items],wordcount,unigram_prog[items]]
        unigram_prob *= unigram_prog[items]


    geometric += pow(unigram_prob, 1 / len(searchable))
    print_table_Unigram(printable_words, -1*math.log(geometric,2),unigram_prob,geometric)

    index1 = 0
    index2 = 1
    bigram_freq = []
    bigrams = []
    while index2 < len(searchable_2):
        try:
            bigram_freq.append(list_of_bigrams[searchable_2[index1], searchable_2[index2]])
            bigrams.append([searchable_2[index1],searchable_2[index2]])
            index1 += 1
            index2 += 1
        except:
            #bigram_freq.append(unigram_prog[searchable_2[index2]])
            bigrams.append([searchable_2[index1], searchable_2[index2]])
            bigram_freq.append(0)
            index1 += 1
            index2 += 1
    print(bigrams)
    word_freq = []
    index_search = 0
    for items in searchable_2:
        if(index_search != len(searchable_2)-1):
            word_freq.append(frequnecy[items])
            index_search += 1
        else:
            break

    bigram_prob = []
    tot_bigram_prob = 1
    index1 = 0
    index2 = 1
    for i in range(0,len(bigram_freq)):
        try:
            bigram_prob.append((word_freq[i]/bigram_freq[i])**-1)
            tot_bigram_prob *= (word_freq[i]/bigram_freq[i])**-1
        except:
            bigram_prob.append(unigram_prog[searchable_2[i+1]])
            tot_bigram_prob *= unigram_prog[searchable_2[i+1]]

    print(bigram_prob)



    print(word_freq)


    print(bigram_freq)
    geometric2 = 0
    geometric2 = pow(tot_bigram_prob, 1 / len(searchable_2))
    print_table_Bigram(bigrams,bigram_freq,word_freq,bigram_prob,-1*math.log(geometric2,2),geometric2,tot_bigram_prob)
def print_table_Unigram(printable,entropy,unigram_prob,geometric):
    print("Unigram Model")
    print("========================================")
    print("wi C(wi) #words P(wi)")
    print("========================================")
    for items in printable:
        print(printable[items])
    print("========================================")
    print("Prob. unigrams = ",unigram_prob)
    print("Geometric mean prob. = ",geometric)
    print("Entropy rate = ",entropy)
    print("Perplexity = ",2**entropy)

def print_table_Bigram(words,bigram_freq,word_freq,bigram_prob,entropy,geometric,tot_bigram_prob):
    print("Bigram Model")
    print("========================================")
    print("wi wi+1 Ci, i+1 C(i) #words P(wi)")
    print("========================================")
    printlist = []
    index = 0
    for items in words:
        printlist.append([words[index],bigram_freq[index],word_freq[index],bigram_prob[index]])
        index += 1


    for i in range(0,len(printlist)):
        print(printlist[i])
    print("========================================")
    print("Prob. unigrams = ",tot_bigram_prob)
    print("Geometric mean prob. = ",geometric)
    print("Entropy rate = ",entropy)
    print("Perplexity = ",2**entropy)



def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies

def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def main():
    sentencese = splitSentences()
    unigrams(sentencese)



if __name__ == '__main__':

    main()
