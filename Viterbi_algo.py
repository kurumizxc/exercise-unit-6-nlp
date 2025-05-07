from Hidden_markov import hidden_markov
from collections import defaultdict
import math

sentences = [
    "The_DET cat_NOUN sleeps_VERB",
    "A_DET dog_NOUN barks_VERB",
    "The_DET dog_NOUN sleeps_VERB",
    "My_DET dog_NOUN runs_VERB fast_ADV",
    "A_DET cat_NOUN meows_VERB loudly_ADV",
    "Your_DET cat_NOUN runs_VERB",
    "The_DET bird_NOUN sings_VERB sweetly_ADV",
    "A_DET bird_NOUN chirps_VERB"
]

#funtion from previous code
transition_probs, emission_probs = hidden_markov(sentences)

def viterbi(sentence, trans_probs, emit_probs):
    words = sentence.split()
    if not words: return []
    
    tags = list(emit_probs.keys())
    v = [{}]
    path = {}
    
    for tag in tags:
        trans = trans_probs['START'].get(tag, 1e-6)
        emit = emit_probs[tag].get(words[0], 1e-6)
        v[0][tag] = math.log(trans) + math.log(emit)
        path[tag] = [tag]
    

    for t in range(1, len(words)):
        v.append({})
        new_path = {}
        
        for curr_tag in tags:
            emit = emit_probs[curr_tag].get(words[t], 1e-6)
            best = max(
                [(prev_tag, v[t-1][prev_tag] + 
                math.log(trans_probs[prev_tag].get(curr_tag, 1e-6)) + 
                math.log(emit)) for prev_tag in tags],
                key=lambda x: x[1]
            )
            v[t][curr_tag] = best[1]
            new_path[curr_tag] = path[best[0]] + [curr_tag]
            
        path = new_path
    
   
    best_tag = max(
        [(tag, v[-1][tag] + math.log(trans_probs[tag].get('END', 1e-6))) 
        for tag in tags],
        key=lambda x: x[1]
    )[0]
    
    return path[best_tag]

# Test sentences
test_sentences = [
    "The cat meows",
    "My dog barks loudly"
]

for sentence in test_sentences:
    tags = viterbi(sentence, transition_probs, emission_probs)
    result = ' '.join(f"{w}_{t}" for w, t in zip(sentence.split(), tags))
    print(f"Sentence: {sentence}\nTagged:   {result}\n")