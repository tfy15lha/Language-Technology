import transition
def extract(stack,queue,graph,feature_names,sentence):
    full_sentence = sentence
    features = []
   # print(sentence)
    try:
        #feature_names = [stack_0_postag, stack_0_form,stack_1_postag,stack_1_form,queue_0_postag,queue_0_form_queue_1_postag,queue_1_form_forward_word_postag,forward_word_form_backward_word_postag_backward_word_form]
        features.append(stack[0]['postag'])
        features.append(stack[0]['form'])
        try:
            features.append(stack[1]['postag'])
            features.append(stack[1]['form'])

        except:
            features.append("nil")
            features.append("nil")
    except:
        features.append("nil")
        features.append("nil")
        features.append("nil")
        features.append("nil")
    try:

        features.append(queue[0]['postag'])
        features.append(queue[0]['form'])
        features.append(queue[1]['postag'])
        features.append(queue[1]['form'])
    except:
        features.append(queue[0]['postag'])
        features.append(queue[0]['form'])
        features.append("nil")
        features.append("nil")
    #print(sentence['id'])
    try:
        id = stack[0]['id']
        for ids in range(len(sentence)):
            if sentence[ids]['id'] == id:
                features.append(sentence[ids+1]['postag'])
                features.append(sentence[ids+1]['form'])
    except:
        features.append('nil')
        features.append('nil')

    try:
        id = stack[0]['id']
        for ids in range(len(sentence)):
            if sentence[ids]['id'] == id:
                features.append(sentence[ids - 1]['postag'])
                features.append(sentence[ids - 1]['form'])
    except:
        features.append('nil')
        features.append('nil')

    if transition.can_leftarc(stack,graph):
        can_la = True
    else:
        can_la = False
    if transition.can_reduce(stack,graph):
        can_re = True
    else:
        can_re = False
    features.append(can_re)
    features.append(can_la)

    return features

