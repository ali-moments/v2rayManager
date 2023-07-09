from datetime import datetime, timedelta
import json
import requests
import random
import string
import uuid


class XUI:
    def __init__(self, ip:str, port:str|int, username:str, password:str) -> None:
        self.panel_url = f"http://{ip}:{port}/xui/"
        self.login_url = f"http://{ip}:{port}/login/"
        self.panel_username = username
        self.panel_password = password
        self.session = self.__get_new_session()
        self.login()
    
    def login(self) -> int:
        r = self.session.post(
            self.login_url, 
            json={
                "username": self.panel_username, 
                "password": self.panel_password,
            },
        )
        if r.status_code != 200:
            print("[error]api not logged in!")
        return r.status_code
    
    def __get_new_session(self) -> requests.Session:
        return requests.Session()
    
    def get_all_inbounds(self) -> list:
        r = self.session.get(f"{self.panel_url}API/inbounds/")
        data = json.loads(r.content)
        if data["success"]:
            return data["obj"]
        return []
    
    def get_inbound(self, id_:int) -> dict:
        r = self.session.get(f"{self.panel_url}API/inbounds/get/{id_}")
        data = json.loads(r.content)
        if data["success"]:
            return data["obj"]
        return {}
    
    def add_client(self, inboundId:int, totalGB:int, tgId:str="", email:str="",) -> bool:
        if not email:
            email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        client_data = {
            "id": str(uuid.uuid4()),
            "alterId": 0,
            "email": email,
            "totalGB": totalGB * (1024 ** 3),
            "expiryTime": int((datetime.now() + timedelta(days=30)).timestamp() * 1000),
            "enable": True,
            "tgId": tgId,
            "subId": ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        }
        payload = {"id": inboundId, "settings": json.dumps({"clients": [client_data]})}
        r = self.session.post(f"{self.panel_url}API/inbounds/addClient", data=payload)
        return json.loads(r.content)['success']

    def get_clients(self, inboundId:int) -> list:
        return json.loads(self.get_inbound(inboundId)["settings"])["clients"]

    def del_client(self, cid:str) -> bool:
        for inbound in self.get_all_inbounds():
            for client in json.loads(inbound["settings"])["clients"]:
                if client["id"] == cid:
                    r = self.session.post(f"{self.panel_url}API/inbounds/{inbound['id']}/delClient/{cid}")
                    return json.loads(r.content)["success"]
        return False
    



if __name__ == "__main__":
    print("""
        this api is specified for https://github.com/alireza0/x-ui/ panel 
    """)
