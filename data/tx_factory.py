class Amount:
    MIN=0.01
    TRANSFER=50
    NORMAL=88
    MAX=10000000
    BIG=10000

class TxType:
    TRANS_OUT = 3   # 转出
    TRANS_IN = 4    # 转入

class Tx_Factory:
    @staticmethod
    def deposit(amount,remark=None,**overide):
        if remark is None:
            remark=f"存款测试 存 {amount}"
        payload={"amount":amount,"remark":remark}
        payload.update(overide)
        return payload

    @staticmethod
    def withdraw(amount,remark=None,**overide):
        if remark is None:
            remark=f"取款测试 取 {amount}"
        payload={"amount":amount,"remark":remark}
        payload.update(overide)
        return payload    

    @staticmethod
    def transfer(fromAccountNo,toAccountNo,amount,remark=None,**overide):
        if remark is None:
            remark=f"转账测试 转 {amount}"
        payload={
          "fromAccountNo": fromAccountNo,
          "toAccountNo": toAccountNo,
          "amount": amount,
          "remark": remark
        }
        payload.update(overide)
        return payload      