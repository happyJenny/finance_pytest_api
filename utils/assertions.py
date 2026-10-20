from utils.amount import to_fen,amount_equal,amount_change_equal
def assert_amount_equal(expect,actual):
    # assert round(expect*100)==round(actual*100),f"amount 不等，实际{actual},期望 {expect}"
    # assert to_fen(expect)==to_fen(actual),f"amount 不等，实际{actual},期望 {expect}"
    assert amount_equal(expect,actual),f"amount 不等，实际{actual},期望 {expect}"

def assert_balance_change(actual,original,change):
    expected = to_fen(original)+to_fen(change)
    # assert round(actual*100)==round(original*100+change*100),f"amount 不等，实际{actual},期望 {expected}"
    # assert to_fen(actual)==to_fen(original)+to_fen(change) ,f"amount 不等，实际{actual},期望 {expected},原始{original} change{change}"
    assert amount_change_equal(actual,original,change),f"amount 不等，实际{actual},期望 {expected},原始{original} change{change}"
def _get_body(response):
    try:
        return response.json()
    except Exception:
        raise AssertionError(
            f"Http response code is {response.status_code}\n"
            f"text: {response.text[:300]}"
        )    


def _fail(response,reason,message=None):
    body=_get_body(response)
    expected = "(未指定期望 message)"
    if message is not None:
            expected = f"期望 {message}" 
    raise AssertionError(
        f"{reason}\n"
        f"url: {response.request.url if (response.request) else None}\n"
        f"HTTP status_code: {response.status_code}\n"
        f"body:{body}\n"
        f"message 实际:{body.get('message') } {expected}\n"
    )

def assert_error(response, code,message=None):
    body=_get_body(response)
    if (response.status_code!=code or body.get("code")!=code):
        _fail(response,f"期望http code {code} 实际http code {response.status_code}")
    if (message is not None and body.get("message")!=message):
        _fail(response, f"期望 message={message}",message=message) 
        # assert   body.get("message")==message , f"期望 message={message!r}，实际 {body.get('message')!r}"
    return body    


def assert_business_error(response, message=None):
   return assert_error(response, 400,message=message)    


def assert_unauthorized(response, message=None):
     return assert_error(response, 401,message=message)

def assert_forbidden(response, message=None):  
    return assert_error(response, 403,message=message)       

def assert_not_found(response, message=None):    
    return assert_error(response, 404,message=message)    

def assert_conflict(response, message=None):    
    return assert_error(response, 409,message=message)    

def assert_server_error(response, message=None):  
    return assert_error(response, 500,message=message)      

def assert_ok(response,expected_status=200):
    body=_get_body(response)
    assert response.status_code==expected_status
    assert body.get("code")==0
    return body.get("data")


def assert_validation_error(response,field=None,message=None):
    """ deposit 金额边界值"""
    body=_get_body(response)
    assert response.status_code==422 , f"期望 HTTP 422, {response.status_code}，body={body}"
    assert body.get("code")==422
    errors = (body.get("data") or {}).get("errors") or {}
    assert isinstance(errors,dict) , \
        f"data.errors 不是字典: {errors}"
    if field is not None:
        assert field in errors    
    if (field is not None) and (message is not None):
        assert errors.get(field)==message,    f"字段 {field!r} 期望 {message!r}，实际 {errors[field]!r}"
    return errors



# def assert_code_error_message(response,status_code,field=None,message=None):
#     assert response.status_code==status_code, f"期望的状态码{status_code}，实际是{response.status_code}"
#     print (response.json())
#     if field is not None:
#         data= response.json()["data"]["errors"]
#         assert field in data, f"错误字段 {field} 不存在: {data}"
#         if message is not None:
#             assert data[field]==message, f"the error tips is not right,acutal error is {data[field]} "

# def assert_error_message(response,status_code,message=None):
#     print (response.json())
#     assert response.status_code==status_code, f"期望的状态码{status_code}，实际是{response.status_code}"

#     field="message"
#     if message is not None:
#         data= response.json()
#         assert field in data, f"错误字段 message 不存在: {data}"
#         if message is not None:
#             assert data[field]==message, f"the error tips is not right,acutal error is {data[field]} "
