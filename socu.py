import os, time
import requests
from bs4 import BeautifulSoup

UNIPA_LOGIN = "https://unipa.socu.ac.jp/up/faces/login/Com00501A.jsp"  # 公式入口
TARGET_URL  = "https://unipa.socu.ac.jp/up/portal/myportal"            # 例：マイポータル等


from dotenv import load_dotenv
load_dotenv() 
USER = os.getenv("SOCU_USER")  #.envファイルから環境変数を取得
PASS = os.getenv("SOCU_PASS")


from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

UNIPA_LOGIN = "https://unipa.socu.ac.jp/up/faces/login/Com00501A.jsp"

with requests.Session() as s:
    #ログインページ取得
    r = s.get(UNIPA_LOGIN, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # ログイン画面全体のうちuserとパスワードにかかわるところを抽出
    form = soup.select_one("form#form1")

    action = form.get("action") or UNIPA_LOGIN         # ← フォームの action を使う
    action = urljoin(r.url, action)                     # ← 絶対URL化

    #payloadという辞書に変更点を載せる。
    payload = {}
    for inp in form.select("input"):
        name = inp.get("name")
        if not name:
            continue
        payload[name] = inp.get("value", "")

    #ここでパスワードとユーザー名を入力している
    payload["form1:htmlUserId"] = USER
    payload["form1:htmlPassword"] = PASS

    #入力した変更点をサイトに送信してログインしている
    r2 = s.post(action, data=payload, headers={"Referer": r.url}, timeout=15, allow_redirects=True)
    r2.raise_for_status()


    #ログイン後のフォームに移動
    r3 = s.get("https://unipa.socu.ac.jp/up/faces/up/po/Poa00601A.jsp", timeout=15)
    r3.raise_for_status()
    soup3 = BeautifulSoup(r3.text, "html.parser")

    #お知らせの a タグ抽出
    mail_list = []
    mails = soup3.select("a.outputLinkEx")
    for mail in mails:
        title = mail.get_text()
        if title in {"山陽小野田市立山口東京理科大学","東京理科大学","公立諏訪東京理科大学","山陽小野田市HP","公共交通活用フリーパス"}:
            continue
        mail_list.append(title)
print(mail_list)