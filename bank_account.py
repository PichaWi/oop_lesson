class AccountDB:
    def __init__(self):
        self.account_database = []

    def insert(self, account):
        index = self.__search_private(account.account_number)
        if index == -1:
            self.account_database.append(account)
        else:
            print(account, "There already exit account; nothing to be insert here")

    def __search_private(self, account_num):
        for i in range(len(self.account_database)):
            if self.account_database[i].account_number == account_num:
                return i
        return -1

    def search_public(self, account_num):
        for account in self.account_database:
            if account.account_number == account_num:
                return account
        return None

    def delete(self, account_num):
        index = self.__search_private(account_num)
        if index != -1:
            self.account_database.pop(index)

    def __str__(self):
        b = ''
        for account in self.account_database:
            b += str(account) + ", "
        return b


class Account:
    def __init__(self, num, type, name, balance):
        self.account_number = num
        self.type = type
        self.account_name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount

    def __str__(self):
        return ('{' + str(self.account_number) + ',' + str(self.type) + ',' + str(self.account_name) + ',' +
                str(self.balance) + '}')


account1 = Account("0000", "saving", "David Patterson", 1000)
account2 = Account("0001", "checking", "John Hennessy", 2000)
account3 = Account("0003", "saving", "Mark Hill", 3000)
account4 = Account("0004", "saving", "David Wood", 4000)
account5 = Account("0004", "saving", "David Wood", 4000)
my_account_DB = AccountDB()
my_account_DB.insert(account1)
my_account_DB.insert(account2)
my_account_DB.insert(account3)
my_account_DB.insert(account4)
my_account_DB.insert(account5)
print(my_account_DB)
my_account_DB.search_public("0003").deposit(50)
print(my_account_DB)
my_account_DB.search_public("0003").withdraw(100)
print(my_account_DB)
my_account_DB.delete('0002')
print(my_account_DB)
my_account_DB.search_public("0010").deposit(50)
print(my_account_DB)
