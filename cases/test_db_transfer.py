from helpers.flow import Flows
from utils.assertions import assert_amount_equal,assert_balance_change,assert_business_error
import uuid
import pytest
from utils.db import query_select,count
from data.tx_factory import TxType

TRANS_AMOUNT=50
@pytest.fixture(scope="module")
def trans_flow():
    remark=f"test_trans_db_flow_{uuid.uuid4().hex[:8]}"
    user_a=Flows.normal_user_with_balance(1000)
    user_b=Flows.normal_user_with_balance(100)
    ac_client=user_a.get("account")
    a_tx_client=user_a.get("tx")
    a_before=ac_client.balance()
    a_c_no=ac_client.account_me()["accountNo"]

    bc_client=user_b.get("account")
    b_before=bc_client.balance()
    b_c_no=bc_client.account_me()["accountNo"]

    a_tx_client.transfer(a_c_no,b_c_no,TRANS_AMOUNT,remark=remark)

    return {
        "user_a":user_a,
        "user_b":user_b,
        "a_before":a_before,
        "b_before":b_before,
        "a_c_no":a_c_no,
        "b_c_no":b_c_no,
        "remark":remark
    }

def test_2_remarks(trans_flow):
    cnt=count("select count(*) from  transactions where remark= %s",(trans_flow["remark"],))
    assert cnt == 2, f"期望 2 个remark，实际 {cnt} for remark {trans_flow['remark']}" 

def test_2_remarks_amounts(trans_flow):

    cnt=count("select count(*) from  transactions where remark= %s and amount= %s",(trans_flow["remark"],TRANS_AMOUNT))
    assert cnt == 2, f"期望 2 个remark，实际 {cnt} for remark {trans_flow['remark']} and amount {TRANS_AMOUNT}" 

def test_2_remarks_type(trans_flow):

    cnt=count("select count(*) from  transactions where remark= %s and tx_type= %s",(trans_flow["remark"],TxType.TRANS_OUT))
    assert cnt == 1, f"期望 1 个remark，实际 {cnt} for remark {trans_flow['remark']} tx_type={TxType.TRANS_OUT}" 
    cnt2=count("select count(*) from  transactions where remark= %s and tx_type= %s",(trans_flow["remark"],TxType.TRANS_IN))
    assert cnt2 == 1, f"期望 1 个remark，实际 {cnt2} for remark {trans_flow['remark']} tx_type={TxType.TRANS_IN}" 

def test_balance_expected(trans_flow):
    a_before=trans_flow.get("a_before")
    b_before=trans_flow.get("b_before")
    a_c_no=trans_flow.get("a_c_no")
    b_c_no=trans_flow.get("b_c_no")
    
    a_after=trans_flow.get("user_a").get("account").balance()
    b_after=trans_flow.get("user_b").get("account").balance()


    cnt=query_select("select balance from accounts where account_no=%s",(a_c_no,))
    cnt2=query_select("select balance from accounts where account_no=%s",(b_c_no,))

    assert_amount_equal(a_after,cnt[0])
    assert_amount_equal(b_after,cnt2[0])

    assert_balance_change(cnt[0],a_before,-TRANS_AMOUNT)
    assert_balance_change(cnt2[0],b_before,TRANS_AMOUNT)
