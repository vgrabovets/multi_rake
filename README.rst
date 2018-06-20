Multilingual Rapid Automatic Keyword Extraction (RAKE)
======================================================

Features
--------
- Automatic keyword extraction from text written in any language
- No need to know language of text beforehand
- No need to have list of stopwords
- 26 languages are currently available, for the rest - stopwords are generated from provided text
- Just configure rake, plug in text and get keywords (see implementation details)

Installation
------------
.. code-block:: bash

    pip install multi-rake

Examples
--------
English text, we don't specify explicitly language nor list of stopwords (built-in list is used).

.. code-block:: python

    text_en = (
        'Compatibility of systems of linear constraints over the set of '
        'natural numbers. Criteria of compatibility of a system of linear '
        'Diophantine equations, strict inequations, and nonstrict inequations '
        'are considered. Upper bounds for components of a minimal set of '
        'solutions and algorithms of construction of minimal generating sets '
        'of solutions for all types of systems are given. These criteria and '
        'the corresponding algorithms for constructing a minimal supporting '
        'set of solutions can be used in solving all the considered types of '
        'systems and systems of mixed types.'
    )

    rake = Rake()

    keywords = rake.apply(text_en)

    print(keywords[:10])

    #  ('minimal generating sets', 8.666666666666666),
    #  ('linear diophantine equations', 8.5),
    #  ('minimal supporting set', 7.666666666666666),
    #  ('minimal set', 4.666666666666666),
    #  ('linear constraints', 4.5),
    #  ('natural numbers', 4.0),
    #  ('strict inequations', 4.0),
    #  ('nonstrict inequations', 4.0),
    #  ('upper bounds', 4.0),
    #  ('mixed types', 3.666666666666667),


Text written in Esperanto (article about `liberalism <https://eo.wikipedia.org/wiki/Liberalismo>`_).
There is no list of stopwords for this language, they will be generated from provided text.

:code:`text` consists of three first paragraphs of introduction. :code:`text_for_stopwords` - all other text.

.. code-block:: python

    text = (
        'Liberalismo estas politika filozofio aŭ mondrigardo konstruita en '
        'ideoj de libereco kaj egaleco. Liberaluloj apogas larĝan aron de '
        'vidpunktoj depende de sia kompreno de tiuj principoj, sed ĝenerale '
        'ili apogas ideojn kiel ekzemple liberaj kaj justaj elektoj, '
        'civitanrajtoj, gazetara libereco, religia libereco, libera komerco, '
        'kaj privata posedrajto. Liberalismo unue iĝis klara politika movado '
        'dum la Klerismo, kiam ĝi iĝis populara inter filozofoj kaj '
        'ekonomikistoj en la okcidenta mondo. Liberalismo malaprobis heredajn '
        'privilegiojn, ŝtatan religion, absolutan monarkion kaj la Didevena '
        'Rajto de Reĝoj. La filozofo John Locke de la 17-a jarcento ofte '
        'estas meritigita pro fondado de liberalismo kiel klara filozofia '
        'tradicio. Locke argumentis ke ĉiu homo havas naturon rekte al vivo, '
        'libereco kaj posedrajto kaj laŭ la socia '
        'kontrakto, registaroj ne rajtas malobservi tiujn rajtojn. '
        'Liberaluloj kontraŭbatalis tradician konservativismon kaj serĉis '
        'anstataŭigi absolutismon en registaroj per reprezenta demokratio kaj '
        'la jura hegemonio.'
    )

    rake = Rake(max_words_unknown_lang=3)

    keywords = rake.apply(text, text_for_stopwords=other_text)

    print(keywords)

    #  ('serĉis anstataŭigi absolutismon', 9.0)  # sought to replace absolutism
    #  ('filozofo john locke', 8.5),  # philosopher John Locke
    #  ('locke argumentis', 4.5)  # Locke argues
    #  ('justaj elektoj', 4.0),  # fair elections
    #  ('libera komerco', 4.0),  # free trade
    #  ('okcidenta mondo', 4.0),  # western world
    #  ('ŝtatan religion', 4.0),  # state religion
    #  ('absolutan monarkion', 4.0),  # absolute monarchy
    #  ('didevena rajto', 4.0),  # Dominican Rights
    #  ('socia kontrakto', 4.0),  # social contract
    #  ('jura hegemonio', 4.0),  # legal hegemony
    #  ('mondrigardo konstruita', 4.0)  # worldview built
    #  ('vidpunktoj depende', 4.0),  # views based
    #  ('sia kompreno', 4.0),  # their understanding
    #  ('tiuj principoj', 4.0),  # these principles
    #  ('gazetara libereco', 3.5),  # freedom of press
    #  ('religia libereco', 3.5),  # religious freedom
    #  ('privata posedrajto', 3.5),  # private property
    #  ('libereco', 1.5),  # liberty
    #  ('posedrajto', 1.5)]  # property

So, we are able to get decent result without explicit set of stopwords.

