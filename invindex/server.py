import shelve

import numpy as np
import tables
from funcserver import Server
import deeputil

class CooccurrenceServerAPI(object):

    def __init__(self, cooccurrence_fpath, vocab_table):
        self._cooccurrence_fpath = tables.open_file(cooccurrence_fpath, 'r')
        self._vocab = shelve.open(vocab_table, 'r')
        self._data = self._cooccurrence_fpath.root.data
        self._indices = self._cooccurrence_fpath.root.indices

    def get_num_docs(self, token):
        token = deeputil.xcode(token) if isinstance(token, unicode) else token

        token = str(token)
        res = dict(token=token)

        index = self._vocab.get(token)

        if index is None:
            res.update(occurrences=0)
            return res

        doc_size = (self._indices[index+1] - self._indices[index]).item()

        res.update(occurrences=doc_size)

        return res

    def _get_docs(self, token_index):
	if token_index == (len(self._indices) - 1):
            docs = self._data[self._indices[token_index]:len(self._data)]
        else:
            token_start = self._indices[token_index]
            token_end = token_start + (self._indices[token_index + 1] - token_start)
            docs = self._data[token_start:token_end]

        return docs

    def get_cooccurrences(self, token1, token2):
        token1 = deeputil.xcode(token1) if isinstance(token1, unicode) else token1
        token2 = deeputil.xcode(token2) if isinstance(token2, unicode) else token2

        token1 = str(token1)
        token2 = str(token2)

        res = dict(token1=token1, token2=token2)

        index1 = self._vocab.get(token1)
        index2 = self._vocab.get(token2)

        if (index1 is None) or (index2 is None):
            res.update(coccurrences=0)
            return res

        docs1 = self._get_docs(index1)

        docs2 = self._get_docs(index2)

        docs = np.intersect1d(docs1, docs2)
        res.update(cooccurrences=len(docs))

        return res


class CooccurrenceServer(Server):

    DESC = 'Document co-occurrences and occurrences service'

    def define_args(self, parser):
        super(CooccurrenceServer, self).define_args(parser)

        parser.add_argument('cooccurrence_fpath',metavar='cooccurrence-fpath',
                            help='Provide coocccurrences HDF5 file name')
        parser.add_argument('vocab_table',metavar='vocab-table',
                            help='Provide vocab hash table file name')

    def prepare_api(self):
        super(CooccurrenceServer, self).prepare_api()

        return CooccurrenceServerAPI(self.args.cooccurrence_fpath, self.args.vocab_table)


if __name__ == '__main__':
    CooccurrenceServer().start()
