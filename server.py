#Server Side

import socket

def main():
    fin_key = "quit"
    fin_b = fin_key.encode("utf-8")#バイナリデータ

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#設定
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)# 'Address already in use' の回避策 (必須ではない)
  
    host = "localhost"
    port = 50007
    s.bind((host, port))# 指定したホスト(IP)とポートをソケットに設定
    print("'Waiting for connections...\n")
    s.listen(1)# 1つの接続要求を待つ/一対一
    soc, addr = s.accept()# 要求が来るまで待機
    print("Conneted by"+str(addr))#サーバ側の合図
    print("**************LINE*************")
    #print("入力するには「 - 」を押してください \n")
    
    while (1):
        while (1):
            data = input("●自分(Server):").encode("utf-8")# 入力待機(サーバー側)
            if len(data) != 0:
                break
            else:
                print("Computer: もう一度入力してください")

        soc.send(data)# ソケットにデータを送信
        data = soc.recv(1024)# データを受信（1024バイトまで）
        print("-相手(Client):",data.decode("utf-8"))# サーバー側の書き込みを表

        if data == fin_b:# quitが押されたら終了
            soc.close()
            print('Bye-Bye:' + str(addr))
            break


if __name__ == '__main__':
    main()

"""
MEMO
なんか知らないけどmacだと送るときにバイナリデータにしないといけない感じがする。
なので送る前に一度エンコードする。
送ってからそれをデコードして読める形にする。
"""