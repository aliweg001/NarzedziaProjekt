import argparse
import logging
import requests
import mysql.connector

logging.basicConfig(level=logging.INFO)

def get_exchange_rate(currency_code):
    try:
        url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency_code.lower()}/'
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Problem z wymiana walut: {e}')
        raise
    return response.json()['rates'][0]['mid']


def exchange_currency(input_value, currency_code):
    exchange_rate = get_exchange_rate(currency_code)
    return round(input_value * exchange_rate,2)

def log_info_to_mysql(Kurs, Waluta, IloscWymiany, CalkowitaKwota):
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin_db",
        passwd="P@s$tdB1",
        database="test_db"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO KursWalut (Kurs, NazwaWaluty, IloscWymiany, CalkowitaKwota) VALUES ("+str(Kurs)+",'"+Waluta+"'"+","+str(IloscWymiany)+","+str(CalkowitaKwota)+");"
    mycursor.execute(sql)
    mydb.commit()
def main():
    parser = argparse.ArgumentParser(description='Kurs walut.')
    parser.add_argument('--currency', required=True, help='Kod wymiany(EUR, GBP, USD, ...)')
    parser.add_argument('--amount',required=True, type=float, help='Ilosc do wymiany')
    args = parser.parse_args()

    result = exchange_currency(args.amount,args.currency)
    print(f'{args.amount} {args.currency} ma wartosc {result} PLN')
    log_info_to_mysql(result/args.amount,args.currency,args.amount,result)  

if __name__ == "__main__":
    main()

