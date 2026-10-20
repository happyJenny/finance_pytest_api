import requests
class BaseClient:
    def __init__(self,baseURL,token=None,timeout=10):
        self.baseURL=baseURL
        self.token=token
        self.timeout=timeout
    
    def _headers(self):
        return  {"Authorization": f"Bearer {self.token}"} if (self.token) else {}
         

    def get(self,path,raise_on_error=True):
        url=self.baseURL+path
        r=requests.get(url,headers=self._headers(),timeout=self.timeout)
        return self._check_error(r,raise_on_error=raise_on_error)

    def post(self,path,json=None,raise_on_error=True):
        url=self.baseURL+path
        r=requests.post(url,json=json,headers=self._headers(),timeout=self.timeout)
        return self._check_error(r,raise_on_error=raise_on_error)

    def put(self,path,json=None,raise_on_error=True):
        url=self.baseURL+path
        r=requests.put(url,json=json,headers=self._headers(),timeout=self.timeout)
        return self._check_error(r,raise_on_error=raise_on_error)

    def _check_error(self,response,raise_on_error=True):  
        if (not raise_on_error):
                return response
        else:
                assert response.status_code==200, f"请求失败：{response.text}"
                return response.json()["data"]
