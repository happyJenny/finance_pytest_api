from utils.assertions import assert_business_error
import pytest
from api5.AuthClient2Raise import AuthAPI
from api5.TransactionClient2Raise import TransactionAPI

from data.user_factory import Users_Factory

VALID_IDCARD =  "d11111222111111111"   
VALID_PHONE  = "2d800138000"
@pytest.mark.parametrize("username,idcard,phone,message",[
    ("","111111222111111111",VALID_PHONE,"用户名不能为空"),   
    ("alice",VALID_IDCARD,"1434324234","手机号必须为 11 位"), 
    ("alice",VALID_IDCARD,"","手机号必须为 11 位"),        # 密码错
    ("aliceandbob","",VALID_PHONE,"身份证号必须为 18 位"),
    ("alice",VALID_IDCARD,VALID_PHONE,"用户名已存在"),  
    ("aliceandaron",VALID_IDCARD,"d104c6bd0bb","手机号已注册"),   
    ("aliceandaron","89dddddddddddddddd",VALID_PHONE,"身份证已注册"),  
    ("' OR '2'='2",VALID_IDCARD,VALID_PHONE,"SQL注入"),  

])
def test_register_failure(logged_out_client, username, idcard,phone, message):

        
    auth = AuthAPI(logged_out_client)
    re = auth.register(username,idcard,phone, raise_on_error=False)
    assert re.status_code != 200, f"注入成功！, resp={re}"
    assert re.status_code == 400, f"注入成功！, resp={re}"
    assert_business_error(re,message) 


# @pytest.mark.skip(reason="接口还没开发完")
@pytest.mark.parametrize("username,password,status",[
    ("' OR '1'='1","some",400),
    ("alice","wrong_password",400),      # 密码错
    ("not_exist_user","whatever",400),   # 用户不存在
    ("", "whatever", 400),                 # 用户名为空
    ("alice", "", 400),                    # 密码为空
])
def test_login_failure(logged_out_client, username, password, status):

        
    auth = AuthAPI(logged_out_client)
    re = auth.login(username, password, raise_on_error=False)
    # assert re.status_code != 200, f"注入成功！, resp={re}"
    
    # assert re.status_code == status, f"注入成功！, resp={re}"
    assert_business_error(re,"用户名或密码错误") 




