import threading
import time  # Import the time module

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.version = 0  # Представляет версию ресурса

    def withdraw(self, amount):
        # Симуляция затратного времени операции
        # Для простоты предположим, что снятие всегда успешно
        self.balance -= amount

    def commit_changes(self, new_balance, new_version):
        # Симуляция проверки конфликтов и применения изменений
        if new_version == self.version + 1:
            self.balance = new_balance
            self.version = new_version
            print(f"Изменения успешно применены. Новый баланс: {self.balance}")
        else:
            print("Обнаружен конфликт. Пожалуйста, разрешите конфликт.")

def user_thread(account, withdrawal_amount):
    # Симуляция пользователя, внесающего изменения в счет
    local_balance = account.balance - withdrawal_amount
    local_version = account.version + 1

    # Симуляция задержки, представляющей работу пользователя
    # В реальном сценарии это могли бы быть серия взаимодействий пользователя и операций
    # перед применением изменений
    time.sleep(2)  # Use time.sleep instead of threading.sleep

    # Попытка применить изменения к счету
    account.commit_changes(local_balance, local_version)

# Пример использования:
if __name__ == "__main__":
    # Создание экземпляра BankAccount
    account = BankAccount(account_id=1, balance=100)

    # Запуск двух потоков пользователя с попыткой снятия денег
    thread1 = threading.Thread(target=user_thread, args=(account, 30))
    thread2 = threading.Thread(target=user_thread, args=(account, 50))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
