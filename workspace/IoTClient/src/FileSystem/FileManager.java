package FileSystem;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Stream;

public class FileManager implements Cloneable
{
    private Path cd;

    public FileManager()
    {
        this.cd = Paths.get(new File(".").getAbsoluteFile().getParent());
    }
    public FileManager(String path)
    {
        this.cd = Paths.get(new File(".").getAbsoluteFile().getParent()).resolve(path).normalize();
    }

    public static File toFile(String path)
    {
        return new File(path);
    }
    public static File toFile(Path path)
    {
        return path.toFile();
    }

    public static Path toPath(String path)
    {
        return Paths.get(path);
    }
    public static Path toPath(File file)
    {
        return file.toPath();
    }

    public Path resolve(Path path)
    {
        return cd.resolve(path).normalize();
    }

    public String resolve(String path)
    {
        return resolve(Paths.get(path)).toString();
    }

    public InputStream getInputStream(Path filename) throws FileNotFoundException
    {
        Path dest = cd.resolve(filename).normalize();

        return new FileInputStream(dest.toString());
    }

    public OutputStream getOutputStream(Path filename) throws FileNotFoundException
    {
        Path dest = cd.resolve(filename).normalize();

        return new FileOutputStream(dest.toString());
    }

    public Path makeFile(Path filename) throws IOException, InvalidPathException
    {
        Path dest = cd.resolve(filename).normalize();

        if(Files.exists(dest)) 
        {
            if(!dest.toFile().isFile()) throw new InvalidPathException(filename, "A Directory with same name already exists");
            
            return dest;
        }

        return Files.createFile(dest);
    }
    public String makeFile(String filename) throws IOException, InvalidPathException
    {
        return makeFile(Paths.get(filename)).toString();
    }

    public Path makeDirectory(Path filename) throws IOException, InvalidPathException
    {
        Path dest = cd.resolve(filename).normalize();
        
        if(Files.exists(dest)) 
        {
            if(dest.toFile().isFile()) throw new InvalidPathException(filename, "A file with same name already exists");
            
            return dest;
        }

        return Files.createDirectory(dest);
    }
    public String makeDirectory(String filename) throws IOException, InvalidPathException
    {
        return makeDirectory(Paths.get(filename)).toString();
    }

    public Path move(Path path) throws InvalidPathException
    {
        Path next = cd.resolve(path).normalize();
        if(Files.notExists(next)) throw new InvalidPathException(path, "Invalid Path");
        if(next.toFile().isFile()) throw new InvalidPathException(path, "The file with same name exists");
        return cd = next; 
    }
    public String move(String path) throws InvalidPathException
    {
        return move(Paths.get(path)).toString();
    }

    
    public Path moveFile(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isFile()) throw new NoSuchFileException("\"" + source + "\"");

        if(dest.toFile().isFile()) throw new IOException("\"" + destination.toString() + "\"" + " already exists");
        else if(dest.toFile().isDirectory())
        {
            dest = dest.resolve(src.getFileName());
        }

        if(Files.notExists(dest.getParent())) throw new InvalidPathException(destination, "Invalid Path");
        if(Files.exists(dest)) throw new IOException("\"" + dest.toString() + "\"" + " already exists");
        
