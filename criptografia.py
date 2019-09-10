import requests
import hashlib
import json

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def get_data():
        url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=31fb27ed1ac4ec8c0396053395bc1892b7c12179'
        r = requests.get(url)
        content = json.loads(r.content)
        return content

def send_data():
        url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=31fb27ed1ac4ec8c0396053395bc1892b7c12179'
        files = {'answer': ('answer.json', open('./answer.json','rb'), 'multipart/form-data')}
        r = requests.post(url, files=files)
        return r

def write_file(content):
        with open('./answer.json', 'w') as f:
                f.write(json.dumps(content))

def cesar_cipher(phrase, key):
        conversion = ''
        
        for i in phrase:
                if i in alphabet:
                        position = alphabet.index(i)
                        conversion += alphabet[(position + key) % len(alphabet)]
                else:
                        conversion += i
        
        return conversion

def hash_sha1(text):
        h = hashlib.sha1()
        h.update(text.encode('utf-8'))
        return h.hexdigest()

def main():
    data = get_data()
    write_file(data)

    decrypt = cesar_cipher(data['cifrado'], -data['numero_casas'])
    data['decifrado'] = decrypt
    write_file(data)

    sha1 = hash_sha1(decrypt)
    data['resumo_criptografico'] = sha1
    write_file(data)

    response = send_data()
    print(response.text)

if __name__ == '__main__':
    main()
