from Banking_System import BankingSystem


class TestBankingSystem:

    def test_luhn_algorithm(self):
        person = BankingSystem()
        assert person.luhn_algorithm('40000078912345') == 'Error'
        assert person.luhn_algorithm('400000789123457') == 4000007891234574
