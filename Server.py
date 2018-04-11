import socket 
 
HOST,PORT = '192.168.100.4',8080                                
meu_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
meu_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
meu_socket.bind((HOST,PORT))                                    
meu_socket.listen(1)                                            
print('Servidor rodando no IP:',HOST, 'e na PORTA:',PORT)

while True:
    clienteConec, address = meu_socket.accept()
    request = clienteConec.recv(1024).decode('utf-8')
    requesting_file = request.split(' ')[1]     

    print('Endereço do Cliente: ',address)
    print('O Cliente requisitou:',requesting_file)
    print('Requisicao:',request)
    
    arquivo = requesting_file.split('?')[0] 
    arquivo = arquivo.lstrip('/')    
    if(arquivo == ''):                
        arquivo = 'index.html'    

    try:
        pagina = open(arquivo,'rb')         
        response = pagina.read()            
        pagina.close()                      
        header = 'HTTP/1.1 200 OK\n'               
        header += 'Content-Type: '+str('text/html')+'\n\n'
    except Exception as e:          
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Servidor Python HTTP</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8') 
    final_response += response               
    clienteConec.send(final_response)        
    clienteConec.close()                     


