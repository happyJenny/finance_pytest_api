"""业务语义层：把多步操作封装成一行。
原则：只推进状态，不写断言。断言留在 cases/。
"""
from api5.BaseClient2Raise_error import BaseClient
from api5.AuthClient2Raise import AuthAPI
from api5.AccountClient2Raise import AccountAPI
from api5.TransactionClient2Raise import TransactionAPI
from config.loader import load_config
from data.user_factory import Users_Factory

CFG = load_config()
BASE_URL = CFG["base_url"]
TIME_OUT = CFG.get("timeout", 10)


class Flows:
    """所有方法都是 staticmethod，调用方式 Flows.xxx()"""

    @staticmethod
    def _new_client(token=None):
        client=BaseClient(BASE_URL,token,timeout=TIME_OUT)
        return client


    @staticmethod
    def register_and_login():
        """注册一个动态用户 + 登录，返回 dict（未开户）"""
        client=Flows._new_client()
        userdata=Users_Factory.build()
        username=userdata["username"]
        auth=AuthAPI(client)
        auth.register(username,userdata["idCard"],userdata["phone"])
        token=auth.login(username,"jepeng").get("token")
        client=Flows._new_client(token)
        return {
            "username":username,
            "client":client,
            "account":AccountAPI(client),
            "tx":TransactionAPI(client)
        }

    @staticmethod
    def normal_user_with_balance(balance):
        """注册 + 开户 + 存款 balance，返回用户 dict"""
        normal_user=Flows.register_and_login()
        normal_user["account"].open_account()
        if balance>=0.01:
           normal_user["tx"].deposit(balance)
        return normal_user



    @staticmethod
    def frozen_user(balance=0):
        """注册 + 开户 + （balance >= 0.01 时存款）+ 冻结"""
        user=Flows.normal_user_with_balance(balance)
        user["account"].freeze()
        return user

    @staticmethod
    def get_balance(user):
        """读余额，float"""
        return user["account"].balance()


    @staticmethod
    def transfer(from_user, to_user, amount, remark=None,raise_on_error=True):
        """转账：from_user → to_user"""
        from_account=from_user["account"]
        from_tx=from_user["tx"]
        to_account=to_user["account"]

        from_account_no=from_account.account_me()["accountNo"]
        to_account_no=to_account.account_me()["accountNo"]
        return from_tx.transfer(from_account_no,to_account_no,amount, remark=remark,raise_on_error=raise_on_error)
        
