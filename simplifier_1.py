import gensim
import pandas as pd
from nltk.corpus import brown
from nltk.probability import *
from nltk.corpus import wordnet
from nltk import sent_tokenize, word_tokenize, pos_tag

def generate_freq_dict():
    """ Create frequency dictionary based on BROWN corpora. """
    freq_dict = FreqDist()
    for sentence in brown.sents():
        for word in sentence:
            freq_dict[word] += 1
    return freq_dict

class Simplifier1:
    def __init__(self):
        # Load ngrams frequency dictionary
        ngrams = pd.read_csv('ngrams.csv')
        ngrams = ngrams.drop_duplicates(subset='bigram', keep='first')

        self.ngram_freq_dict = dict(zip(ngrams.bigram, ngrams.freq))
        self.freq_dict = generate_freq_dict()

        self.steps = open('steps.txt', 'w')

    def return_bigram_score(self, context, token, replacement):
        """ Return ad averaged frequency of left- and right-context bigram. """
        score = 0
        if (context[0] + ' ' + replacement).lower() in self.ngram_freq_dict.keys():
            score += self.ngram_freq_dict[(context[0] + ' ' + replacement).lower()]
        if (replacement + ' ' + context[2]).lower() in self.ngram_freq_dict.keys():
            score += self.ngram_freq_dict[(replacement + ' ' + context[2]).lower()]
        return score / 2

    def check_if_word_fits_the_context(self, context, token, replacement):
        """ Check if bigram with the replacement exists. """
        if len(context) == 3:
            if (context[0] + ' ' + replacement).lower() in self.ngram_freq_dict.keys():
                return True
            if (replacement + ' ' + context[2]).lower() in self.ngram_freq_dict.keys():
                return True
            else:
                return False
        else:
            return False
    
    def check_if_replacable(self, word):
        """ Check POS, we only want to replace nouns, adjectives and verbs. """
        word_tag = pos_tag([word])
        if 'NN' in word_tag[0][1] or 'JJ' in word_tag[0][1] or 'VB' in word_tag[0][1]:
            return True
        else:
            return False
    
    def check_pos_tags(self, sent, token_id, replacement):
        old_tag = pos_tag(sent)[token_id][1]
        sent[token_id] = replacement
        new_tag = pos_tag(sent)[0][1]
        if new_tag == old_tag:
            return True
        else:
            return False

    def generate_wordnet_candidates(self, word):
        """ Generate wordnet candidates for each word in input. """
        candidates = set()
        if self.check_if_replacable(word):
            for synset in wordnet.synsets(word):
                for lemma in synset.lemmas():
                    converted =lemma.name().lower()
                    if converted != word and converted != None:
                        candidates.add(converted)

        return candidates
    
    def simplify(self, input):
        simplified = ''

        sent = input
        # Top N most frequent words we never replace
        top_n = 3000
        freq_top_n = sorted(self.freq_dict.values(), reverse=True)[top_n - 1]

        self.steps.write(sent + '\n')
        tokens = word_tokenize(sent)  # Split a sentence by words

        # Find difficult words - long and infrequent
        difficultWords = [t for t in tokens if self.freq_dict[t] < freq_top_n]
        self.steps.write('difficultWords:' + str(difficultWords) + '\n')

        all_options = {}
        for difficultWord in difficultWords:
            replacement_candidate = {}
             # 2. Generate candidates
            for option in self.generate_wordnet_candidates(difficultWord):
                replacement_candidate[option] = self.freq_dict.freq(option)
            # 2.1. Replacement options with frequency
            all_options[difficultWord] = replacement_candidate
        self.steps.write('all_options:' + str(all_options) + '\n')

        # 2.2. Replacement options with bigram score
        best_candidates = {}
        for token_id in range(len(tokens)):
            token = tokens[token_id]
            best_candidates[token] = {}
            if token in all_options:
                for opt in all_options[token]:
                    if token_id != 0 and token_id != len(tokens):  # if not the first or the last word in the sentence
                        if self.check_if_word_fits_the_context(tokens[token_id - 1:token_id + 2], token, opt):
                            # Return all candidates with its bigram scores
                            best_candidates[token][opt] = self.return_bigram_score(tokens[token_id - 1:token_id + 2], token, opt)
        self.steps.write('best_candidates:' + str(best_candidates) + '\n')

        simplified0 = ''
         # 3. Generate replacements1 - take the word with the highest frequency + check the context
        output = []
        for token in tokens:
            if token in best_candidates:
                if token.istitle() is False and best_candidates[token] != {}:
                    # Choose the one with the highest bigram score
                    best = max(best_candidates[token], key=lambda i: best_candidates[token][i])
                    self.steps.write('best v1:' + str(token) + ' -> ' + str(best) + '\n')
                    output.append(best)
                else:
                    output.append(token)
            else:
                output.append(token)
        # print('v0', ' '.join(output))
        simplified0 += ' '.join(output)
        print(simplified0)
        return simplified0

if __name__ == '__main__':
    S=Simplifier1()
    S.simplify("We slept in what had once been the gymnasium.")