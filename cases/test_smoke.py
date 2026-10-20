import requests,pytest
from config.loader import load_config
from utils.assertions import assert_amount_equal
CFG = load_config()
def test_ok_test():
    response=requests.get(f"{CFG['base_url']}/api/ping",timeout=CFG.get("timeout", 10))
    assert response.text=="pong"
    assert response.status_code==200

def test_assertion_works():
    assert_amount_equal(100, 100.00)  # 不报错，正常通过 
    """断言函数能检测到不等"""
    with pytest.raises(AssertionError):
        assert_amount_equal(100, 999)