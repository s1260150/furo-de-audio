package app;

import java.io.*;
import FileSystem.*;

public class MyFileReceiver {
    
    private MyReader reader;

    public MyFileReceiver(MyReader reader)
    {
        this.reader = reader;
    }

    public void receiveFile(String dest) throws IOException
    {
        String filename = reader.readMsg();
        System.out.println("filename : " + filename);

        long fileSize = reader.readLong();
        System.out.println("file size : " + fileSize);

        byte[] buffer = new byte[1024];

        try(MyWriter writer = new MyWriter(new FileOutputStream(dest + File.separator + filename)))
        {
            int total = 0;
            while(total < fileSize)
            {
                int bytesRead = reader.readBinary(buffer, 0, (1024 > fileSize - total ? (int)fileSize - total : 1024));
                total += bytesRead;

                writer.writeBinary(buffer);
            }
        }
        System.out.println("Received");
    }
}