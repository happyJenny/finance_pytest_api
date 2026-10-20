from data.user_factory import Users_Factory
class AuthAPI:
    def __init__(self,client):
        self.client=client
            

    def login(self,username,password,raise_on_error=True):
        login_data = {
        "username":username,
        "password": password
        }
        return self.client.post("/api/auth/login",json=login_data,raise_on_error=raise_on_error)

    def register(self,username,idCard,phone,raise_on_error=True,**overide):
        register_data = {
            "username": username,
            "password": "jepeng",
            "realName": username,
            "idCard": idCard,
            "phone": phone
        }
        register_data.update(overide)
        print(f"[REGISTER BODY] {register_data}") 
        # import json
        # print("SEND JSON:", json.dumps(register_data, ensure_ascii=False))
        return self.client.post("/api/auth/register",json=register_data,raise_on_error=raise_on_error)    

    def register_tx(self,raise_on_error=True):
        payload= Users_Factory.build()
        print(f"-----{payload}")
        return self.client.post("/api/auth/register",json=payload,raise_on_error=raise_on_error)    

  