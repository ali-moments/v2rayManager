import base64
import json
import uuid
import random
import string
import requests
from datetime import datetime, timedelta


class XUI:
    def __init__(self, ip: str, port: str | int, username: str, password: str) -> None:
        self.ip = ip
        self.panel_url = f"http://{ip}:{port}/xui/"
        self.login_url = f"http://{ip}:{port}/login/"
        self.panel_username = username
        self.panel_password = password
        self.session = self.__get_new_session()
        self.logged_in = self.login()

    def login(self) -> bool:
        r = self.session.post(
            self.login_url,
            json={
                "username": self.panel_username,
                "password": self.panel_password,
            },
        )
        if r.status_code == 200:
            return True
        print("[error] API login failed!")
        return False

    def __get_new_session(self) -> requests.Session:
        return requests.Session()

    def get_all_inbounds(self) -> list:
        r = self.session.get(f"{self.panel_url}API/inbounds/")
        if r.status_code == 200:
            data = json.loads(r.content)
            if data["success"]:
                return data["obj"]
        print("[error] Failed to retrieve inbounds!")
        return []

    def get_inbound(self, id_: int) -> dict:
        r = self.session.get(f"{self.panel_url}API/inbounds/get/{id_}")
        if r.status_code == 200:
            data = json.loads(r.content)
            if data["success"]:
                return data["obj"]
        print(f"[error] Failed to retrieve inbound with ID {id_}!")
        return {}

    def add_client_to_inbound(
        self,
        inboundId: int,
        totalGB: int,
        tgId: str = "",
        email: str = "",
    ) -> dict:
        if not email or email in self.get_all_emails():
            email = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            while email in self.get_all_emails():
                email = "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=10)
                )
            
        client_data = {
            "id": str(uuid.uuid4()),
            "alterId": 0,
            "email": email,
            "totalGB": totalGB * (1024**3),
            "expiryTime": int((datetime.now() + timedelta(days=30)).timestamp() * 1000),
            "enable": True,
            "tgId": tgId,
            "subId": "".join(
                random.choices(string.ascii_lowercase + string.digits, k=20)
            ),
        }
        payload = {"id": inboundId, "settings": json.dumps({"clients": [client_data]})}
        r = self.session.post(f"{self.panel_url}API/inbounds/addClient", data=payload)
        if json.loads(r.content)["success"]:
            return {"success": True, "client": client_data}
        return {"success": False, "client": None}

    def get_clients_of_inbound(self, inboundId: int) -> list:
        try:
            return json.loads(self.get_inbound(inboundId)["settings"])["clients"]
        except:
            print(f"[error] Failed to retrive clients of inbound {inboundId}")
            return []

    def del_client(self, cid: str) -> bool:
        for inbound in self.get_all_inbounds():
            for client in json.loads(inbound["settings"])["clients"]:
                if client["id"] == cid:
                    r = self.session.post(
                        f"{self.panel_url}API/inbounds/{inbound['id']}/delClient/{cid}"
                    )
                    return json.loads(r.content)["success"]
        return False

    def edit_client(self,id_: str,alterId: int,email: str,totalGB: int,expTime: int,tgId: str,enabled: bool,subId: str,) -> dict:
        for inbound in self.get_all_inbounds():
            for client in json.loads(inbound["settings"])["clients"]:
                if client["email"] == email:
                    inboundId = inbound["id"]
                    client_data = {
                        "id": id_,
                        "alterId": alterId,
                        "email": email,
                        "totalGB": totalGB * (1024**3),
                        "expiryTime": expTime,
                        "enable": enabled,
                        "tgId": tgId,
                        "subId": subId,
                    }
                    payload = {"id": inboundId, "settings": json.dumps({"clients": [client_data]})}
                    r = self.session.post(
                        f"{self.panel_url}API/inbound/updateClient/{id_}", data=payload
                    )
                    if json.loads(r.content)["success"]:
                        return {"success": True, "client": client_data}
        return {"success": False, "client": None}

    def get_emails_of_inbound(self, inboundId: int) -> list:
        try:
            return [client["email"] for client in self.get_clients_of_inbound(inboundId)]
        except:
            return []
    
    def get_all_emails(self) -> list:
        try:
            return [client["email"] for inboundId in [x["id"] for x in self.get_all_inbounds()] for client in self.get_clients_of_inbound(inboundId)]
        except:
            return []


    def get_all_status(self) -> list:
        try:
            return [client for inbound in self.get_all_inbounds() for client in inbound["clientStats"]]
        except:
            return []
    
    def get_client_stats(self, email: str) -> dict:
        try:
            return [client for inbound in self.get_all_inbounds() for client in inbound["clientStats"] if client["email"]==email][0]
        except IndexError:
            print(f"[error] no user with email: {email} exists!")
            return {}

    def reset_client_traffic(self, email:str) -> bool:
        for inbound in self.get_all_inbounds():
            for client in json.loads(inbound["settings"])["clients"]:
                if client["email"] == email:
                    r = self.session.post(
                        f"{self.panel_url}API/inbounds/{inbound['id']}/resetClientTraffic/{email}"
                    )
                    return json.loads(r.content)["success"]
        return False
    
    def renewal_subscription(self, email:str, totalGB:int=None) -> bool:
        pass

    def get_remaining_volume(self, email:str) -> None:
        
        return self.get_client_stats(email)

    def get_remaining_time(self, email:str) -> None:
        pass

    def check_account(self, email:str) -> bool:
        pass

    def get_client_url(self, inboundId:int, email:str) -> str:
        try:
            client = [x for x in self.get_inbound(inboundId) if x['email']==email][0]
            data = self.__inbound_info(inboundId)
            data["ps"] = f"-{email}"
            data["id"] = client["id"]
            return f"vmess://{base64.urlsafe_b64encode(str(data).encode()).decode()}"
        except:
            return ""

    def __inbound_info(self, inboundId: int) -> dict:
        if inboundId == 1:
            return {"v": "2","ps": None,"add": self.ip,"port": 443,"id": None,"aid": 0,"net": "tcp","type": "http","tls": "none","path": "/","host": "telewebion.com"}
        if inboundId == 2:
            pass
        if inboundId == 4:
            pass
        if inboundId == 5:
            pass
        if inboundId == 6:
            pass
        return {}

if __name__ == "__main__":
    print(
        """
        this api is specified for https://github.com/alireza0/x-ui/ panel 
    """
    )

    panel = XUI(
        ip="5.75.198.82",
        port=1402,
        username="admin",
        password="admin"
    )

    print(panel.get_remaining_volume("T256"))

