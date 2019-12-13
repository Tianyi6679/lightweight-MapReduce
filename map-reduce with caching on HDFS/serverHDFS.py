import socket
import pickle
import os
import re
class ProcessData:
    messageType=""
    fileName = ""
    data = ""
    dataNodeAddressList=[]


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.56.103', 12347))
serv.listen(5)

#serv.settimeout(0.0)
#serv.setblocking(0)

while True:
    conn, addr = serv.accept()
    #serv.setblocking(0)
    #serv.settimeout(1.0)

    from_client = ''
    try:
      data=b""
      while True:
        packet = conn.recv(4096)
        if not packet: break
        if packet[-4:]=="FINI".encode(): 
          data +=packet[:-4]
          break
        data += packet

        #print(packet)
    except:
       print("recv error")
    print(data)
    data_variable = pickle.loads(data)
    if data_variable.messageType==4:
      command="$HADOOP_HOME/bin/hdfs dfs -copyToLocal /mapreduce/"+data_variable.fileName+ " /root/hdfsTemp2/"
      os.system(command)
      
      file = open("/root/hdfsTemp2/"+data_variable.fileName, 'rb')
      #file = open("/root/hdfsTemp2/fileName453", 'rb')
      baseFileName=os.path.basename(file.name)
      sendData= ProcessData();
      sendData.fileName=baseFileName
      sendData.data=pickle.load(file)
      
      data_string = pickle.dumps(sendData)
      conn.send(data_string)
      conn.send("FINI".encode())  
    elif data_variable.messageType==2:
      file = open("/root/hdfsTemp/"+data_variable.fileName, 'wb')
      pickle.dump(data_variable.data, file)
      file.close()
      print(data_variable.fileName)
      print(data_variable.data)
      print("OS COMMAND CALLED")
      fileName1="$HADOOP_HOME/bin/hdfs dfs -copyFromLocal /root/hdfsTemp/"+data_variable.fileName+ " /mapreduce/"
      os.system(fileName1)
      conn.send("I am SERVER\n".encode())
    elif data_variable.messageType==3:
      command="$HADOOP_HOME/bin/hdfs fsck /mapreduce/"+data_variable.fileName +" -files -blocks -locations | grep 'Data' | sed 's/^.*: //'e"
      result=os.popen(command).read()
      r1 = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b",result)
      print(r1)
      sendData= ProcessData();
      sendData.dataNodeAddressList=r1
      
      data_string = pickle.dumps(sendData)
      conn.send(data_string)
    
    conn.close()
    print ('client disconnected')

