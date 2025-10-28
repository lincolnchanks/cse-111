import random
import pytest
from french_practice import get_conjugation_index, make_sentence, choose_verb, \
    choose_object_noun, passe_compose, extract_data, conjugate_verb, imparfait

def test_get_conjugation_index():
    assert get_conjugation_index("je") == 0
    assert get_conjugation_index("tu") == 1
    assert get_conjugation_index("il") == 2
    assert get_conjugation_index("elle") == 2
    assert get_conjugation_index("on") == 2
    assert get_conjugation_index("nous") == 3
    assert get_conjugation_index("vous") == 4
    assert get_conjugation_index("ils") == 5
    assert get_conjugation_index("elles") == 5

def test_conjugate_verb():
    data = extract_data("french.json")
    assert conjugate_verb("être", 0, data) == "suis"
    assert conjugate_verb("être", 1, data) == "es"
    assert conjugate_verb("être", 2, data) == "est"
    assert conjugate_verb("être", 3, data) == "sommes"
    assert conjugate_verb("être", 4, data) == "êtes"
    assert conjugate_verb("être", 5, data) == "sont"
    assert conjugate_verb("avoir", 0, data) == "ai"
    assert conjugate_verb("avoir", 1, data) == "as"
    assert conjugate_verb("avoir", 2, data) == "a"
    assert conjugate_verb("avoir", 3, data) == "avons"
    assert conjugate_verb("avoir", 4, data) == "avez"
    assert conjugate_verb("avoir", 5, data) == "ont"
    assert conjugate_verb("entendre", 0, data) == "entends"
    assert conjugate_verb("entendre", 1, data) == "entends"
    assert conjugate_verb("entendre", 2, data) == "entend"
    assert conjugate_verb("entendre", 3, data) == "entendons"
    assert conjugate_verb("entendre", 4, data) == "entendez"
    assert conjugate_verb("entendre", 5, data) == "entendent"

def test_choose_object_noun():
    data = extract_data("french.json")
    random.seed(42)
    assert choose_object_noun("entendre", data) == "un bruit"
    random.seed(76)
    assert choose_object_noun("entendre", data) == "une conversation"

def test_choose_verb():
    data = extract_data("french.json")
    
    random.seed(42) # Found this from Google's AI Overview
    assert choose_verb(data, "tu") == ("vois", "voir")
    
    random.seed(76)
    assert choose_verb(data, "tu") == ("fais", "faire")

def test_make_sentence():
    data = extract_data("french.json")
    assert make_sentence("je", "ai", "un livre", data) == "J'ai un livre"
    assert make_sentence("elles", "peuvent", "gagner", data) == "Elles peuvent gagner"
    assert make_sentence("on", "a", "une question", data) == "On a une question"

def test_passe_compose():
    data = extract_data("french.json")

    random.seed(42)
    pronoun = random.choice(data[0])

    verb_key = choose_verb(data, pronoun)[1]
    assert passe_compose(verb_key, pronoun, data) == "as été"
    assert passe_compose("entendre", "tu", data) == "as entendu"

def test_imparfait():
    data = extract_data("french.json")
    assert imparfait("entendre", "je", data) == "entendais"
    assert imparfait("entendre", "tu", data) == "entendais"
    assert imparfait("entendre", "il", data) == "entendait"
    assert imparfait("entendre", "elle", data) == "entendait"
    assert imparfait("entendre", "on", data) == "entendait"
    assert imparfait("entendre", "nous", data) == "entendions"
    assert imparfait("entendre", "vous", data) == "entendiez"
    assert imparfait("entendre", "ils", data) == "entendaient"
    assert imparfait("entendre", "elles", data) == "entendaient"
    assert imparfait("pouvoir", "je", data) == "pouvais"
    assert imparfait("pouvoir", "tu", data) == "pouvais"
    assert imparfait("pouvoir", "il", data) == "pouvait"
    assert imparfait("pouvoir", "elle", data) == "pouvait"
    assert imparfait("pouvoir", "on", data) == "pouvait"
    assert imparfait("pouvoir", "nous", data) == "pouvions"
    assert imparfait("pouvoir", "vous", data) == "pouviez"
    assert imparfait("pouvoir", "ils", data) == "pouvaient"
    assert imparfait("pouvoir", "elles", data) == "pouvaient"

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])