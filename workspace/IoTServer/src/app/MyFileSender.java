package app;

import java.io.*;

public class MyFileSender {
    
    private MyWriter writer;

    public MyFileSender(MyWriter writer)
    {
        this.writer = writer;
    }

    public void sendFile(String source) throws IOException, FileNotFoundException
    {
        try(MyReader reader = new MyReader(new FileInputStream(source)))
        {
            String filename = new File(source).getName();
            writer.writeMsg(filename);

            byte[] buffer = new byte[1024];
            long fileSize = new File(source).length();
            writer.writeLong(fileSize);

            int bytesRead = 0;
            while((bytesRead = reader.readBinary(buffer)) != -1)
            {
                writer.writeBinary(buffer, 0, bytesRead);
            }

            System.out.println("Sended");
        }
    }
}