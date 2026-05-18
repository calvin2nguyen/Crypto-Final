class Authenticator:

    def __init__(self):
        self.valid_atms = {
            "ATM1": "keys/atm1_public.pem",
            "ATM2": "keys/atm2_public.pem"
        }

    def atm_valid(self, atm_id):
        return atm_id in self.valid_atms

    def get_atm_path(self, atm_id):
        return self.valid_atms.get(atm_id)

    def valid_user(self, user_id):
        return len(user_id) == 6 and user_id.isdigit()

    def verify_user(self, account_db, user_id, user_pass):
        return account_db.authenticate(user_id, user_pass)