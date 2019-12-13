import socket
import pickle



class ProcessData:
    messageType=""
    fileName = ""
    data = ""
    dataNodeAddressList=[]  


def copyFromHdfs(key):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('192.168.56.103', 12347))
        sendData= ProcessData();
        sendData.messageType=4;
        sendData.fileName=key
        data_string = pickle.dumps(sendData)
        filename=client.send(data_string)
        client.send("FINI".encode())
        #from_server = client.recv(4096)
        try:
           data=b""
           while True:
               packet = client.recv(4096)
               if not packet: break
               if packet[-4:]=="FINI".encode():
                 data +=packet[:-4]
                 break
               data += packet
               
               print(packet)
        except:
               print("recv error")
           
        data_variable = pickle.loads(data)
        file = open(data_variable.fileName, 'wb')
        #dump information to that file
        pickle.dump(data_variable.data, file)
        # close the file
        file.close()
        client.close()
        return data_variable.data




def copyToHdfs(key,data):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('192.168.56.103', 12347))

	sendData= ProcessData();
	sendData.messageType=2;
	sendData.fileName=key

	sendData.data=data

	data_string = pickle.dumps(sendData)
	filename=client.send(data_string)
	client.send("FINI".encode())
	from_server = client.recv(4096)
	client.close()
	print (from_server.decode())

def getDataNodeAddress(key):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('192.168.56.103', 12347))

	sendData= ProcessData();
	sendData.messageType=3;
	sendData.fileName=key

	data_string = pickle.dumps(sendData)
	filename=client.send(data_string)

	from_server = client.recv(4096)
	   
	data_variable = pickle.loads(from_server)
	print(data_variable.dataNodeAddressList)
	client.close()
	#print from_server


def sendData():

  file = open("/root/mincemeatpy-workingBranch-2/1_map_output", 'rb')
  data=pickle.load(file)
  copyToHdfs("CCCCC",data)


copyFromHdfs("1_map_output")

