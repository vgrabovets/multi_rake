import cld2
import regex

LETTERS_RE = regex.compile(r'\p{L}+')

SENTENCE_DELIMITERS_RE = regex.compile(
    r'[\.,;:¡!¿\?…⋯‹›«»\\"“”\[\]\(\)⟨⟩}{&]'  # any punctuation sign or &
    '|\s[-–~]+\s',  # or '-' between spaces
    regex.VERBOSE,
)


def detect_language(text, proba_threshold):
    _, _, details = cld2.detect(text)

    language_code = details[0].language_code
    probability = details[0].percent

    if language_code != 'un' and probability > proba_threshold:
        return language_code


def keep_only_letters(string):
    return ' '.join(token.group() for token in LETTERS_RE.finditer(string))


def separate_words(text):
    words = []

    for word in text.split():
        if not word.isnumeric():
            words.append(word)

    return words


def split_sentences(text):
    sentences = SENTENCE_DELIMITERS_RE.split(text)
    return sentences
