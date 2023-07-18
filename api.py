import base64
import json
import uuid
import random
import string
import requests
import urllib.parse
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
    
    def renewal_subscription(self, email:str, totalGB:int=None, days=30) -> dict:
        data = self.get_client_stats(email)
        if not totalGB:
            totalGB = data["total"]
        rt = self.get_remaining_time(email)
        rv = self.get_remaining_volume(email)
        if totalGB != 0 and (rt > 0 or rt == -1):
            totalGB += rv
        else:
            self.reset_client_traffic(email)
        for client in self.get_clients_of_inbound(data["inboundId"]):
            if client["email"] == email:
                break
        exptime = int((datetime.now() + timedelta(days=days)).timestamp() * 1000)
        r = self.edit_client(
            id_=client["id"],
            alterId=client["alterId"],
            email=email,
            totalGB=totalGB,
            expTime=exptime,
            tgId=client["tgId"],
            enabled=True,
            subId=client["subId"]
        )
        return r
        
    def get_remaining_volume(self, email:str) -> None:
        data = self.get_client_stats(email)
        if data["total"] == 0:
            return -1 # no limit
        remain = data["total"] - (data["up"] + data["down"])
        if remain <= 0:
            return 0 # end
        return remain # remaining volume

    def get_remaining_time(self, email:str) -> None:
        data = self.get_client_stats(email)
        if data["expiryTime"] == 0:
            return -1 # no limit
        remaining_time_ms = data["expiryTime"] - int(datetime.now().timestamp() * 1000)
        if remaining_time_ms <= 0:
            return 0  # expired, return 0 seconds
        return remaining_time_ms # remaining time

    def check_account(self, email:str) -> bool:
        rv = self.get_remaining_volume(email)
        rt = self.get_remaining_time(email)
        if rt == -1 and rv == -1:
            return True
        if rt == 0:
            return False
        if rv == 0:
            return False
        if rv > 0 or rt > 0:
            return True
        return False

    def get_client_url(self, email:str, inboundId:int=None) -> str:
        try:
            if not inboundId:
                inboundId = next((inbound["id"] for inbound in self.get_all_inbounds() for client in json.loads(inbound["settings"])["clients"] if client["email"] == email), None)
            client = [x for x in json.loads(self.get_inbound(inboundId)["settings"])["clients"] if x['email']==email][0]
            inbound = panel.get_inbound(inboundId)
            settings = json.loads(inbound["streamSettings"])
            if inbound["protocol"] == "vmess":
                data = {
                    "v": "2",
                    "ps": f"-{email}",
                    "add": self.ip,
                    "port": inbound["port"],
                    "id": client["id"],
                    "aid": 0,
                    "net": settings["network"],
                    "type": settings["tcpSettings"]["header"]["type"],
                    "tls": settings["security"],
                    "path": settings["tcpSettings"]["header"]["request"]["path"][0],
                    "host": settings["tcpSettings"]["header"]["request"]["headers"]["Host"][0]
                }
                return "vmess://" + base64.urlsafe_b64encode(json.dumps(data, indent=2).encode('utf-8')).decode()
            elif inbound["protocol"] == "vless":
                id_ = client["id"]
                port = inbound["port"]
                type_ = settings["network"]
                path = urllib.parse.quote(settings["tcpSettings"]["header"]["request"]["path"][0], safe='')
                host = settings["tcpSettings"]["header"]["request"]["headers"]["Host"][0]
                headertype = settings["tcpSettings"]["header"]["type"]
                return f"vless://{id_}@{self.ip}:{port}?type={type_}&path={path}&host={host}&headerType={headertype}#-{email}"
            return ""
        except:
            return ""

if __name__ == "__main__":
    print(
        """
        this api is specified for https://github.com/alireza0/x-ui/ panel 
        """
    )

    
    
