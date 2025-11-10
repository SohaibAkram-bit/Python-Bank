accounts: dict[int, "BankAccount"] = {}  # Keyed by accountNumber

class BankAccount:
    accountNumberCounter = 1000

    def __init__(self, name: str):
        self.Name = name
        BankAccount.accountNumberCounter += 1
        self.accountNumber = BankAccount.accountNumberCounter
        self.Deposit = 0
        self.transactions: list[str] = []  # Transaction history list

    def __str__(self):
        return f"Candidate Name: {self.Name} | Account Number: {self.accountNumber} | Available balance: {self.Deposit}"

    def deposit(self, amount: int = None):
        if amount is None:
            try:
                amount = int(input("Enter the deposit amount: "))
            except ValueError:
                print("Invalid amount.")
                return
        if amount <= 0:
            print("Deposit amount must be positive.")
        else:
            self.Deposit += amount
            self.transactions.append(f"Deposited {amount}. Balance: {self.Deposit}")
            print(f"Deposited {amount}. Current balance: {self.Deposit}")

    def withdraw(self, amount: int = None):
        if amount is None:
            try:
                amount = int(input("Enter the withdrawal amount: "))
            except ValueError:
                print("Invalid amount.")
                return
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.Deposit:
            print("Insufficient balance.")
        else:
            self.Deposit -= amount
            self.transactions.append(f"Withdrew {amount}. Balance: {self.Deposit}")
            print(f"Withdrew {amount}. Current balance: {self.Deposit}")

    def transfer_to(self, other: "BankAccount", amount: int):
        if amount <= 0:
            print("Transfer amount must be positive.")
        elif amount > self.Deposit:
            print("Insufficient balance for transfer.")
        else:
            self.Deposit -= amount
            other.Deposit += amount
            self.transactions.append(f"Transferred {amount} to {other.Name} (ID: {other.accountNumber}). Balance: {self.Deposit}")
            other.transactions.append(f"Received {amount} from {self.Name} (ID: {self.accountNumber}). Balance: {other.Deposit}")
            print(f"Transferred {amount} to {other.Name}. Your new balance: {self.Deposit}")

    def print_statement(self):
        print(f"\n--- Transaction Statement for {self.Name} (ID: {self.accountNumber}) ---")
        if not self.transactions:
            print("No transactions yet.")
        else:
            for t in self.transactions:
                print(t)
        print(f"Current Balance: {self.Deposit}")
        print("-" * 50)


def make_account():
    name = input("Enter account holder's name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    account = BankAccount(name)
    if input("Do you want to make an initial deposit (Yes/No): ").lower() == "yes":
        account.deposit()
    accounts[account.accountNumber] = account
    print(f"Account created!\n{account}")


def get_account_by_id(prompt="Enter account ID: ") -> BankAccount | None:
    try:
        acc_id = int(input(prompt))
    except ValueError:
        print("Invalid ID.")
        return None
    account = accounts.get(acc_id)
    if not account:
        print("Account not found.")
    return account


while True:
    print("\n" + "_"*30)
    print("1. Make Account")
    print("2. View Accounts")
    print("3. Deposit")
    print("4. Withdrawal")
    print("5. Transfer")
    print("6. Account Statement")
    print("7. Exit")

    try:
        option = int(input("Choose an operation (1-7): "))
    except ValueError:
        print("Invalid input. Enter a number 1-7.")
        continue

    match option:
        case 1:
            make_account()
        case 2:
            if accounts:
                for acc in accounts.values():
                    print(acc)
            else:
                print("No accounts created yet.")
        case 3:
            acc = get_account_by_id()
            if acc:
                acc.deposit()
        case 4:
            acc = get_account_by_id()
            if acc:
                acc.withdraw()
        case 5:
            sender = get_account_by_id("Enter sender account ID: ")
            if not sender:
                continue
            receiver = get_account_by_id("Enter receiver account ID: ")
            if not receiver:
                continue
            try:
                amount = int(input("Enter transfer amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            sender.transfer_to(receiver, amount)
        case 6:
            acc = get_account_by_id()
            if acc:
                acc.print_statement()
        case 7:
            print("Exiting program.")
            break
        case _:
            print("Invalid option. Choose 1-7.")
