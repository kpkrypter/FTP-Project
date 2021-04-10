import pysftp
from termcolor import colored, cprint
import os

def ScanTree(ftpHandle, path, destination, overwrite=False):   
    path = path.lstrip("/")
    Current_Dir = os.getcwd()  
    os.chdir(destination)  
    with ftpHandle.cd(path):     
        for i in ftp.listdir(): 
            if ftpHandle.isdir(i):           
                ftpHandle.get_r(lstrip("/"),destination, preserve_mtime=True)                
                print(colored("[+] Downloaded: {0}".format(i),'green'))
            else: 
                ftpHandle.get(lstrip("/"), preserve_mtime=True)
                print(colored("[+] Downloaded: {0}".format(i),'green'))
    
    os.chdir(Current_Dir) 

def ConnectFTP():   
    try:
        host = "IP/SiteName"
        username = "YOURSFTPUSER"
        password = "PWD"
        ftp = pysftp.Connection(host, username=username, password=password)        
        print(colored("\n[*] Connection Successfull.",'yellow'))
        return ftp
    except:
        print(colored("[-] An exception occurred",'red'))

if __name__ == "__main__":
    remoteDir = "YourRemoteSFTPFoler/Example"
    localDir = "YourDownloadDestination"
    try:
        ftp = Connect_ftp()   
        if ftp:
            ScanTree(ftp, remote_dir, local_dir, overwrite=False)
    except:
        print(colored("[-] An exception occurred",'red'))