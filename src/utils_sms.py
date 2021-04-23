import spacy
from spacy.matcher import Matcher
nlp = spacy.load('es_core_news_lg')


def show_ents(sms):
    doc = nlp(sms)
    if doc.ents:
        for ent in doc.ents:
            print(ent.text+' - '+ent.label_+' - '+str(spacy.explain(ent.label_)))
    else:
        print('No named entities found.')

def language(sms):
    init_language = matcher(nlp(sms))

    spanish_flow = False
    english_flow = False

    if init_language  == 'Saludo_ES':
        case = 'español'
        spanish_flow =True
    elif init_language == 'Saludo_EN':
        case = 'ingles'
        english_flow = True
    else:
        case = 'no_saludo'

    return case, spanish_flow, english_flow

def matcher(sms):

    matcher = Matcher(nlp.vocab)

    spanish_pattern = [{'LOWER': 'hola'}, {'IS_PUNCT': False, 'OP': '*'}]
    english_pattern1 = [{'LOWER': 'hi'}, {'IS_PUNCT': False, 'OP': '*'}]
    english_pattern2 = [{'LOWER': 'hello'}, {'IS_PUNCT': False, 'OP': '*'}]
    # UDF{5}
    matcher.add('Saludo_ES', [spanish_pattern])
    matcher.add('Saludo_EN', [english_pattern1, english_pattern2 ])

    matcher_found = matcher(sms)
    string_id=''

    for match_id, start, end in matcher_found:
        string_id = nlp.vocab.strings[match_id]  # get string representation (Saludo_ES / Saludo_EN)

    return str(string_id)
