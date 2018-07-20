import socket
import threading

class SocketClient():
    #トーク退出のword
    global end_key 
    end_key = "end"
    def __init__(self, name):
        self.host = socket.gethostname()
        self.port = 50007
        self.client_name = name


    def socket_client_up(self):
        
        # クライアントソケット作成(IPv4, TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # サーバソケットへ接続しに行く(サーバのホスト名, ポート番号)
                sock.connect((self.host, self.port))
                # スレッド作成
                thread = threading.Thread(target=self.handler, args=(sock,), daemon=True)
                # スレッドスタート
                thread.start()
                sock.send(("※※※※※※{}さんが入室しました※※※※※※".format(self.client_name)).encode())
                print('{}さん、こんにちは。チャットを開始します。'.format(self.client_name))
                # クライアントからメッセージを送る
                self.send_message(sock)
            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                print('ソケットサーバに接続を拒否されました。')
                print('先にソケットサーバを立ち上げてください')

    def send_message(self, sock):
        while True:
            try:
                my_message = input()
                # 文字入力＋ユーザ名をメッセージに格納
                msg = "●{}:".format(self.client_name) + my_message
            except KeyboardInterrupt:
                #例外のkeyが入力された際の処理
                print("[Computer]もう一度入力してください")
                continue
            if msg == ('●{}:'+end_key).format(self.client_name):
                msg = '{} さんが退出しました。'.format(self.client_name)
                # 退出メッセージの送信
                sock.send(msg.encode('utf-8'))
                break
            elif msg:
                try:
                    sock.send(msg.encode('utf-8'))
                except ConnectionRefusedError:
                    # 接続先のソケットサーバが立ち上がっていない場合、
                    # 接続拒否になることが多い
                    break
                except ConnectionResetError:
                    break

    def handler(self, sock):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                data = sock.recv(1024)
                print(data.decode("utf-8"))
            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                break
            except ConnectionResetError:
                break


if __name__ == "__main__":
    print("##########LINE##########")
    print("最大ユーザ数：５人")
    info = "トーク終了時は「{}」を入力してください".format(end_key)
    print(info)
    print("人数情報：「member」")
    print("天気情報:「weather」")
    while True:
        print("名前を入力してください：",end="")
        client_name = str(input()).strip()
        if len(client_name) >=1:
            break
        
    sc = SocketClient(client_name)
    sc.socket_client_up()