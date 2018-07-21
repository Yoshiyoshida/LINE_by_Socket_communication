import json
import socket
import threading
import requests


class SocketServer():
    member_count = 0
    def __init__(self):
        #self.host = socket.gethostname()
        self.host = "localhost"
        self.port = 50007
        self.clients = []
        self.member_count = 0

    def socket_server_up(self):
        # ソケットサーバ作成(IPv4, TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 接続待ちするサーバのホスト名とポート番号を指定
        try:
            sock.bind((self.host, self.port))
        except OSError:
            print("ポートが使用中です")
            print("接続しなおしてください")
        # 5 ユーザまで接続を許可
        sock.listen(5)

        while True:
            try:
                # 接続要求を受信
                conn, addr = sock.accept()
            except KeyboardInterrupt:
                break
            # アドレス確認
            print("[接続]{}".format(addr))
            # クライアントを追加
            self.clients.append((conn, addr))
            self.member_count += 1
            # 各ユーザのスレッド作成
            thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
            # スレッドスタート
            thread.start()
            

    def close_connection(self, conn, addr):
        print('[切断]{}'.format(addr))
        # 通信を遮断する
        conn.close()
        # クライアントを除外する
        self.clients.remove((conn, addr))
        self.member_count -= 1
    
    def weather_api(self):
        API_KEY = "67b1900b35302d14a27601e16e326625"
        url = "http://api.openweathermap.org/data/2.5/weather?id=1850147&units=metric&appid={}".format(API_KEY)
        res = requests.get(url)
        weather_datas = json.loads(res.text)
        weather = weather_datas["weather"][0]["main"]
        return ("明日の東京の天気は{}です".format(weather)).encode()

    def handler(self, conn, addr):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                data = conn.recv(1024)
            except ConnectionResetError:
                # クライアント側でソケットを強制終了(Ctrl + c)すると
                # ソケットサーバが処理落ちするので、コネクションを切断する
                self.close_connection(conn, addr)
                break

            if not data:
                # データが無い場合、接続を切る
                self.close_connection(conn, addr)
                break
            else:
                
                if data.find(b'weather') > 0:
                    data = self.weather_api()
                elif data.find(b'member') > 0:
                    data = "{}名".format(str(self.member_count)).encode()

                print('data : {}, addr&port: {}'.format(data, addr))
                for client in self.clients:
                    try:
                        client[0].sendto(data, client[1])
                    except ConnectionResetError:
                        print("通信エラー")
                        break

if __name__ == "__main__":
    print("サーバーを立ち上げます")
    ss = SocketServer()
    ss.socket_server_up()

