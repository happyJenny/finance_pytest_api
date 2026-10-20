import uuid
class Users_Factory:
    @staticmethod
    def _gen_uuid():
        return uuid.uuid4().hex


    @staticmethod
    def idcard(size):
        return uuid.uuid4().hex[:size] 

    @staticmethod
    def phone(size):
        return uuid.uuid4().hex[:size]


    @staticmethod    
    def build(username=None,prefix="api_test_",**overide):
        random=uuid.uuid4().hex
        register_data = {
            "username": username or f"{prefix}{random[:8]}",
            "password": "jepeng",
            "realName": "api-test",
            "idCard": random[:18],
            "phone": f"185{random[:8]}"
        }
        register_data.update(overide)
        return register_data        