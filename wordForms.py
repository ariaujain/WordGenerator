#finds all the word forms of a given word

import inflect
from word_forms.word_forms import get_word_forms

p = inflect.engine()

def getAllForms(word):
    wordForms = get_word_forms(word)
    all_forms = set()
    sameWord = set()

    # Check and add verb forms
    if 'v' in wordForms:
        for form in wordForms['v']:
            all_forms.add(form)
            if not form.startswith(word[0:1]):
                break
            else:
                sameWord.add(form)

    # Check and add noun forms
    if 'n' in wordForms:
        for form in wordForms['n']:
            all_forms.add(form)
            if (form.startswith(word[0:len(word)-2]) and form.endswith('ing')):
                sameWord.add(form)
            if (form == word + 's' or form.endswith("ies")):
                sameWord.add(form)

    # Check and add adjective forms
    if 'a' in wordForms:
        for form in wordForms['a']:
            all_forms.add(form)
            if (form.startswith(word[0:len(word)-2]) and form.endswith('s')):
                sameWord.add(form)

    # Check and add adverb forms
    if 'r' in wordForms:
        for form in wordForms['r']:
            all_forms.add(form)
            if (form.startswith(word)):
                sameWord.add(form)


    return all_forms, sameWord


words = []

all_filtered_forms = {}
for word in words:
    allForms, sameWord = getAllForms(word)


