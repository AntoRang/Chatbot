from googletrans import  Translator

S_URLS = ['translate.google.com','translate.google.es']

def any_to_spanish(text: str) -> tuple:
    ''' Function that returns the spanish translation of a given text'''
    gt = Translator(service_urls=S_URLS)
    org_lang = str()
    try:
        org_lang = gt.detect(text).lang
        es_txt = str(gt.translate(text, src=org_lang, dest='es').text).lower() if org_lang != 'es' else text
        del gt
        return es_txt, org_lang
    except Exception:
        org_lang = 'es'
        del gt
        return text, org_lang


def spanish_to_any(text: str, any_lang:str ) -> str:
    ''' Function that returns the translated text of a given lang'''
    gt = Translator(service_urls=S_URLS)
    try:
        org_txt = gt.translate(text, src='es', dest=any_lang).text
        del gt
        return org_txt
    except Exception:
        del gt
        return text