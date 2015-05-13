import antigravity
import random

class TestSimpleSuite(object):

    def test_verdadero_es_verdadero(self):
        assert True == True
        #assert_equals

    def test_suma(self):
        assert 3 == 2+1

    def test_falla(self):
        assert 34 != 32+2
        #assert_not_equals

    def test_puede_andar(self):
        ran = random.randint(1, 4)
        assert ran == 2
