import random
import pytest
from french_practice import get_conjugation_index, make_sentence, choose_verb, read_data, \
    choose_object_noun, passe_compose

def test_conjugate_verb():
    assert get_conjugation_index("je") == 0
    assert get_conjugation_index("tu") == 1
    assert get_conjugation_index("il") == 2
    assert get_conjugation_index("elle") == 2
    assert get_conjugation_index("on") == 2
    assert get_conjugation_index("nous") == 3
    assert get_conjugation_index("vous") == 4
    assert get_conjugation_index("ils") == 5
    assert get_conjugation_index("elles") == 5

def test_choose_object_noun():
    pass

def test_choose_verb():
    words_data = read_data("french.json")
    verbs_dict = words_data["verbs"]
    verb_keys = list(verbs_dict.keys())
    
    random.seed(42) # Found this from Google's AI Overview
    result = choose_verb(verbs_dict, "tu")
    assert result == ("vois", "voir")
    
    random.seed(76)
    assert choose_verb(verbs_dict, "tu") == ("fais", "faire")

def test_make_sentence():
    vowels = ["a", "e", "i", "o", "u", "h"]
    assert make_sentence("je", "ai", "un livre", vowels) == "J'ai un livre"
    assert make_sentence("elles", "peuvent", "gagner", vowels) == "Elles peuvent gagner"
    assert make_sentence("on", "a", "une question", vowels) == "On a une question"

def test_passe_compose():
    words_data = read_data("french.json")
    verbs_dict = words_data["verbs"]
    verb_keys = list(verbs_dict.keys())
    verbs_passe_compose = words_data["verbs-passe-compose"]
    pronouns = words_data["pronouns"]
    
    random.seed(42)
    pronoun = random.choice(pronouns)
    verb, verb_key = choose_verb(verbs_dict, pronoun)
    assert passe_compose(verb_key, verbs_passe_compose, pronoun, verbs_dict) == "as été"
    assert passe_compose("entendre", verbs_passe_compose, "tu", verbs_dict) == "as entendu"



# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])