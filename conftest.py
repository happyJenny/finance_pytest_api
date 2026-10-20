from api5.BaseClient2Raise_error import BaseClient
from api5.AuthClient2Raise import AuthAPI
from api5.AccountClient2Raise import AccountAPI
from api5.TransactionClient2Raise import TransactionAPI
from config.loader import load_config
import pytest

CFG=load_config()
Base_URL=CFG["base_url"]
TIME_OUT=CFG["timeout"]


def _register_and_login():
    """动态用户：注册 + 登录，返回 (client, username)"""
    client=BaseClient(Base_URL,timeout=TIME_OUT)
    username=AuthAPI(client).register_tx().get("username")
    token=AuthAPI(client).login(username,"jepeng").get("token")
    client=BaseClient(Base_URL,token,timeout=TIME_OUT)
    return username,client
 # ==================== B. 动态用户 fixture ====================

@pytest.fixture
def new_user_no_account():
    """动态用户 + 未开户"""
    username,client=_register_and_login()
    return {
        "username":username,
        "client":client,
        "account":AccountAPI(client),
        "tx":TransactionAPI(client)
    }

@pytest.fixture
def new_user_opened_account(new_user_no_account):  
    """动态用户 + 已开户"""
    ac_api=new_user_no_account.get("account")   
    ac_api.open_account()
    return new_user_no_account

@pytest.fixture
def new_user_2_opened_account():  
    """动态用户 + 已开户"""
    username,client=_register_and_login()
    AccountAPI(client).open_account()
    return  {
        "username":username,
        "client":client,
        "account":AccountAPI(client),
        "tx":TransactionAPI(client)
    }

def _login_client(user):
    client=BaseClient(Base_URL,timeout=TIME_OUT)
    token=AuthAPI(client).login(CFG["users"][user]["username"],CFG["users"][user]["password"])["token"]
    client=BaseClient(Base_URL,token,timeout=TIME_OUT)
    return client

@pytest.fixture(scope="session")
def login_client_alice():
    return  _login_client("alice")

@pytest.fixture(scope="session")
def login_client_bob():
    return  _login_client("transfer_to")

@pytest.fixture(scope="session")
def login_client_transfer_from():
    return  _login_client("transfer_from")




@pytest.fixture
def account_api_transfer_from(login_client_transfer_from):
    return AccountAPI(login_client_transfer_from)

# @pytest.fixture
# def tx_api_transfer_from(login_client_transfer_from):
#     return TransactionAPI(login_client_transfer_from)
# 解决余额太少的问题
@pytest.fixture
def tx_api_transfer_from(login_client_transfer_from):
    ac=AccountAPI(login_client_transfer_from)
    tx=TransactionAPI(login_client_transfer_from)
    if ac.balance()<100:
        print(f"------------we wil depoist 100")
        tx.deposit(100)
    return tx

@pytest.fixture(scope="session")
def login_client_no_account():
    return  _login_client("without_open_account_user")


@pytest.fixture(scope="session")
def login_client_freeze():
    return  _login_client("freeze_account_user")

@pytest.fixture
def logged_out_client():
    return BaseClient(Base_URL,timeout=TIME_OUT)

@pytest.fixture
def invalid_token_client():
    return BaseClient(Base_URL,token="ab-invalid",timeout=TIME_OUT)


@pytest.fixture
def invalid_tx_token_client(invalid_token_client):
    return TransactionAPI(invalid_token_client)

@pytest.fixture
def account_api_alice(login_client_alice):
    return AccountAPI(login_client_alice)



@pytest.fixture
def tx_api_alice(login_client_alice):
    return TransactionAPI(login_client_alice)


@pytest.fixture
def account_api_bob(login_client_bob):
    return AccountAPI(login_client_bob)

@pytest.fixture
def tx_api_bob(login_client_bob):
    return TransactionAPI(login_client_bob)

