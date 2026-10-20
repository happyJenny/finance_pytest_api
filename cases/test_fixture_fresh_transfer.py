from utils.assertions import assert_amount_equal,assert_balance_change
from data.tx_factory import Amount


def test_transfer(new_user_opened_account,new_user_2_opened_account):
    amount_deposit=Amount.NORMAL
    amount_transfer=Amount.TRANSFER

    ac_a=new_user_opened_account.get("account")
    tx_a=new_user_opened_account.get("tx")
    ac_2=new_user_2_opened_account.get("account")
    tx_2=new_user_2_opened_account.get("tx")
    account_a_me=ac_a.account_me()
    account_a_no=account_a_me["accountNo"]

    tx_a.deposit(amount_deposit)
    assert ac_a.balance()==amount_deposit

    account_a_balance_original=ac_a.balance()



    account_b_me=ac_2.account_me()
    account_b_no=account_b_me["accountNo"]
    account_b_balance_original=account_b_me.get("balance")


    assert account_a_balance_original>amount_transfer, f"account_a_balance_original {account_a_balance_original} should bigger than {amount_transfer} "
   
    actual_amount_transfer=tx_a.transfer(account_a_no,account_b_no,amount_transfer)["amount"]
    # print(f"sssssssssssssss{actual_amount_transfer}")
    a_last_balance=ac_a.balance()
    b_last_balance=ac_2.balance()

    assert_amount_equal(amount_transfer,actual_amount_transfer)
    assert_balance_change(a_last_balance,account_a_balance_original,-actual_amount_transfer)
    assert_balance_change(b_last_balance,account_b_balance_original,actual_amount_transfer)


    delta_a=account_a_balance_original-a_last_balance
    delata_b=b_last_balance-account_b_balance_original
    assert_amount_equal(delta_a,delata_b)



