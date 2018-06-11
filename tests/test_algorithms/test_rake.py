import math

from multilang_rake import Rake


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

    text = (
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

    result = rake.apply(text)

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

    for i in range(len(result)):
        assert result[i][0] == expected[i][0]
        assert math.isclose(result[i][1], expected[i][1])

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

    result = rake.apply(text)

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

    for i in range(len(result)):
        assert result[i][0] == expected[i][0]
        assert math.isclose(result[i][1], expected[i][1])
