import unittest #biblioteka do testow jednostkowych
from main import get_exchange_rate
from main import exchange_currency

class ExchangeTest(unittest.TestCase):
    def setUp(self): #ustalnenie wartosci do testowania
        self.a = 10
        self.b = "USD"
    def test_exchange_rate(self): #testujemy funkcje exchange_rate
        print("Test 1")
        #Act
        result = get_exchange_rate(self.b)  #pobieranie kursu dolara 
        
        #Assert
        self.assertLess(result,self.a/self.a)  #sprawdzenie czy kurs dolara jest wiekszy niz jeden

    def test_exchange_currency(self): #testujemy funkcje wymaine walut
        print("Test 2")
        #Act
        exchange_rate = get_exchange_rate(self.b)  #sprawdzamy jaki jest kurs wymainy dla dolara
        result = exchange_currency(self.a,self.b)  #sprawdzamy wartosc wymiany 10 dolarow
        #Assert
        self.assertEqual(result,round(exchange_rate * self.a,2)) #sprawdzamy czy wartosci sa takie same przy wykorzystaniu funkcji exchange_currency i bez niej





if __name__ == "__main__":
    unittest.main()



    
