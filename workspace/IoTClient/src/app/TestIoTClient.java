package app;

import java.io.IOException;

public class TestIoTClient {
    public static void main(String[] args)
    {
        try
        {
            IoTClient client = new IoTClient();
            client.update();
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
    }   
}