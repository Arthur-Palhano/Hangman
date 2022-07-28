import requests, json, os, random
from translate import Translator

t = Translator(to_lang="pt")

URL = "https://hangman-api.herokuapp.com/hangman"

def hit():input('Tecle ENTER para continuar...')

def new_game():
    req = json.loads(requests.post(URL).text)
    TOKEN = req['token']
    AWNSER = json.loads(requests.get(URL + '', params={'token': TOKEN}).text)['solution']
    if len(req['hangman']) > 8 or t.translate(AWNSER).lower() == AWNSER.lower():
        return new_game()
    else:
        return req

def slice_letters(txt):
    _txt = []
    _txt[:0] = txt
    return _txt

def normalize_letters(a):
    if a in ['á', 'à', 'ã', 'â']:
        return 'a'
    if a in ['é', 'è', 'ẽ', 'ê']:
        return 'e'
    if a in ['ó', 'õ', 'ô']:
        return 'o'
    if a in ['í', 'ì', 'î', 'ĩ']:
        return 'i'
    if a in ['ú', 'ù', 'ũ', 'û']:
        return 'u'
    if a in ['ç']:
        return 'c'
    return a

def add_to_word(word, hangman):
    word = slice_letters(word)
    hangman = slice_letters(hangman)

    for _ in range(0, len(word)):
        if hangman[_] != '_':
            word[_] = hangman[_]

    return ''.join(word)

def is_correct(letter, awnser):
    B_awnser = slice_letters(awnser)
    awnser = slice_letters(awnser)
    hangman = ""
    correct = False

    for l in range(0, len(awnser)):
        awnser[l] = normalize_letters(awnser[l])

    if letter in awnser:
        correct = True
        for _ in range(0, len(awnser)):
            if awnser[_] == letter:
                hangman += B_awnser[_]
                used_letters.append(B_awnser[_])
            elif awnser[_] == ' ':
                hangman += ' '
            else:
                hangman += "_"
    else:
        used_letters.append(letter)
    return {'correct': correct, 'hangman': hangman}

os.system('cls' if os.name == 'nt' else 'clear')

NEW_GAME = new_game()

TOKEN = NEW_GAME['token']
used_letters = [' ']
AWNSER = t.translate(json.loads(requests.get(URL, params={'token': TOKEN}).text)['solution']).lower()
word = slice_letters('_' * len(AWNSER))

for _ in word:
    if _ == '-' or _ == ' ':
        _ = ' '
    elif not _.isalpha():
        _ = ""
word = ''.join(word)

label = 'Uma dica aparecerá aqui após 3 tentativas.'

def get_hint():
    hint = " "
    while hint in used_letters:
        hint = random.choice(AWNSER)
    return hint

chances = 8

while chances != 0:
    print(label)
    print()
    print(word)
    print('Número de tentativas: ', chances)
    print()
    letter = input('Adivinhe uma letra: ').lower()

    if len(letter) != 1 or not letter.isalpha():
        print('Por favor, tecle uma letra válida.')
        hit()
    elif letter in used_letters:
        print('Você já tentou esse letra.')
        hit()
    else:
        res = is_correct(letter, AWNSER)
        if res['correct']:
            word = add_to_word(word, res['hangman'])

            if word.lower() == AWNSER.lower():
                os.system('cls' if os.name == 'nt' else 'clear')
                print('A palavra é: ' + AWNSER)
                print()
                print('Você venceu!')
                hit()
                break
        else:
            chances -= 1

            if chances == 5 :
                label = "A palavra tem a letra " + get_hint()

            if chances == 0:
                print()
                print('Fim de jogo')
                print(f'A resposta era: {AWNSER}')
                hit()

    os.system('cls' if os.name == 'nt' else 'clear')
