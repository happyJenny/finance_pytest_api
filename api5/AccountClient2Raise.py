class AccountAPI:
    def __init__(self,client):
        self.client=client
    

    def open_account(self,raise_on_error=True):
        return self.client.post("/api/accounts/open",json={"accountType": 1},raise_on_error=raise_on_error)

    def account_me(self,raise_on_error=True):
        return self.client.get("/api/accounts/me",raise_on_error=raise_on_error)

    def balance(self):
        return self.account_me()["balance"]

    def status(self):
        return self.account_me()["status"]    

    def freeze(self,raise_on_error=True): 
        id=self.account_me(raise_on_error=True)["id"]
        payload={"status":0}
        return self.client.put(f"/api/accounts/{id}/status",json=payload,raise_on_error=raise_on_error)

