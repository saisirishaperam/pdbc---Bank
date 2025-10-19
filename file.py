import MySQLdb.connections
class BANK_PDBC:
    def __init__(self):
        self.conn = MySQLdb.connections.Connection(
            user='root',
            host='localhost',
            database='44_pdbc',
            password='Sirisha@09')
        self.cursor=self.conn.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS accounts(
                            acc_no INTEGER PRIMARY KEY,
                            name TEXT,
                            balance float
                            )''')
        self.conn.commit()
    

    def account_exists(self, acc_no):
        self.cursor.execute('SELECT * FROM accounts  WHERE acc_no = %s',(acc_no,))
        return self.cursor.fetchone() is not None
    
    def create_account(self):
        acc_no = int(input("Enter Account Number: "))
        if self.account_exists(acc_no):
            print('Account already exists!')
            return
        
        name = input('Enter Account Holder name:')
        balance = float(input('Enter Initial Balance:'))
        self.cursor.execute(
            "INSERT INTO  accounts (acc_no, name, balance) VALUES (%s,%s,%s)",
            (acc_no, name, balance)
        )
        self.conn.commit()
        print("Account created successfully")

    def deposit(self):
        acc_no = int(input("Enter Account Number: "))
        if not self.account_exists(acc_no):
            print('Account number not found')
            return
        
        amount = float(input("Anter Amount to deposite:"))
        self.cursor.execute(
            'UPDATE accounts SET balance = balance + %s WHERE acc_no = %s',(amount, acc_no))
        self.conn.commit()
        print('Deposite succesufull')

    def withdraw(self):
        acc_no = int(input("Enter Account Number:"))
        self.cursor.execute('SELECT balance FROM accounts WHERE acc_no = %s',(acc_no,))
        result = self.cursor.fetchone()
        if result :
            balance = result[0]
            amount = float(input('Enter Amount to Withdraw:'))
            if balance >= amount:
                self.cursor.execute(
                    'UPDATE accounts SET balance = balance - %s WHERE acc_no = %s',
                    (amount, acc_no)
                )
                self.conn.commit()
                print('withdrawl sucessfull!')
            else:
                print('Insufficient ')
        else:
            print("Account number not found")

    def check_balance(self):
        acc_no = int(input("Enter Account Number:"))
        self.cursor.execute('SELECT balance FROM accounts WHERE acc_no = %s ',(acc_no,))
        result = self.cursor.fetchone()
        if result:
            print(f" Balance for Account {acc_no}: {result[0]}")
        else:
            print("Account number not found")


    def close_connection(self):
        'close cursor and connecton safely'
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('Data base connection closed.')


obj = BANK_PDBC()

while True:
            print("\n ---Banking Menu--- ")
            print('1. Create Account')
            print('2. Deposite ')
            print('3. Withdraw')
            print('4 Check Balance')
            print('5. closing connection')
            print('6. Exit loop')

            choice = input('Enter your choice (1-6):')
            if choice == '1':
                    obj.create_account()
            elif choice == '2':
                    obj.deposit()
            elif choice == '3':
                    obj.withdraw()
            elif choice == '4':
                    obj.check_balance()
            elif choice == '5':
                    obj.close_connection()
            elif choice == '6':
                    print("Thank you for using the banking system.")
                    break
            else:
                    print("Invalid option. Please choose between 1 to 6.")