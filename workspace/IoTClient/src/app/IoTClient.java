package app;

import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import FileSystem.FileManager;

public class IoTClient{

    public static final String HOST = "localhost";
    public static final int PORT    = 50576;


    private Socket sock;
    private MyWriter writer;
    private MyReader reader;

    public IoTClient()
    {
    }

    public void update() throws IOException
    {
        try(Socket cs = new Socket(HOST, PORT))
        {
            sock = cs;
            writer = new MyWriter(sock.getOutputStream());
            reader = new MyReader(sock.getInputStream());

            
            Thread receiver = new Thread(){
                public void run(){
                    try
                    {
                        while(true){
                            String str = reader.readMsg();
                            System.out.println(str);
                        }
                    }
                    catch(IOException e)
                    {
                        e.printStackTrace();
                    }
                }
            };
            
            Thread sender = new Thread(){
                public void run(){
                    try(MyReader user = new MyReader(System.in))
                    {
                        while(true){
                            String msg = user.readMsg();
                            
                            if(msg.equals("quit")) break;
                            
                            sendFile(msg);
                        }
                    }
                    catch(IOException e)
                    {
                        e.printStackTrace();
                    }
                }
            };

            receiver.start();
            sender.start();

            while(receiver.isAlive() && sender.isAlive());
        }
        finally
        {
            System.out.println("Connection Closed");
        }
    }



    //Runメソッドの実装
    public void run()
    {
        try(Socket cs = new Socket(HOST, PORT))
        {
            sock = cs;
            writer = new MyWriter(sock.getOutputStream());
            reader = new MyReader(sock.getInputStream());

            while(true){
                String str = reader.readMsg();
                System.out.println(str);
            }
        }
        catch(Exception e)
        {
            System.out.println("Connection Closed");
        }
    }

    public void sendFile(String source)
    {
        try
        {
            Path path = Paths.get(new FileManager().resolve(source));
            if(Files.notExists(path))
            {
                System.out.println("\"" + path.toString() + "\"" + " doesn't exists");
                return;
            }

            String filename = path.toFile().getName();
            new MyFileSender(writer).sendFile(path.toString());

            System.out.println("Send : " + filename );
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}

//50576