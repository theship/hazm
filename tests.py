# coding: utf8

from __future__ import unicode_literals
import sys, inspect, doctest, unittest
from hazm import *

modules = {
	'peykare': PeykareReader(),
	'bijankhan': BijankhanReader(),
	'hamshahri': HamshahriReader(),
	'dadegan': DadeganReader(),
	'treebank': TreebankReader(),
	'sentence_tokenizer': SentenceTokenizer(),
	'word_tokenizer': WordTokenizer(),
	'normalizer': Normalizer(),
	'stemmer': Stemmer(),
	'lemmatizer': Lemmatizer(),
	'tagger': POSTagger(),
	'chunker': Chunker(),
	'parser': DependencyParser(tagger=POSTagger(), lemmatizer=Lemmatizer())
}


class UnicodeOutputChecker(doctest.OutputChecker):

	def check_output(self, want, got, optionflags):
		try:
			want, got = eval(want), eval(got)
		except Exception:
			got = got.decode('unicode-escape')
			want = want.replace('آ', 'ا')  # decode issue

		if type(want) == unicode:
			want = want.replace('٫', '.')  # eval issue

		return want == got


if __name__ == '__main__':
	# test all modules if no one specified
	all_modules = len(sys.argv) < 2

	suites = []
	checker = UnicodeOutputChecker() if utils.PY2 else None
	for name, object in modules.items():
		if all_modules or name in sys.argv:
			suites.append(doctest.DocTestSuite(inspect.getmodule(object), extraglobs={name: object}, checker=checker))

	if not utils.PY2 and all_modules:
		suites.append(doctest.DocFileSuite('README.md'))

	runner = unittest.TextTestRunner(verbosity=2)
	for suite in suites:
		runner.run(suite)
