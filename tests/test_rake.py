import pytest

from multi_rake import Rake


def test_rake():
    rake = Rake(
        min_chars=3,
        max_words=3,
        min_freq=1,
        lang_detect_threshold=50,
        max_words_unknown_lang=2,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    )
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
    result = rake.apply(text_en)
    result = _postprocess_result(result)
    expected = [
        ('minimal generating sets', 8.666666666666666),
        ('linear diophantine equations', 8.5),
        ('minimal supporting set', 7.666666666666666),
        ('minimal set', 4.666666666666666),
        ('linear constraints', 4.5),
        ('natural numbers', 4.0),
        ('strict inequations', 4.0),
        ('nonstrict inequations', 4.0),
        ('upper bounds', 4.0),
        ('mixed types', 3.666666666666667),
        ('considered types', 3.166666666666667),
        ('set', 2.0),
        ('types', 1.6666666666666667),
        ('considered', 1.5),
        ('compatibility', 1.0),
        ('systems', 1.0),
        ('criteria', 1.0),
        ('system', 1.0),
        ('components', 1.0),
        ('solutions', 1.0),
        ('algorithms', 1.0),
        ('construction', 1.0),
        ('constructing', 1.0),
        ('solving', 1.0),
    ]
    expected = _postprocess_result(expected)
    assert result == expected

    rake_en = Rake(
        min_chars=3,
        max_words=3,
        min_freq=1,
        language_code='en',
    )
    result = rake_en.apply(text_en)
    result = _postprocess_result(result)
    assert result == expected

    text_esperanto = (
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
    result = rake.apply(text_esperanto)
    result = _postprocess_result(result)
    expected = [
        ('vidpunktoj depende', 4.0),
        ('sia kompreno', 4.0),
        ('tiuj principoj', 4.0),
        ('justaj elektoj', 4.0),
        ('libera komerco', 4.0),
        ('okcidenta mondo', 4.0),
        ('ŝtatan religion', 4.0),
        ('absolutan monarkion', 4.0),
        ('didevena rajto', 4.0),
        ('socia kontrakto', 4.0),
        ('jura hegemonio', 4.0),
        ('gazetara libereco', 3.5),
        ('religia libereco', 3.5),
        ('privata posedrajto', 3.5),
        ('libereco', 1.5),
        ('posedrajto', 1.5),
        ('ideoj', 1.0),
        ('egaleco', 1.0),
        ('civitanrajtoj', 1.0),
        ('klerismo', 1.0),
        ('ekonomikistoj', 1.0),
        ('reĝoj', 1.0),
        ('laŭ', 1.0),
    ]
    expected = _postprocess_result(expected)
    assert result == expected

    rake_max_words_unknown_lang_none = Rake(
        min_chars=3,
        max_words=3,
        min_freq=1,
        lang_detect_threshold=50,
        max_words_unknown_lang=None,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    )
    result = rake_max_words_unknown_lang_none.apply(text_esperanto)
    result = _postprocess_result(result)
    expected = [
        ('filozofo john locke', 9.0),
        ('serĉis anstataŭigi absolutismon', 9.0),
        ('vidpunktoj depende', 4.0),
        ('sia kompreno', 4.0),
        ('tiuj principoj', 4.0),
        ('justaj elektoj', 4.0),
        ('libera komerco', 4.0),
        ('okcidenta mondo', 4.0),
        ('ŝtatan religion', 4.0),
        ('absolutan monarkion', 4.0),
        ('didevena rajto', 4.0),
        ('socia kontrakto', 4.0),
        ('jura hegemonio', 4.0),
        ('gazetara libereco', 3.5),
        ('religia libereco', 3.5),
        ('privata posedrajto', 3.5),
        ('libereco', 1.5),
        ('posedrajto', 1.5),
        ('ideoj', 1.0),
        ('egaleco', 1.0),
        ('civitanrajtoj', 1.0),
        ('klerismo', 1.0),
        ('ekonomikistoj', 1.0),
        ('reĝoj', 1.0),
        ('laŭ', 1.0),
    ]
    expected = _postprocess_result(expected)
    assert result == expected

    text_numbers = '123, 123, 123, 123'
    result = rake.apply(text_numbers)
    assert result == [('123', 0)]

    rake_min_freq2 = Rake(
        min_chars=3,
        max_words=3,
        min_freq=2,
        lang_detect_threshold=50,
        max_words_unknown_lang=2,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    )
    text_starts_with_stopword = (
        'and keywords... keywords are the best words'
    )
    result = rake_min_freq2.apply(text_starts_with_stopword)
    assert result == [('keywords', 1.0)]

    with pytest.raises(NotImplementedError):
        Rake(language_code='xxx')

    rake_uk = Rake(
        min_chars=3,
        max_words=4,
        min_freq=1,
        language_code='uk',
    )
    text_en_uk = (
        'Compatibility of systems of linear constraints над the set of '
        'natural numbers. Criteria of compatibility of a system of linear '
        'Diophantine equations, strict inequations, та nonstrict inequations '
        'are considered. Upper bounds для components of a minimal set of '
        'solutions та algorithms of construction of minimal generating sets '
        'of solutions для всіх types of systems are given. Ці criteria та '
        'the corresponding algorithms для constructing a minimal supporting '
        'set of solutions може бути used в solving всіх the considered types '
        'of systems та systems of mixed types.'
    )
    result = rake_uk.apply(text_en_uk)
    result = _postprocess_result(result)
    expected = [
        ('minimal set of solutions', 15.6),
        ('systems of mixed types', 15.6),
        ('nonstrict inequations are considered', 15.0),
        ('criteria of compatibility of', 13.7),
        ('the corresponding algorithms', 9.0),
        ('components of', 5.6),
        ('strict inequations', 5.0),
        ('upper bounds', 4.0),
        ('criteria', 2.5),
        ('constructing', 1.0),
        ('used', 1.0),
        ('solving', 1.0),
    ]
    expected = _postprocess_result(expected)
    assert result == expected


def _postprocess_result(result, round_digits=5):
    ret = set()

    for word, score in result:
        ret.add((word, round(score, round_digits)))

    return ret
