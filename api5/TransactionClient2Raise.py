from data.tx_factory import Tx_Factory,Amount
class TransactionAPI:
    def __init__(self,client):
        self.client=client
    

    def deposit(self,amount=Amount.NORMAL,raise_on_error=True,remark=None,**overide):
        payload= Tx_Factory.deposit(amount,remark=remark,**overide)
        print(f"-----{payload}")
        return self.client.post("/api/transactions/deposit",json=payload,raise_on_error=raise_on_error)

    def withdraw(self,amount=Amount.MIN,raise_on_error=True,remark=None,**overide):
        payload= Tx_Factory.withdraw(amount,remark=remark,**overide)
        print(f"-----{payload}")
        return self.client.post("/api/transactions/withdraw",json=payload,raise_on_error=raise_on_error)

    def transfer(self,fromAccountNo,toAccountNo,amount,raise_on_error=True,remark=None,**overide):
        payload= Tx_Factory.transfer(fromAccountNo,toAccountNo,amount,remark=remark,**overide)
        print(f"-----{payload}")
        return self.client.post("/api/transactions/transfer",json=payload,raise_on_error=raise_on_error)


