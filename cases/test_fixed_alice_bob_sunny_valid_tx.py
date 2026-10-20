from utils.assertions import assert_amount_equal,assert_balance_change
from data.tx_factory import Amount

normal=Amount.NORMAL
mini=Amount.MIN
def test_valid_deposit(account_api_alice,tx_api_alice):
    AccountAPI,TransactionAPI=account_api_alice,tx_api_alice
    balance_original=AccountAPI.balance()


    deposit_Amount=111
    amount=TransactionAPI.deposit(deposit_Amount,remark="存3个1")["amount"]
    assert_amount_equal(deposit_Amount,amount)
    new_balance=AccountAPI.balance()
    assert_balance_change(new_balance,balance_original,amount)


def test_withdraw(account_api_alice,tx_api_alice):
    AccountAPI,TransactionAPI=account_api_alice,tx_api_alice
    balance_original=AccountAPI.balance()
    # withdraw_amount=10
    assert balance_original>normal, f"balance_original {balance_original} should bigger than {mini} "
#   
    amount=TransactionAPI.withdraw()["amount"]
    assert_amount_equal(mini,amount)

    new_balance=AccountAPI.balance()

    assert_balance_change(new_balance,balance_original,-amount)    


def test_transfer(account_api_transfer_from,tx_api_transfer_from,account_api_bob,tx_api_bob):

    account_a_me=account_api_transfer_from.account_me()
    account_a_no=account_a_me["accountNo"]
    account_a_balance_original=account_a_me.get("balance")

    account_b_me=account_api_bob.account_me()
    account_b_no=account_b_me["accountNo"]
    account_b_balance_original=account_b_me.get("balance")

    amount_transfer=Amount.NORMAL
    assert account_a_balance_original>amount_transfer, f"account_a_balance_original {account_a_balance_original} should bigger than {amount_transfer} "
    actual_amount_transfer=tx_api_transfer_from.transfer(account_a_no,account_b_no,amount_transfer)["amount"]
    # print(f"sssssssssssssss{actual_amount_transfer}")
    a_last_balance=account_api_transfer_from.balance()
    b_last_balance=account_api_bob.balance()

    assert_amount_equal(amount_transfer,actual_amount_transfer)
    assert_balance_change(a_last_balance,account_a_balance_original,-actual_amount_transfer)
    assert_balance_change(b_last_balance,account_b_balance_original,actual_amount_transfer)


    delta_a=account_a_balance_original-a_last_balance
    delata_b=b_last_balance-account_b_balance_original
    assert_amount_equal(delta_a,delata_b)



