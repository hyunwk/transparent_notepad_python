# -*- coding:utf-8 -*-
import urllib3
import json
import base64
import sounddevice as sd
def play_audio():
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "89334df6-5042-4381-ac37-63341ef90e72"

    audioFilePath = "./output.wav"
    languageCode = "korean"

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    print("[responseCode] " + str(response.status))
    print("[responBody]")
    print("===== 결과 확인 ====")
    data = json.loads(response.data.decode("utf-8", errors='ignore'))
    print(data['return_object']['recognized'])