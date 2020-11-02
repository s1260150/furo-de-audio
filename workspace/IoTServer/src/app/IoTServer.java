package app;

import java.io.*;
import java.net.*;

public class IoTServer
{
    private ServerSocket serverSock;
    //PORT Number
    public static final int PORT = 50576; //待ち受けポート番号

    public void update()
    {
        try(ServerSocket ss = new ServerSocket(PORT))
        {
            serverSock = ss;

            while(true)
            {
                //サーバー側ソケット作成
                Socket clientSock = serverSock.accept();
                System.out.println("Welcom!");

                Client cc= new Client(clientSock);
                cc.start();
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}

class Client extends Thread
{
    private Socket sock;
    private MyReader reader;
    private MyWriter writer;

    public Client(Socket sc) throws IOException
    {
        this.sock = sc;
        this.reader = new MyReader(sc.getInputStream());
        this.writer = new MyWriter(sc.getOutputStream());

        writer.writeMsg("Welcom!");
    }

    @Override
    public void run()
    {
        //本来であれば一番外側の出力ストリームを指定しなければ
        //バッファリングされたデータがフラッシュされないので注意
        try(OutputStream outStream = sock.getOutputStream())
        {
            while(true)
            {
                new MyFileReceiver(reader).receiveFile("Receive");
            }
        }
        catch(IOException e)
        {
            System.out.println("Connection Closed");
        }
        System.out.println("Good Bye !!");
    }
}