class Authenticator:
    def __init__(self):
        self.valid_atms = {
            "ATM1" : "keys/atm_public.pem",
            "ATM2" : "keys/atm2.public.pem"
        }

    def atm_valid(self,atm_id):
        return atm_id in self.atm_valid
    
    def get_atm_path(self,atm_id):
        return self.atm_valid.get(atm_id)
    def valid_customer(self,user_id):
        return len(user_id) == 6 and user_id.isdigit()
    def verify_customer(self,account_db, user_id,user_pass):
        return account_db.authenticate(user_id,user_pass)
