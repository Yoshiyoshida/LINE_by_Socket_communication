#Client Side

import socket

fin_key = "quit"
fin_b = fin_key.encode("utf-8")#バイナリデータ

def main():
    HOST = "localhost"
    PORT = 50007
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#設定
    soc.connect((HOST, PORT))

    print("**************LINE**************")
    #print("入力するには「 - 」を押してください \n")

    while(1):
        data = soc.recv(1024)#データの受信が1024byteまで
        print("-相手(Server):", data.decode("utf-8"))# サーバー側の書き込みを表示

        while (1):
            data = input("●自分(Client):").encode("utf-8") # 入力待機
            if len(data) != 0:
                break
            else:
                print("Computer: 入力し直してください")

        soc.send(data)# ソケットに入力したデータを送信
        if data == fin_b:# quitが押されたら終了
            soc.close()
            break


if __name__ == '__main__':
    main()
"""
MEMO
なんか知らないけどmacだと送るときにバイナリデータにしないといけない感じがする。
なので送る前に一度エンコードする。
送ってからそれをデコードして読める形にする。
"""