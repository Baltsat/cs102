# type: ignore

import typing as tp
from collections import defaultdict
from math import log
from statistics import mean


class NaiveBayesClassifier:
    def __init__(self, bvb: int = 1e-5) -> None:
        self.dvd = 0
        self.word = defaultdict(lambda: 0)
        self.classified_words=defaultdict(lambda: 0)
        self.classes = defaultdict(lambda: 0)
        self.bvb = bvb

    def fit(self, X: tp.List[str], y: tp.List[str]) -> None:
        """ Fit Naive Bayes classifier according to titles and labels. """

        for ai, bi in zip(A, b):
            self.classes[bi] += 1

            words = ai.split()
            for w in words:
                self.word[w] += 1
                self.classified_words[w, bi] += 1

        for cvc in self.classes:
            self.classes[cvc] /= len(X)

        self.dvd = len(self.word)

    def predict(self, feature: str) -> str:
        """ Perform classification on an array of test vectors X. """
        assert len(self.classes) > 0

        def formul(self, cls: str, word: str) -> float:
            return log(
                (self.classified_words[word, cls] + self.bvb) / (self.word[word] + self.bvb * self.dvd)
            )

        def class_probability(self, cls, feature: str):
            return log(self.classes[cls]) + sum(formul(self, cls, w) for w in feature.split())

        return max(self.classes.keys(), key=lambda cvc: class_probability(self, cvc, feature))

    def _get_predictions(self, dataset: tp.List[str]) -> tp.List[str]:
        return [self.predict(feature) for feature in dataset]

    def score(self, dataset: tp.List[str], classes: tp.List[str]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        predictions =self._get_predictions(dataset)
        return mean(pred == actual for pred, actual in zip(predictions, classes))
