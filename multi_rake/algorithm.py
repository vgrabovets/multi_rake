import operator
from collections import Counter, defaultdict

import numpy as np

from multi_rake.stopwords import STOPWORDS
from multi_rake.utils import (
    detect_language, keep_only_letters, separate_words, split_sentences,
)


class Rake:
    def __init__(
        self,
        min_chars=3,
        max_words=3,
        min_freq=1,
        language_code=None,
        stopwords=None,
        lang_detect_threshold=50,
        max_words_unknown_lang=2,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    ):
        self.min_chars = min_chars
        self.max_words = max_words
        self.min_freq = min_freq
        self.lang_detect_threshold = lang_detect_threshold
        self.max_words_unknown_lang = max_words_unknown_lang
        self.generated_stopwords_percentile = generated_stopwords_percentile
        self.generated_stopwords_max_len = generated_stopwords_max_len
        self.generated_stopwords_min_freq = generated_stopwords_min_freq

        if language_code is not None and language_code not in STOPWORDS:
            error_msg = (
                'There are no built-in stopwords for {lang_code} language code!\n'  # noqa
                'Possible solutions:\n'
                '1. Check list of supported languages at https://github.com/vgrabovets/multi_rake\n'  # noqa
                '2. Provide your own set of stopwords in stopwords argument\n'
                '3. Leave arguments language_code and stopwords as None and '
                'stopwords will be generated from provided text'.format(
                    lang_code=language_code,
                )
            )
            raise NotImplementedError(error_msg)

        elif stopwords is not None:
            self.stopwords = stopwords

        else:
            self.stopwords = STOPWORDS.get(language_code, set())

    def apply(self, text, text_for_stopwords=None):
        text = text.lower()

        max_words = self.max_words

        if self.stopwords:
            stop_words = self.stopwords

        else:
            language_code = detect_language(text, self.lang_detect_threshold)

            if language_code is not None and language_code in STOPWORDS:
                stop_words = STOPWORDS[language_code]

            else:
                if text_for_stopwords:
                    text_for_stopwords = text_for_stopwords.lower()
                    text_for_stopwords = ' '.join([text, text_for_stopwords])
                else:
                    text_for_stopwords = text

                stop_words = self._generate_stop_words(text_for_stopwords)

                if self.max_words_unknown_lang is not None:
                    max_words = self.max_words_unknown_lang

        sentence_list = split_sentences(text)

        phrase_list = self._generate_candidate_keywords(
            sentence_list,
            stop_words,
            max_words,
        )

        word_scores = Rake._calculate_word_scores(phrase_list)

        keywords = self._generate_candidate_keyword_scores(
            phrase_list,
            word_scores,
        )

        keywords = sorted(
            keywords.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )

        return keywords

    def _generate_stop_words(self, text):
        stop_words = set()

        text = keep_only_letters(text)

        if not text:
            return stop_words

        text = text.split()

        word_counts = Counter(text).most_common()
        counts_sample = [word_count[1] for word_count in word_counts]

        upper_bound = np.percentile(
            counts_sample,
            self.generated_stopwords_percentile,
        )

        upper_bound = max(upper_bound, self.generated_stopwords_min_freq)

        for word, count in word_counts:  # pragma: no branch
            if count >= upper_bound:
                if len(word) <= self.generated_stopwords_max_len:
                    stop_words.add(word)
            else:
                break

        return stop_words

    def _generate_candidate_keywords(
        self,
        sentence_list,
        stop_words,
        max_words,
    ):
        result = []
        phrases = []

        for sentence in sentence_list:
            tmp = []

            for word in sentence.split():
                if word in stop_words:
                    if tmp:
                        phrases.append(' '.join(tmp))
                        tmp = []

                else:
                    tmp.append(word)

            if tmp:
                phrases.append(' '.join(tmp))

        for phrase in phrases:
            if (
                    phrase and
                    len(phrase) >= self.min_chars and
                    len(phrase.split()) <= max_words
            ):
                result.append(phrase)

        return result

    def _generate_candidate_keyword_scores(self, phrase_list, word_score):
        keyword_candidates = {}

        for phrase in phrase_list:
            if phrase_list.count(phrase) >= self.min_freq:
                word_list = separate_words(phrase)
                candidate_score = 0

                for word in word_list:
                    candidate_score += word_score[word]

                keyword_candidates[phrase] = candidate_score

        return keyword_candidates

    @staticmethod
    def _calculate_word_scores(phrase_list):
        word_frequency = defaultdict(int)
        word_degree = defaultdict(int)

        for phrase in phrase_list:
            word_list = separate_words(phrase)
            word_list_length = len(word_list)
            word_list_degree = word_list_length - 1

            for word in word_list:
                word_frequency[word] += 1
                word_degree[word] += word_list_degree

        for item in word_frequency:
            word_degree[item] = word_degree[item] + word_frequency[item]

        word_score = defaultdict(int)

        for item in word_frequency:
            word_score[item] = word_degree[item] / word_frequency[item]

        return word_score
