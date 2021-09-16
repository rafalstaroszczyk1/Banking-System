import random
import array
import sqlite3

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                );"""
INSERT_CARD = "INSERT INTO card (number, pin)  VALUES (?, ?)"
GET_PIN_BY_CARD = "SELECT pin FROM card WHERE number =?;"
GET_NUMBER_BY_PIN = "SELECT number FROM card WHERE pin =?;"
GET_BALANCE_BY_NUMBER = "SELECT balance FROM card WHERE number =?;"
ADD_INCOME = "UPDATE card SET balance = balance + ? WHERE number = ?;"
CHECK_EXIST_NUMBER = "SELECT number FROM card WHERE number =?;"
SUBTRACT_MONEY = "UPDATE card SET balance = balance - ? WHERE number = ?;"
DELETE_ACCOUNT = "DELETE FROM card WHERE number = ?;"


def connect():
    return sqlite3.connect('card.s3db')


def create_table():
    with connection:
        connection.execute(CREATE_TABLE)


def add_card(card_number, card_pin):
    with connection:
        connection.execute(INSERT_CARD, (card_number, card_pin))


def get_number_by_pin(pin):
    with connection:
        return connection.execute(GET_NUMBER_BY_PIN, (pin,)).fetchone()


def get_pin_by_number(numbers):
    with connection:
        return connection.execute(GET_PIN_BY_CARD, (numbers,)).fetchone()


def get_balance_from(number):
    with connection:
        return connection.execute(GET_BALANCE_BY_NUMBER, (number,)).fetchone()


def add_income(number, income):
    with connection:
        connection.execute(ADD_INCOME, (income, number))


def check_exist_number(number):
    with connection:
        return connection.execute(CHECK_EXIST_NUMBER, (number,)).fetchone()


def subtract_money(number, amount_of_money):
    with connection:
        connection.execute(SUBTRACT_MONEY, (amount_of_money, number))


def delete_account(number):
    with connection:
        connection.execute(DELETE_ACCOUNT, (number,))


connection = connect()
create_table()


class BankingSystem:
    def __init__(self):
        self.item_number = int
        self.card_number = str
        self.card_pin = str
        self.user_card = str
        self.user_pin = str
        self.check_sum = int
        self.log_in_option = int
        self.balance = int

    def menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        self.item_number = int(input())
        return self.item_number

    def luhn_algorithm(self, card_number):
        if len(card_number) != 15:
            return "Error"
        else:
            number_card_array = array.array('i', [int(i) for i in card_number])
            i = 0
            while i < len(number_card_array):
                number_card_array[i] *= 2
                if number_card_array[i] > 9:
                    number_card_array[i] -= 9
                i += 2
            if sum(number_card_array) % 10 != 0:
                self.check_sum = str(10 - sum(number_card_array) % 10)
            else:
                self.check_sum = str(0)
            self.card_number = int(card_number + self.check_sum)

    def create_account(self):
        print(f'\nYour card has been created\n'
              f'Your card number:\n'
              f'{self.card_number}\n'
              f'Your card PIN:\n'
              f'{self.card_pin}\n')

        add_card(self.card_number, self.card_pin)

    def log_in_account(self):
        self.user_card = input('\nEnter your card number:\n')
        self.user_pin = input('Enter your PIN:\n')
        number_from_table = get_number_by_pin(self.user_pin)
        pin_from_table = get_pin_by_number(self.user_card)
        if number_from_table is None or pin_from_table is None:
            print('\nWrong card number or PIN!\n')
        elif number_from_table[0] != self.user_card or pin_from_table[0] != self.user_pin:
            print('\nWrong card number or PIN!\n')
        else:
            print('You have successfully logged in!\n')
            self.account_main(self.user_card)

    def account_main(self, user_card):
        while True:
            print('1. Balance\n'
                  '2. Add income\n'
                  '3. Do Transfer\n'
                  '4. Close account\n'
                  '5. Log out\n'
                  '0. Exit')

            self.log_in_option = int(input())
            self.balance = get_balance_from(user_card)[0]
            if self.log_in_option == 1:
                print(f'\nBalance: {self.balance}\n')
            elif self.log_in_option == 2:
                income = input('\nEnter income:\n')
                print('Income was added!\n')
                add_income(user_card, income)
            elif self.log_in_option == 3:
                print('\nTransfer\n')
                transfer_card_number = input('Enter card number:\n')
                if transfer_card_number == user_card:
                    print("You can't transfer money to the same account!\n")
                elif self.luhn_algorithm(transfer_card_number[0:len(transfer_card_number) - 1]) == "Error":
                    print('Probably you made a mistake in the card number. Please try again!\n')
                elif str(self.card_number) != transfer_card_number:
                    print('Probably you made a mistake in the card number. Please try again!\n')
                elif check_exist_number(transfer_card_number) is None:
                    print('Such a card does not exist.')
                else:
                    print('Enter how much money you want to transfer:')
                    transfer_amount_of_money = int(input())
                    if transfer_amount_of_money > int(self.balance):
                        print('Not enough money!')
                    else:
                        add_income(transfer_card_number, transfer_amount_of_money)
                        subtract_money(user_card, transfer_amount_of_money)
                        print('Success!')
            elif self.log_in_option == 4:
                print('The account has been closed!\n')
                delete_account(user_card)
                break
            elif self.log_in_option == 5:
                print('You have successfully logged out!\n')
                break
            elif self.log_in_option == 0:
                exit()
            else:
                print("\nUnknown option.\n")

    def main(self):
        while True:
            self.menu()
            if self.item_number == 1:
                self.card_number = '400000' + str(random.randint(100000000, 999999999))
                self.card_pin = (str(random.randint(0000, 9999))).zfill(4)
                self.luhn_algorithm(self.card_number)
                self.create_account()
            elif self.item_number == 2:
                self.log_in_account()
            elif self.item_number == 0:
                print('Bye!')
                break


if __name__ == '__main__':
    person = BankingSystem()
    person.main()

