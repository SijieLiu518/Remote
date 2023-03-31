import paramiko
import time
import os

class Remote:
    def __init__(self, hostname, username, password, commands, file, localpath, remotepath):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.commands = commands
        self.localpath = localpath
        self.remotepath = remotepath
        self.file = file
        self.ssh, self.trans = self.connect()
        self.sftp = paramiko.SFTPClient.from_transport(self.trans)
        
    def connect(self):
        trans = paramiko.Transport((self.hostname))
        trans.connect(username=self.username, password=self.password)  
        
        ssh = paramiko.SSHClient()
        ssh._transport = trans
        
        return ssh, trans
    
    def close(self):
        self.trans.close()
        
    def upload(self):
        self.sftp.put(localpath=os.path.join(self.localpath+'/degraded', self.file), remotepath=os.path.join(self.remotepath+'/degraded', self.file))
    
    def download(self):
        file = self.file.split('.')[0] + '.png'
        self.sftp.get(remotepath=os.path.join(self.remotepath+'/restored', file), localpath=os.path.join(self.localpath+'/restored', file))
        
    def exec_command(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(self.commands)
        print(ssh_stdout.read().decode())       


if __name__ == '__main__':    
    hostname = '10.177.58.67'
    username = 'videt'
    password = 'videt'
    commands = 'cd lsj_SR/Restormer; \
                rm demo/Deraining/restored/Deraining/Rain100H-62-input.png; \
                nohup /home/videt/miniconda3/envs/pytorch181/bin/python demo.py --task Deraining --input_dir demo/Deraining/degraded --result_dir demo/Deraining/restored > output.log 2>&1 &'
               
    file = 'Rain100H-62-input.jpg' 
    localpath='demo'
    remotepath='lsj_SR/Restormer/demo/Deraining'
            
    server = Remote(hostname, username, password, commands, file, localpath, remotepath)
    server.upload()
    server.exec_command()
    time.sleep(5)
    server.download()
    



    