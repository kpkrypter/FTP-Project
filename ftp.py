import ftplib
import os
import re
import ntpath

def CreateParentDir(Dpath):
    dirname = os.path.dirname(Dpath)
    while not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            print("[+] Created {0}".format(dirname))
        except OSError:
            CreateParentDir(dirname)

def DownloadFile(ftpHandle, name, dest, overwrite):
    CreateParentDir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftpHandle.retrbinary("RETR {0}".format(name), f.write)
            print("[+] Downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("[-] Failed: {0}".format(dest))
    else:
        print("[+] Already exists: {0}".format(dest))

def FilterByExtension(ByExt, name):
    if ByExt is None:
        return True
    else:
        return bool(re.match(ByExt, name))

def CheckIsDir(ftpHandle, name):
    if len(name) >= 4:
        if name[-4] == '.':
            return False
    
    CurrentCWD = ftpHandle.pwd()  
    try:
        ftpHandle.cwd(name) 
        ftpHandle.cwd(CurrentCWD)  
        return True
    
    except ftplib.error_perm as e:
        return False

    except Exception as e:
        return False

def ScanDir(ftpHandle, name, ByExt,overwrite):
    for item in ftpHandle.nlst(name):
        try:
            if CheckIsDir(ftpHandle, item):
                ScanDir(ftpHandle, item, ByExt,overwrite )
            else:                
                if FilterByExtension(ByExt, name):
                    DownloadFile(ftpHandle, item, item, overwrite)
                else:
                    pass
        except:
            print("[-] Disconnected!!!... Try to connect again")
            ftpHandle = ConnectFTP()

def ScanTree(ftpHandle, path, Dest):  
    path = path.lstrip("/")    
    Current_Dir= os.getcwd()  
    os.chdir(Dest)  
    
    ScanDir(ftpHandle, path, None, False)
    
    os.chdir(Current_Dir) 

def ConnectFTP():   
    try:
        host = "IP/SiteName"
        username = "YOURFTPUSER"
        password = "PWD"
        ftp = ftplib.FTP(host, username, password)
        ftp.set_pasv(True)
        print("[*] Connection Successfull.")
        return ftp
    except Exception as ex2:
        print("[-] An exception occurred") 
        print(ex2)

if __name__ == "__main__":
    remoteDir = "YourRemoteFTPFoler/Example"
    localDir = "YourDownloadDestination"
    try:
        ftp = ConnectFTP()
        if ftp:
            ScanTree(ftp, remoteDir, localDir)
    except:
        print("[!] An exception occurred") 