        return Files.move(src, dest);
    }
    public String moveFile(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveFile(Paths.get(source), Paths.get(destination)).toString();
    }
    
    public Path moveFiles(Path source, Path destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        if(!dest.toFile().isDirectory()) throw new InvalidPathException(destination, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        for(File file : list)
        {
            if(file.isFile()) 
            {
                moveFile(file.toPath(), destination);
            }
        }
        return destination.normalize();
    }
    public Path moveFiles(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveFiles(source, destination, "");
    }
    public String moveFiles(String source, String destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveFiles(Paths.get(source), Paths.get(destination), filter).toString();
    }
    public String moveFiles(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveFiles(Paths.get(source), Paths.get(destination), "").toString();
    }






    public Path moveDirectory(Path source, Path destination) throws IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(src.getRoot().toString() == src.toString()) throw new InvalidPathException(source, "can't move the root directory");

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        
        if(dest.toFile().isFile()) throw new IOException("\"" + destination.toString() + "\"" + " already exists");
        else if(dest.toFile().isDirectory())
        {
            dest = dest.resolve(src.getFileName());
        }
        
        if(Files.notExists(dest.getParent())) throw new InvalidPathException(destination, "Invalid Path");
        if(Files.exists(dest)) throw new IOException("\"" + dest.toString() + "\"" + " already exists");

        return Files.move(src, dest);
    }
    public String moveDirectory(String source, String destination) throws IOException, InvalidPathException
    {
        return moveDirectory(Paths.get(source), Paths.get(destination)).toString();
    }

    public Path moveDirectories(Path source, Path destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        if(!dest.toFile().isDirectory()) throw new InvalidPathException(destination, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        for(File file : list)
        {
            if(file.isDirectory()) 
            {
                moveDirectory(file.toPath(), destination);
            }
        }
        return destination.normalize();
    }
    public Path moveDirectories(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveDirectories(source, destination, "");
    }
    public String moveDirectories(String source, String destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveDirectories(Paths.get(source), Paths.get(destination), filter).toString();
    }
    public String moveDirectories(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return moveDirectories(Paths.get(source), Paths.get(destination), "").toString();
    }


    public void moveAll(Path source, Path destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        moveFiles(source, destination, filter);
        moveDirectories(source, destination, filter);
    }
    public void moveAll(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        moveAll(source, destination, "");
    }
    public void moveAll(String source, String destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        moveAll(Paths.get(source), Paths.get(destination), filter);
    }
    public void moveAll(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        moveAll(source, destination, "");
    }



    public Path copyFile(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isFile()) throw new NoSuchFileException("\"" + source + "\"");

        if(dest.toFile().isFile()) throw new IOException("\"" + destination.toString() + "\"" + " already exists");
        else if(dest.toFile().isDirectory())
        {
            dest = dest.resolve(src.getFileName());
        }

        if(Files.notExists(dest.getParent())) throw new InvalidPathException(destination, "Invalid Path");
        if(Files.exists(dest)) throw new IOException("\"" + dest.toString() + "\"" + " already exists");
        
        return Files.copy(src, dest);
    }
    public String copyFile(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyFile(Paths.get(source), Paths.get(destination)).toString();
    }

    public Path copyFiles(Path source, Path destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        if(!dest.toFile().isDirectory()) throw new InvalidPathException(destination, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        for(File file : list)
        {
            if(file.isFile()) 
            {
                copyFile(file.toPath(), destination);
            }
        }
        return destination.normalize();
    }
    public Path copyFiles(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyFiles(source, destination, "");
    }
    public String copyFiles(String source, String destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyFiles(Paths.get(source), Paths.get(destination), filter).toString();
    }
    public String copyFiles(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyFiles(Paths.get(source), Paths.get(destination), "").toString();
    }





    
    public Path copyDirectory(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        
        if(dest.toFile().isFile()) throw new IOException("\"" + destination.toString() + "\"" + " already exists");
        else if(dest.toFile().isDirectory())
        {
            dest = dest.resolve(src.getFileName());
        }
        
        if(Files.notExists(dest.getParent())) throw new InvalidPathException(destination, "Invalid Path");
        if(Files.exists(dest)) throw new IOException("\"" + dest.toString() + "\"" + " already exists");

        
        final Path des = dest;
        try(Stream<Path> walk = Files.walk(source))
        {
            walk.sorted(Comparator.naturalOrder())
            .map(Path::toFile)
            .forEach(file ->
            {
                Path target = des.resolve(source.relativize(file.toPath()));
                System.out.println("source : " + file.toPath().toString() + ", dest : " + target.toString());
                try
                {
                    Files.copy(file.toPath(), target);
                }
                catch(IOException e)
                {
                    throw new UncheckedIOException(e);
                }
            });
        }

        return destination.normalize();
    }
    public String copyDirectory(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyDirectory(Paths.get(source), Paths.get(destination)).toString();
    }

    public Path copyDirectories(Path source, Path destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        Path src = cd.resolve(source).normalize();
        Path dest = cd.resolve(destination).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(source, "No Such Directory");
        if(!dest.toFile().isDirectory()) throw new InvalidPathException(destination, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        for(File file : list)
        {
            if(file.isDirectory()) 
            {
                copyDirectory(file.toPath(), destination);
            }
        }
        return destination.normalize();
    }
    public Path copyDirectories(Path source, Path destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyDirectories(source, destination, "");
    }
    public String copyDirectories(String source, String destination, String filter) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyDirectories(Paths.get(source), Paths.get(destination), filter).toString();
    }
    public String copyDirectories(String source, String destination) throws NoSuchFileException, IOException, InvalidPathException
    {
        return copyDirectories(source, destination, "").toString();
    }













    public boolean removeFile(Path path) throws InvalidPathException, IOException
    {
        Path target = cd.resolve(path).normalize();

        if(!target.toFile().isFile()) throw new InvalidPathException(path, "No Such File");

        Files.delete(target);

        return Files.notExists(target);
    }
    public boolean removeFile(String path) throws InvalidPathException, IOException
    {
        return removeFile(Paths.get(path));
    }

    public void removeFiles(Path path, String filter) throws InvalidPathException, IOException
    {
        Path src = cd.resolve(path).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(path, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        boolean result = true;
        for(File file : list)
        {
            if(file.isFile()) 
            {
                result &= file.delete();
            }
        }

        if(!result) throw new IOException("Some files could not be deleted.");
    }
    public void removeFiles(Path path) throws InvalidPathException, IOException
    {
        removeFiles(path, "");
    }
    public void removeFiles(String path, String filter) throws InvalidPathException, IOException
    {
        removeFiles(Paths.get(path), filter);
    }
    public void removeFiles(String path) throws InvalidPathException, IOException
    {
        removeFiles(Paths.get(path), "");
    }
    

    public boolean removeDirectory(Path path) throws InvalidPathException, IOException
    {
        Path target = cd.resolve(path).normalize();

        if(!target.toFile().isDirectory()) throw new InvalidPathException(path, "No Such Directory");
        
        try(Stream<Path> walk = Files.walk(target))
        {
            walk.sorted(Comparator.reverseOrder())
            .map(Path::toFile)
            .forEach(File::delete);
        }

        return Files.notExists(target);
    }
    public boolean removeDirectory(String path) throws InvalidPathException, IOException
    {
        return removeDirectory(Paths.get(path));
    }

    public void removeDirectories(Path path, String filter) throws IOException, InvalidPathException
    {
        Path src = cd.resolve(path).normalize();

        if(!src.toFile().isDirectory()) throw new InvalidPathException(path, "No Such Directory");

        File[] list = src.toFile().listFiles((File file, String filename) ->
        {
            return filename.indexOf(filter) != -1;
        });

        boolean result = true;
        for(File directory : list)
        {
            if(directory.isDirectory()) 
            {
                result &= removeDirectory(directory.toPath());
            }
        }

        if(!result) throw new IOException("Some Directories could not be deleted.");
    }
    public void removeDirectories(Path path) throws IOException, InvalidPathException
    {
        removeDirectories(path, "");
    }
    public void removeDirectories(String path, String filter) throws InvalidPathException, IOException
    {
        removeDirectories(Paths.get(path), filter);
    }
    public void removeDirectories(String path) throws InvalidPathException, IOException
    {
        removeDirectories(Paths.get(path), "");
    }


    public void removeAll(Path path, String filter) throws InvalidPathException, IOException
    {
        removeFiles(path, filter);
        removeDirectories(path, filter);
    }
    public void removeAll(Path path) throws InvalidPathException, IOException
    {
        removeAll(path, "");
    }
    public void removeAll(String path, String filter) throws InvalidPathException, IOException
    {
        removeAll(Paths.get(path), filter);
    }
    public void removeAll(String path) throws InvalidPathException, IOException
    {
        removeAll(Paths.get(path));
    }





    public Path getPath()
    {
        return cd;
    }

    @Override
    public FileManager clone()
    {
        FileManager v = null;

        try
        {
            v = (FileManager)super.clone();
            v.cd = Paths.get(cd.toString());
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
        
        return v;
    }

    private class InvalidPathException extends Exception
    {
	    private static final long serialVersionUID = 1L; 

        InvalidPathException(Path filename){
            super("\"" + filename.toString() + "\" is invalid");
        }
        InvalidPathException(Path filename, String reason){
            super("\"" + filename.toString() + "\" is invalid\n" + reason);
        }
    }
}