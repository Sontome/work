import aiohttp
import json
import re
import asyncio

class PowerCallClient:
    def __init__(self, cookie_file="statevna.json"):
        self.cookie_file = cookie_file
        self.session = None
        self.cookies = self._load_cookies()

        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://wholesale.powercallair.com/booking/findSkdFareGroup.lts?mode=v3"
        }

        self.url = "https://wholesale.powercallair.com/booking/findSkdFareGroup.lts?viewType=xml"

    # ===== util =====
    def _load_cookies(self):
        with open(self.cookie_file, "r", encoding="utf-8") as f:
            raw = json.load(f)["cookies"]
        return {c["name"]: c["value"] for c in raw}

    def _js_object_to_json(self, text: str):
        text = re.sub(r'([{,]\s*)([A-Za-z0-9_]+)\s*:', r'\1"\2":', text)
        text = re.sub(r'([{,]\s*)(\d+)\s*:', r'\1"\2":', text)
        return json.loads(text)

    def _parse_response(self, text: str):
        text = text.strip()

        if not text:
            return "EMPTY", None

        if "<html" in text.lower():
            return "HTML", text[:300]

        if text.startswith("{") and '"' in text:
            try:
                return "JSON", json.loads(text)
            except Exception as e:
                return "JSON_ERROR", str(e)

        try:
            return "JS_OBJECT", self._js_object_to_json(text)
        except Exception as e:
            return "JS_OBJECT_ERROR", str(e)

    # ===== session =====
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(
            cookies=self.cookies,
            headers=self.headers,
            connector=connector
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    # ===== API =====
    async def getfulllistCA(self):
        form_data = {
            "mode": "v3",
            "qcars": "",
            "trip": "RT",
            "dayInd": "N",
            "strDateSearch": "202601",
            "day": "",
            "plusDate": "",
            "daySeq": "0",
            "dep0": "ICN",
            "dep1": "HAN",
            "dep2": "",
            "dep3": "",
            "arr0": "HAN",
            "arr1": "ICN",
            "arr2": "",
            "arr3": "",
            "depdate0": "20260102",
            "depdate1": "20260103",
            "depdate2": "",
            "depdate3": "",
            "retdate": "20260103",
            "val": "",
            "comp": "Y",
            "adt": "1",
            "chd": "0",
            "inf": "0",
            "car": "YY",
            "idt": "ALL",
            "isBfm": "Y",
            "CBFare": "YY",
            "skipFilter": "Y",
            "miniFares": "Y",
            "sessionKey": ""
        }

        async with self.session.post(self.url, data=form_data) as resp:
            text = await resp.text()
            status, data = self._parse_response(text)

            if status != "JSON":
                return {"status": status, "raw": data}

        ca_list = []
        VA =data.get("FILTER", {}).get("VA", [])
        SK =data.get("FILTER", {}).get("SK", [])
        MA=data.get("FILTER", {}).get("MA", [])
        XA=data.get("FILTER", {}).get("XA", [])
        for item in data.get("FILTER", {}).get("CA", []):
            ca_list.append({
                "hang": item.get("value"),
                "ten": item.get("label"),
                "status": item.get("ST"),
                "gia_min": item.get("MA"),
                "gia_full": item.get("XA")
            })

        return {
            "status": "OK",
            "SessionKey": data.get("SessionKey"),
            "CA": ca_list,
            "VA":VA,
            "SK" :SK,
            "MA":MA,
            "XA":XA
        }

    async def getflights(
        self,
        repca:dict,
        session_key: str,
        activedCar: str,
        dep0: str,
        dep1: str,
        depdate0: str,
        depdate1: str | None = None,
        activedVia: str = "0"
    ):
        is_rt = bool(depdate1)

        form_data = {
            "qcars": "",
            "mode": "v3",
            "activedCar": activedCar,
            "activedCLSS1": "Y,Q,S,B,U,K,M,Q,U,E,L,T,R,H,B,Y,S,N,V",
            "activedCLSS2": "Y,Q,S,B,U,K,M,Q,U,E,L,T,R,H,B,Y,S,N,V",
            "activedVia": activedVia,
            "activedStatus": "OK,HL",
            "activedIDT": "ADT,STU,VFR,LBR",
            "minAirFareView": "0",
            "maxAirFareView": "2000000",
            "page": "1",
            "sort": "priceAsc",
            "filterTimeSlideMin0": "005",
            "filterTimeSlideMax0": "2355",
            "filterTimeSlideMin1": "005",
            "filterTimeSlideMax1": "2355",
            "trip": "RT" if is_rt else "OW",
            "dayInd": "N",
            "strDateSearch": depdate0[:6],
            "daySeq": "0",
            "dep0": dep0,
            "dep1": dep1,
            "dep2": "", 
            "dep3": "",
            "arr0": dep1,
            "arr1": dep0 if is_rt else "",
            "arr2": "",
             "arr3": "",
            "depdate0": depdate0,
            "depdate1": depdate1 or "",
            "depdate2": "",
            "depdate3": "",
            "retdate": depdate1 or "",
            "comp": "Y",
            "adt": "1",
            "chd": "0",
            "inf": "0",
            "car": "YY",
            "idt": "ALL",
            "isBfm": "Y",
            "CBFare": "YY",
            "miniFares": "Y",
            "sessionKey": session_key
        }

        # activedAirport theo trip
        if is_rt:
            form_data["activedAirport"] = f"{dep0}-{dep1}-{dep1}-{dep0}"
        else:
            form_data["activedAirport"] = f"{dep0}-{dep1}"

        async with self.session.post(self.url, data=form_data) as resp:
            text = await resp.text()
            status, data = self._parse_response(text)

            if status not in ("JSON", "JS_OBJECT"):
                return {"status": status, "raw": data}

        return {
            "status": "OK",
            "PAGE": data.get("PAGE"),
            "TOTALPAGE": data.get("TOTALPAGE"),
            "TOTALFARES": data.get("TOTALFARES"),
            "FARES": data.get("FARES", []),
            "SessionKey": data.get("SessionKey")
        }
async def main():
    async with PowerCallClient() as pc:
        ca = await pc.getfulllistCA()
        
        ca_list = ca.get("CA", [])
        print(ca["SK"])
        sskey = ca.get("SessionKey")
        # check có hãng VN không
        has_vn = any(hang .get("hang") == "VN" for hang in ca_list)
       

        
        if has_vn and  sskey :
            flights = await pc.getflights(
                repca=ca,
                session_key= sskey,
                activedCar= "VN",
                dep0= "ICN",
                dep1= "HAN",
                depdate0= "20260102",
                depdate1= "20260103" ,
                activedVia=  "0")
            print(flights)
            print(sskey)

asyncio.run(main())
