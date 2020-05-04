package app;

import java.io.*;

public class MyReader implements AutoCloseable{
    private InputStream is;
    private BufferedReader br;
    private DataInputStream dis;

    public MyReader(InputStream is)
    {
        this.is = is;
        this.br = new BufferedReader(new InputStreamReader(is));
        this.dis = new DataInputStream(new BufferedInputStream(is));
    }

    public String readMsg() throws IOException
    {
        return br.readLine();
    }

    public int readBinary() throws IOException
    {
        return dis.read();
    }
    public int readBinary(byte[] buffer) throws IOException
    {
        return dis.read(buffer);
    }

    public int readBinary(byte[] buffer, int offset, int length) throws IOException
    {
        return dis.read(buffer, offset, length);
    }

    public int readInt() throws IOException
    {
        return dis.readInt();
    }

    public long readLong() throws IOException
    {
        return dis.readLong();
    }

    public Float readFloat() throws IOException
    {
        return dis.readFloat();
    }

    public double readDouble() throws IOException
    {
        return dis.readDouble();
    }

    public boolean readBoolean() throws IOException
    {
        return dis.readBoolean();
    }


    @Override
    public void close() throws IOException {
        is.close();
    }
}