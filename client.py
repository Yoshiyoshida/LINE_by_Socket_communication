#Client Side

import datetime
import socket


fin_key = "quit".encode("utf-8")#バイナリデータ

def main():
    HOST = "localhost"
    PORT = 50006
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#設定
    client.connect((HOST, PORT))

    print("**************LINE**************")

    while(1):
        data = client.recv(1024)#データの受信が1024byteまで
        print("-相手(Server):", data.decode("utf-8"))# サーバー側の書き込みを表示

        while (1):
            dt_now = datetime.datetime.now()
            data = str(dt_now.day ).encode("utf-8")
            data = str(dt_now.time ).encode("utf-8")
            data += input("●自分(Client):").encode("utf-8") # 入力待機
            if len(data) != 0:
                break
            else:
                print("Computer: 入力し直してください")

        client.send(data)# ソケットに入力したデータを送信
        if data == fin_key:# quitが押されたら終了
            client.close()
            break


if __name__ == '__main__':
    main()
"""
MEMO
なんか知らないけどmacだと送るときにバイナリデータにしないといけない感じがする。
なので送る前に一度エンコードする。
送ってからそれをデコードして読める形にする。
"""