package app;

import java.io.*;

public class MyWriter implements AutoCloseable{
    private OutputStream os;
    private DataOutputStream dos;
    private PrintWriter pw;

    public MyWriter(OutputStream os)
    {
        this.os = os;
        dos = new DataOutputStream(new BufferedOutputStream(os));
        pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(os)));
    }

    public void writeBinary(byte[]... binaries) throws IOException
    {
        try
        {
            for(byte[] binary : binaries)
            {
                dos.write(binary);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    public void writeBinary(byte[] binary, int offset, int length) throws IOException
    {
        try
        {
            dos.write(binary, offset, length);
            dos.flush();
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    //BufferedReader::ReadLine と対応
    public void writeMsg(String... msgs) throws IOException
    {
        try
        {
            for(String msg : msgs)
            {
                pw.println(msg);
                pw.flush();
                if(pw.checkError()) throw new IOException();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            pw.close();
            throw e;
        }
    }

    public void writeInt(Integer... nums) throws IOException
    {
        try
        {
            for(Integer num : nums)
            {
                dos.writeInt(num);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    public void writeLong(Long... nums) throws IOException
    {
        try
        {
            for(Long num : nums)
            {
                dos.writeLong(num);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    public void writeFloat(Float... nums) throws IOException
    {
        try
        {
            for(Float num : nums)
            {
                dos.writeFloat(num);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    public void writeDouble(Double... nums) throws IOException
    {
        try
        {
            for(Double num : nums)
            {
                dos.writeDouble(num);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }
    
    public void writeBoolean(Boolean... bools) throws IOException
    {
        try
        {
            for(Boolean bool : bools)
            {
                dos.writeBoolean(bool);
                dos.flush();
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
            dos.close();
            throw e;
        }
    }

    @Override
    public void close() throws IOException {
        os.close();
    }
}