import transition
def extract(stack,queue,graph,feature_names,sentence):
    full_sentence = sentence
    features = []

    try:
        features.append(stack[0]['postag'])
        features.append(stack[0]['form'])
    except:
        features.append("nil")
        features.append("nil")

    features.append(queue[0]['postag'])
    features.append(queue[0]['form'])
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

