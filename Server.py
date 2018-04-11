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
    string_list = request.split(' ')     
    method = string_list[0]             
    requesting_file = string_list[1]     

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
        if(arquivo.endswith(".jpg")):       
            mimetype = 'image/jpg'
        elif(arquivo.endswith(".css")):    
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'         
        header += 'Content-Type: '+str(mimetype)+'\n\n' 

    except Exception as e:          
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Servidor Python HTTP</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8') 
    final_response += response               
    clienteConec.send(final_response)        
    clienteConec.close()                     


