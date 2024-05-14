import argparse #biblioteka do przekazywania parametrow/argumentow z linii komend
import logging #biblioteka do logowania bledow/ zapisywania bledow
import requests #sluzaca do zapytania restowych i pobierania wartosci z api np z banku
import mysql.connector #biblioteka sluzaca do polaczenia z baza mysql

logging.basicConfig(level=logging.INFO)

def get_exchange_rate(currency_code):
    try:
        url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency_code.lower()}/'
        response = requests.get(url)
        response.raise_for_status() #zgloszenie informacji jaki byl status czy sie udalo czy nie udalo polaczyc
    except requests.exceptions.RequestException as e: #gdyby sie nie udalo polaczyc to loggujemy/zapisujemy bledy
        logging.error(f'Problem z wymiana walut: {e}') #logowanie statusu bledu jezeli nie udalo sie polaczyc do strony
        raise
    return response.json()['rates'][0]['mid'] #wydobywamy wartosc kursu z odpowiedzi ktora jest w jsonie


def exchange_currency(input_value, currency_code): #funkcja do wymiany walut
    exchange_rate = get_exchange_rate(currency_code) #pobieranie kursu waluty
    return round(input_value * exchange_rate,2) #mnozenie ilosci pieniedzy razy ten kurs

def log_info_to_mysql(Kurs, Waluta, IloscWymiany, CalkowitaKwota): #zapisywanie informacji na mysql
    mydb = mysql.connector.connect( #ustalenie parametrow do polaczenia z moja baza
        host="localhost", #na lokalnym serwerze
        user="admin_db", #jak sie nazywa konto z ktorym sie laczymy
        passwd="P@s$tdB1", #jak sie nazywa haslo
        database="test_db" #jak sie nazwya baza
    )
    mycursor = mydb.cursor() #storzenie polaczenia z baza
    sql = "INSERT INTO KursWalut (Kurs, NazwaWaluty, IloscWymiany, CalkowitaKwota) VALUES ("+str(Kurs)+",'"+Waluta+"'"+","+str(IloscWymiany)+","+str(CalkowitaKwota)+");" #wprowadzenie danych do tabeli kurs walut
    mycursor.execute(sql)#wykonanie skryptu powyzej
    mydb.commit() #stwierdzenie skryptu, zaakceptowanie
def main():
    parser = argparse.ArgumentParser(description='Kurs walut.') #przekazywanie parametrow do terminala zeby sie wyswietlalo
    parser.add_argument('--currency', required=True, help='Kod wymiany(EUR, GBP, USD, ...)') #podac walute
    parser.add_argument('--amount',required=True, type=float, help='Ilosc do wymiany') #podac ilosc
    args = parser.parse_args() #przekazywanie argumentow do funkcji

    result = exchange_currency(args.amount,args.currency) #wynik wymainy walut
    print(f'{args.amount} {args.currency} ma wartosc {result} PLN') #wypisanie ile to wyjdzie
    log_info_to_mysql(result/args.amount,args.currency,args.amount,result)  #wpisanie informacji do bazy

if __name__ == "__main__":
    main()

