from os import listdir
from json import loads
from ast import literal_eval
from Crypto.PublicKey import RSA
from Crypto.Cipher import  PKCS1_OAEP

KS_paths = {
    'pub' : 'src/gs_api_credentials/pub.pem',
    'priv' : 'src/gs_api_credentials/priv.pem'
}
BIN_CREDENTIALS = 'src/gs_api_credentials/credentials_bin/'
ENCODING = 'utf-8'

def create_rsa_keys():
    '''
    Generates new RSA keys
    '''  
    key = RSA.generate(2048)
    public_k = key.publickey()
    with open(KS_paths['pub'],'wb') as f:
        f.write(public_k.exportKey('PEM'))
        f.close()
    with open(KS_paths['priv'],'wb') as f:
        f.write(key.exportKey('PEM'))
        f.close()


def mess_decrypt(message: bytes) -> str:
    '''
    Decrypts with RSA a given message
    '''
    privateKey = RSA.importKey(open(KS_paths['priv']).read())
    cipher = PKCS1_OAEP.new(privateKey)
    orgMsg = cipher.decrypt(message)
    return orgMsg.decode(ENCODING)


def mess_encrypt(message: str) -> bytes:
    '''
    Encrypts wth RSA a given message
    '''
    message = message.encode(ENCODING)
    key = RSA.importKey(open(KS_paths['pub']).read())
    cipher = PKCS1_OAEP.new(key)
    cryptMsg = cipher.encrypt(message)
    return cryptMsg


def get_current_credentials() -> dict:
    '''
    Function that returns google api credentials as dict
    '''
    
    bin_cred_parts = [BIN_CREDENTIALS+file for file in listdir(BIN_CREDENTIALS)]
    credentials = ''
    for f_name in sorted(bin_cred_parts):
        with open(f_name, 'rb') as f:
            credentials += mess_decrypt(f.read())
            f.close()
    return literal_eval(credentials)


def parted_string(string: str, n_char: int) -> list:
    '''Returns a given string parted as list every n_char'''
    return [string[i : i+n_char] for i in range(0, len(string), n_char)]


def update_json_conf(json_file: str):
    '''
    Saves securely google api json credentials
    '''
    create_rsa_keys()
    j_data = loads(open(json_file, 'r', encoding=ENCODING).read())
    str_j_data= str(j_data)
    parted_j_data = parted_string(str_j_data, 200)

    for i, string in enumerate(parted_j_data):
        index_part = '0'+str(i) if len(str(i))<=1 else str(i)
        part_f_name = BIN_CREDENTIALS+'cred_part_'+index_part+'.bin'
        with open(part_f_name, 'wb') as f:
            f.write(mess_encrypt(string))
            f.close()
    
    