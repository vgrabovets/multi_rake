import cld2
import regex

LETTERS_RE = regex.compile(r'\p{L}+')

SENTENCE_DELIMITERS_RE = regex.compile(
    r'[\.,;:¡!¿\?…⋯‹›«»\\"“”\[\]\(\)⟨⟩}{&]'  # any punctuation sign or &
    r'|\s[-–~]+\s',  # or '-' between spaces
    regex.VERBOSE,
)


def detect_language(text, proba_threshold):
    """Detect language code and probability of input text based on 'cld2'.
    
    Parameters
    ----------
    text : utf8Bytes
        Text to detect language as unicode.
    proba_threshold : float
        Minimum probability cld2 language detection has to output in order to accept proposed language code.
    
    Returns
    -------
    str
        Language code detected by cld2.
    """
    _, _, details = cld2.detect(text)

    language_code = details[0].language_code
    probability = details[0].percent

    if language_code != 'un' and probability > proba_threshold:
        return language_code


def keep_only_letters(text):
    """Apply regex to only keep letters.
    
    Parameters
    ----------
    text : str
        Text to search for letters in.
    
    Returns
    -------
    str
        Input text cleaned by regex to only contain letters.
    """
    return ' '.join(token.group() for token in LETTERS_RE.finditer(text))


def separate_words(text):
    """Seperate text to tokens by whitespace and dimiss numeric tokens.
    
    Parameters
    ----------
    text : str
        Text to tokenize.
    
    Returns
    -------
    list of str
        Tokenized text.
    """
    words = []

    for word in text.split():
        if not word.isnumeric():
            words.append(word)

    return words


def split_sentences(text):
    """Split text into sentences with custom regex boundaries.
    
    Parameters
    ----------
    text : str
        Text to split on sentence delimiters.
    
    Returns
    -------
    list of str
        Text split into sentences.
    """
    sentences = SENTENCE_DELIMITERS_RE.split(text)
    return sentences
