from utils.assertions import assert_unauthorized,assert_business_error,assert_not_found
import pytest
from api5.AuthClient2Raise import AuthAPI
from api5.TransactionClient2Raise import TransactionAPI



def test_withdraw_freeze_account(login_client_freeze):   
    re=TransactionAPI(login_client_freeze).withdraw(2,raise_on_error=False)
    '''400'''
    assert_business_error(re,"账户状态异常")


# @pytest.mark.skip(reason="接口还没开发完")
def test_depost_no_token(logged_out_client):
    re=TransactionAPI(logged_out_client).deposit(2,raise_on_error=False)
    assert_unauthorized(re,"未登录或 token 缺失")

# @pytest.mark.skip(reason="接口还没开发完")
def test_deposit_without_open_account(login_client_no_account):   
    re=TransactionAPI(login_client_no_account).deposit(2,raise_on_error=False)
    '''404'''
    assert_not_found(re,"账户不存在，请先开户")

