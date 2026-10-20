import pytest

from utils.assertions import assert_server_error,assert_validation_error


@pytest.mark.parametrize("deposit_Amount,message,field,expect",[
    (-1,"金额必须大于等于 0.01","amount","validation"),
    (9999999999,"单笔金额不能超过 1000 万","amount","validation"),
    ("ssss",'Character s is neither a decimal digit number, decimal point, nor "e" notation exponential mark.',"amount","server_error"),
    #   (1,200,"金额必须大于等于 0.01",None),
])


def test_invalid_deposit_small(account_api_alice,tx_api_alice,deposit_Amount,message,field,expect):

    AccountAPI,TransactionAPI=account_api_alice,tx_api_alice
    # account_me=AccountAPI.account_me()
    re=TransactionAPI.deposit(deposit_Amount,False)
    print(re.json())
    if expect=="server_error":
     assert_server_error(re,message)
    else:
     assert_validation_error(re,field,message)



