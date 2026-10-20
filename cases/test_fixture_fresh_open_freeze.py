def test_open_account(new_user_no_account):
    ac_api=new_user_no_account.get("account")   
    re=ac_api.open_account()
    assert isinstance(re.get("accountId"), int)

def test_freeze_active_account(new_user_opened_account):
#   auth=AuthAPI(logged_out_client)
#   token= auth.login("performanceTest88881124437","jepeng")
    account=new_user_opened_account
    ac=account.get("account")
    re=ac.freeze()
    assert re.get("status")==0




