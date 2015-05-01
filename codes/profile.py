import theano
import numpy as np
from settings import *
from datetime import datetime
import os

class BaseExecutor:
    def __init__(self, name):
        now = datetime.now()
        now_str = now.strftime('%m%d_%H%M%S')
        self.name = name + '_' + now_str
        self.path = os.path.join(PATH['output'], self.name)
        os.mkdir(self.path)
        pass

    def get_io(self):
        raise NotImplementedError('self.get_io() not implemented')

    def start(self):
        self.x = T.matrix('features', config.floatX)
        self.y = T.imatrix('targets')
        raise NotImplementedError('self.start() not implemented')

    def end(self):
        self.predict_test()

    def predict_test(self):
        x, y_hat = self.get_io()
        fun = theano.function([x], y_hat)

        test_feature = np.load(self.test_file)
        result = fun(test_feature)

        from phomap import id2ph

        answer = []
        for r in result:
            answer.append(id2ph(r))

        with open(os.path.join(self.path, 'test.out')) as f:
            f.write('\n'.join(answer))
