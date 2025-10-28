import random
import json

FIRST_PERSON_SING_INDEX = 0
SECOND_PERSON_SING_INDEX = 1
THIRD_PERSON_SING_INDEX = 2
FIRST_PERSON_PLUR_INDEX = 3
SECOND_PERSON_PLUR_INDEX = 4
THIRD_PERSON_PLUR_INDEX = 5

def get_conjugation_index(pronoun):
    '''Pass in a pronoun. From that pronoun, return the matching conjugation index.
    This is used to conjugate verbs later on.

    If this function doesn't raise any ValueErrors if pronoun is an invalid data type,
    like str. This is because it automatically returns THIRD_PERSON_PLUR_INDEX if the
    pronun doesn't match the others, regardless of type.'''
    conj_index = 0
    if pronoun == "je":
        conj_index = FIRST_PERSON_SING_INDEX
    elif pronoun == "tu":
        conj_index = SECOND_PERSON_SING_INDEX
    elif pronoun == "il" or pronoun == "elle" or pronoun == "on":
        conj_index = THIRD_PERSON_SING_INDEX
    elif pronoun == "nous":
        conj_index = FIRST_PERSON_PLUR_INDEX
    elif pronoun == "vous":
        conj_index = SECOND_PERSON_PLUR_INDEX
    else:
        conj_index = THIRD_PERSON_PLUR_INDEX
    return conj_index

def conjugate_verb(verbs_dict, verb_key, conj_index):
    '''Passes in the verb dictionary and the verb key, along with the conjugation index.
    These values will tell the program how to conjugate the verb. The verb will be conjugated
    accordingly and returned.'''
    verb_conj = verbs_dict[verb_key][conj_index]
    return verb_conj

def choose_object_noun(masculine_dict, feminine_dict, verb_key):
    '''From a list of masculine and feminine nouns, choose a random noun and return it.
    This function:
        1) Generates a random gender between masculine and feminine.
        2) Chooses a random noun of that gender, from the list provided by the verb. <--this hasn't been done yet
        3) returns the noun, combined with its article.
        '''
    gender = random.choice(("masc", "fem"))
    if gender == "masc": # Use the verb key to pick a random noun. # masculine_dict[verb_key] returns the list of nouns.
        # Choose a random noun from the specified gender list, that matches the verb.
        object_noun = random.choice(masculine_dict[verb_key])
        # If the verb is pouvoir, parler, or aller, it should not have an article.
        if verb_key not in list(("pouvoir", "parler", "aller")):
            object_noun = f"un {object_noun}"
    else:
        # Same code from before.
        object_noun = random.choice(feminine_dict[verb_key])
        if verb_key not in list(("pouvoir", "parler", "aller")):
            object_noun = f"une {object_noun}"
    
    return object_noun

def choose_verb(pronoun):
    '''From the dictionary of verbs, choose a random key, which corresponds to a verb.
    Conjugate that verb according to the pronoun passed in. Return the conjugated
    verb and its verb key (infinitive form).'''
    
    data = extract_data("french.json") # Extract data
    
    verb_key = random.choice(data[VERB_KEYS_INDEX]) # Choose a random verb to act as the "verb key".
    verb_dictionary = data[VERBS_DICT_INDEX]

    conj_index = get_conjugation_index(pronoun) # Conjugate and return the verb and its key.
    verb = conjugate_verb(verb_dictionary, verb_key, conj_index)
    return verb, verb_key

def make_sentence(pronoun, verb, object_noun, vowels):
    '''Input: A pronoun, a verb, an object noun (all strings), and a list of vowels.
    Return: A formatted string of the pronoun, verb, and object noun ordered in a sentence.
    If the pronoun is "je" and the verb starts with a vowel, change "je" to " je' " and
    alter its placement in the sentence. Return the sentence.'''
    if verb[0] in vowels and pronoun == "je":
        pronoun = "j'"
        sentence = f"{pronoun}{verb} {object_noun}".capitalize()
        return sentence
    sentence = f"{pronoun} {verb} {object_noun}".capitalize()
    return sentence

def passe_compose(verb_key, passe_list, pronoun, verb_dict):
    '''Passes in a verb key (infinitive form), and returns its passe compose form with the avoir construction.
    If the verb key is aller, return the passe compose form with the être construction.'''
    new_verb = passe_list[verb_key]
    conjugat_index = get_conjugation_index(pronoun)
    if verb_key == "aller":
        etre_form = verb_dict["être"][conjugat_index]
        if pronoun in ("nous", "vous", "ils"):
            # Handles "Les accords" when the pronoun is plural.
            new_verb = f"{etre_form} {new_verb}s"
            return new_verb
        elif pronoun == "elle":
            # Handles les accords when the pronoun is feminine singular.
            new_verb = f"{etre_form} {new_verb}e"
            return new_verb
        elif pronoun == "elles":
            # Handles les accords when the pronoun is feminine plural
            new_verb = f"{etre_form} {new_verb}es"
            return new_verb
        # If there are no accords to make, return the normal verbs.
        new_verb = f"{etre_form} {new_verb}"
        return new_verb
    # If the verb is not an être verb, just return the normal construction.
    avoir_form = verb_dict["avoir"][conjugat_index]
    new_verb = f"{avoir_form} {new_verb}"
    return new_verb

