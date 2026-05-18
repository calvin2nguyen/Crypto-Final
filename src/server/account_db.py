class AccountDatabase:
    def __init__(self):

        self.accounts = {
            "123456": {
                "password": "test123",
                "balance": 1000.00,
                "activity": []
            },

            "654321": {
                "password": "password",
                "balance": 500.00,
                "activity": []
            }
        }
    def authenticate(self,user_id,user_password):
        if user_id not in self.accounts:
            return False
        stored_password = self.accounts[user_id]["password"]
        return user_password == stored_password
    
    def get_balance(self,user_id):
        return self.accounts[user_id]["balance"]
    
    def deposit(self,user_id,deposit_amount):        
        self.accounts[user_id]["balance"] += deposit_amount
        print(f"Deposited: {deposit_amount}")        
        current_balance = self.accounts[user_id]["balance"]
        print(f"New balance: {current_balance}")

    def withdraw(self,user_id,withraw_ammount):
        current_balance = self.accounts[user_id]["balance"]
        if(withraw_ammount > current_balance):
            print("Withraw ammount exceeds current balance")
            return False
        current_balance -= withraw_ammount
        print(f"Withrew: {withraw_ammount}")
        current_balance = self.accounts[user_id]["balance"]    
        print(f"New balance: {current_balance}")
    