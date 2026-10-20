from helpers.flow import Flows
from utils.assertions import assert_amount_equal,assert_balance_change,assert_business_error
import pytest

@pytest.fixture(scope="module")
def trans_flow_frozen_user():
    user=Flows.frozen_user(100)
    return user


def test_froze_deposit(trans_flow_frozen_user):
    ac,tx=trans_flow_frozen_user.get("account"),trans_flow_frozen_user.get("tx")
    balance_before=ac.balance()
    deposit_amount=10
    tx.deposit(deposit_amount)
    balance_after=ac.balance()
    assert_balance_change(balance_after,balance_before,deposit_amount)

def test_froze_withdraw(trans_flow_frozen_user):  
    ac,tx=trans_flow_frozen_user.get("account"),trans_flow_frozen_user.get("tx")
    withdraw_amount=10
    re=tx.withdraw(withdraw_amount,raise_on_error=False)
    assert_business_error(re,"账户状态异常") 


def test_transfer_from_froze(trans_flow_frozen_user):  
    user_to=Flows.normal_user_with_balance(0.01)
    transfer_amount=10
    re=Flows.transfer(trans_flow_frozen_user,user_to,transfer_amount,raise_on_error=False)
    assert_business_error(re,"转出账户状态异常")      

def test_transfer_to_froze(trans_flow_frozen_user):  
    user_a=Flows.normal_user_with_balance(500)
    user_to=trans_flow_frozen_user
    old_a=user_a.get("account").balance()
    old_b=user_to.get("account").balance()

    transfer_amount=10
    re=Flows.transfer(user_a,user_to,transfer_amount,"god i am taking")
    actual_amount=re.get("amount")


    new_a=user_a.get("account").balance()
    new_b=user_to.get("account").balance()

    assert_balance_change(new_a,old_a,-actual_amount)     
    assert_balance_change(new_b,old_b,actual_amount)  
    assert_amount_equal(old_a-new_a,new_b-old_b)  
