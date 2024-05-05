import unittest
from main import get_exchange_rate
from main import exchange_currency

class ExchangeTest(unittest.TestCase):
    def setUp(self):
        self.a = 10
        self.b = "USD"
    def test_exchange_rate(self):
        print("Test 1")
        #Act
        result = get_exchange_rate(self.b)
        
        #Assert
        self.assertGreater(result,self.a/self.a)

    def test_exchange_currency(self):
        print("Test 2")
        #Act
        exchange_rate = get_exchange_rate(self.b)
        result = exchange_currency(self.a,self.b)
        #Assert
        self.assertEqual(result,round(exchange_rate * self.a,2))



if __name__ == "__main__":
    unittest.main()



    