Usage
-----
Initialize rake object

.. code-block:: python

    from multi_rake import Rake

    rake = Rake(
        min_chars=3,
        max_words=3,
        min_freq=1,
        language_code=None,  # 'en'
        stopwords=None,  # {'and', 'of'}
        lang_detect_threshold=50,
        max_words_unknown_lang=2,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    )

**min_chars** - word is selected to be part of keyword if its length is >= min_chars. *Default 3*

**max_words** - maximum number of words in phrase considered to be a keyword. *Default 3*

**min_freq** - minimum number of occurences of a phrase to be considered a keyword. *Default 1*

**language_code** - provide language code as string to use built-in set of stopwords. See list of available languages. If language is not specified algorithm will try to determine language with `cld2 <https://pypi.org/project/cld2-cffi/>`_ and use corresponding set of built-in stopwords. *Default None*

**stopwords** - provide own collection of stopwords (preferably as set, lowercased). Overrides :code:`language_code` if it was specified. *Default None*

Keep :code:`language_code` and :code:`stopwords` as :code:`None` and stopwords will be generated from provided text.

**lang_detect_threshold** - threshold for probability of detected language in `cld2 <https://pypi.org/project/cld2-cffi/>`_ (0-100). *Default 50*

**max_words_unknown_lang** - the same as :code:`max_words` but will be used if language is unknown and stopwords are generated from provided text. Usually the best result is obtained when specifically crafted set of stopwords is used, in case of its absence and usage of generated stopwords resulting keywords may not be as pretty and it may be good idea, for example, to produce 2-word keywords for unknown languages and 3-word keywords for languages with predefined sets of stopwords. *Default 2*

**generated_stopwords_percentile** - to generate stopwords we create distribution of every word in text by frequency. Words above this percentile (0 - 100) will be considered candidates to become stopwords. *Default 80*

**generated_stopwords_max_len** - maximum character length of generated stopwords. *Default 3*

**generated_stopwords_min_freq** - minimum frequency of generated stopwords in the distribution. *Default 2*

|

Apply rake object to text.

.. code-block:: python

    keywords = rake.apply(
        text,
        text_for_stopwords=None,
    )

**text** - string containing text from which keywords should be generated.

**text_for_stopwords** - string containing text which will be used for stopwords generation alongside :code:`text`. For example, you have article with introduction and several subsections. You know that for your purposes keywords from introduction will suffice, you don't know language of text nor you have list of stopwords. So stopwords can be generated from text itself and the more text you have, the better. Than you may specify :code:`text=introduction, text_for_stopwords=rest_of_your_text`.

Implementation Details
----------------------
RAKE algorithm works as described in Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons

This implementation is different from others by its multilingual support.
Basically you may provide text without knowing its language (it should be written with cyrillic or latin alphabets),
without explicit list of stopwords and get decent result.
Though the best result is achieved with thoroughly constructed list of stopwords.

What is happening under the hood:

1) if stopwords are specified, then they will be used
2) if language is specified, then built-in stopwords for this language will be used, if there are no built-in stopwords --> 4
3) if language is not specified, then `cld2 <https://pypi.org/project/cld2-cffi/>`_ will try to determine language --> 2
4) stopwords are generated from :code:`text` and :code:`text_for_stopwords`

We generate stopwords by creating frequency distribution of words in text and filtering them with parameters :code:`generated_stopwords_percentile`, :code:`generated_stopwords_max_len`, :code:`generated_stopwords_min_freq`. We won't be able to generate them perfectly but it is rather easy to find articles and prepositions, because usually they consist of 3-4 characters and appear frequently. These stopwords, coupled with punctuation delimiters, enable us to get decent results for languages we don't understand.

List of Currently Available Languages
-------------------------------------
During RAKE initialization only language code should be used.

- bg - Bulgarian
- cs - Czech
- da - Danish
- de - German
- el - Greek
- en - English
- es - Spanish
- fi - Finnish
- fr - French
- ga - Irish
- hr - Croatian
- hu - Hungarian
- id - Indonesian
- it - Italian
- lt - Lithuanian
- lv - latvian
- nl - Dutch
- no - Norwegian
- pl - Polish
- pt - Portuguese
- ro - Romanian
- ru - Russian
- sk - Slovak
- sv - Swedish
- tr - Turkish
- uk - Ukrainian

Development
----------------------------
Repository has configured linter, tests and coverage.

Create new virtual environment in order to use it.

.. code-block:: bash

    virtualenv env
    source env/bin/activate

    make install-dev  # install dependencies

    make lint  # run linter

    make test  # run tests and coverage

References
----------
RAKE algorithm: Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons

As a basis RAKE implementation by `fabianvf <https://github.com/fabianvf/python-rake>`_ was used.

Stopwords: `trec-kba <https://github.com/trec-kba/many-stop-words/tree/master/orig>`_, `Ranks NL <https://www.ranks.nl/stopwords>`_
