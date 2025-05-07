from collections import defaultdict
import pprint

def hidden_markov(sentences):
    transition_counts = defaultdict(lambda: defaultdict(int))
    emission_counts = defaultdict(lambda: defaultdict(int))

    for sentence in sentences:
        words_tags = sentence.split()
        tags = ["START"] + [wt.split('_')[1] for wt in words_tags] + ["END"]

        for i in range(len(tags) - 1):
            prev, curr = tags[i], tags[i+1]
            transition_counts[prev][curr] += 1

        for wt in words_tags:
            word, tag = wt.split('_')
            emission_counts[tag][word] += 1

    transition_probs = defaultdict(dict)
    for prev in transition_counts:
        total = sum(transition_counts[prev].values())
        for curr in transition_counts[prev]:
            transition_probs[prev][curr] = transition_counts[prev][curr] / total

    emission_probs = defaultdict(dict)
    for tag in emission_counts:
        total = sum(emission_counts[tag].values())
        for word in emission_counts[tag]:
            emission_probs[tag][word] = emission_counts[tag][word] / total

    return transition_probs, emission_probs


if __name__ == "__main__":
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

    trans_probs, emit_probs = hidden_markov(sentences)

    print("Transition Probabilities")
    pprint.pprint(dict(trans_probs))

    print("\nEmission Probabilities")
    pprint.pprint(dict(emit_probs))