def imparfait(verb_key, imparfait_list, pronoun):
    '''This function passes in a verb key, the list of imparfait verbs, and the pronoun
    of the sentence. It changes the desired verb into its imparfait form, conjugated to match
    its pronoun. The new verb construction is returned.'''
    imparfait_conjugations = imparfait_list[verb_key] # Returns the list of imparfait forms for the chosen verb.
    conj_index = get_conjugation_index(pronoun) # Returns the conjugation index of the pronoun
    imparfait_form = imparfait_conjugations[conj_index]
    return imparfait_form

def read_data(file):
    '''Taking a file as input, read the json file into a dictionary using the json module.
    Return the dictionary.'''
    with open(file, "rt", encoding="utf-8") as filehandle: # Thank you to ChatGPT for pointing out that I should use encoding="utf-8", or else the unicode accented characters would break. That probably saved me at least an hour of work.
        # Read the json file into dictionaries for pronouns and verbs
        data = filehandle.read()
        words_data = json.loads(data)

    return words_data

def extract_data(file):
    '''This function takes a file, calls read_data to read it into a dictionary, then
    saves each list or dictionary as a separate variable. These variables are all returned
    in a tuple, which can then be pulled from in other functions.
    
    This function's purpose is to cut down on how much data is passed in as parameters.'''
    words_data = read_data(file)

    pronouns = words_data["pronouns"]
    verbs_dict = words_data["verbs"]
    verb_keys = list(verbs_dict.keys()) # Make a list of verb keys (verbs in infinitive forms)
    vowels = words_data["vowels"]
    nouns_masculine = words_data["nouns"]["masculine"]
    nouns_feminine = words_data["nouns"]["feminine"]
    verbs_passe_compose = words_data["verbs-passe-compose"]
    verbs_imparfait = words_data["verbs-imparfait"]

    return pronouns, verbs_dict, verb_keys, vowels, nouns_masculine, nouns_feminine, verbs_passe_compose, verbs_imparfait

# def check_task(user_sentence, correct_sentence):
#     correct = user_sentence.lower() == correct_sentence.lower()
#     return correct

PRONOUNS_INDEX = 0
VERBS_DICT_INDEX = 1
VERB_KEYS_INDEX = 2
VOWELS_INDEX = 3
NOUNS_MASCULINE_INDEX = 4
NOUNS_FEMININE_INDEX = 5
VERBS_PASSE_COMPOSE_INDEX = 6
VERBS_IMPARFAIT_INDEX = 7

def main():
    # Read the json data into a dictionary.
    
    data = extract_data("french.json")
    # Unpack the various dictionaries from french.json.
    
    # Choose a random pronoun, verb, and object noun.
    pronoun = random.choice(data[PRONOUNS_INDEX])
    
    verb, verb_key = choose_verb(pronoun)
    verb_passe = passe_compose(verb_key, data[VERBS_PASSE_COMPOSE_INDEX], pronoun, data[VERBS_DICT_INDEX])
    verb_imparfait = imparfait(verb_key, data[VERBS_IMPARFAIT_INDEX], pronoun)

    object_noun = choose_object_noun(data[NOUNS_MASCULINE_INDEX], data[NOUNS_FEMININE_INDEX], verb_key)

    tasks = ["present-passe", "present-imparfait"] # , "passe-present", "passe-imparfait", "imparfait-present", "imparfait-passe"
    task = random.choice(tasks)

    # Make a sentence with the new words and print it.
    sentence = make_sentence(pronoun, verb, object_noun, data[VOWELS_INDEX])
    sentence_passe = make_sentence(pronoun, verb_passe, object_noun, data[VOWELS_INDEX])
    sentence_imparfait = make_sentence(pronoun, verb_imparfait, object_noun, data[VOWELS_INDEX])
    
    # Set the correct sentence and instructions, based on whichever task was chosen.
    if task == "present-passe":
        correct_sentence = sentence_passe
        print("Please change the following sentence from present tense to PASSÉ COMPOSÉ.")
    elif task == "present-imparfait":
        correct_sentence = sentence_imparfait
        print("Please change the following sentence from present tense to IMPARFAIT.")
    print(sentence)

    # Answer loop. So long as the user has not entered a correct answer, prompt the user
    # to enter a sentence again.
    correct = False
    user_sentence = input("Your answer: ") # This line feels redundant but IDK how to remove it.
    while not correct:
        correct = user_sentence.lower() == correct_sentence.lower()
        if correct:
            print("Correct!")
        else:
            print("Try again!")
            user_sentence = input("Your answer: ")

if __name__ == "__main__":
    main()