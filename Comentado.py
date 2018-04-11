		######################################################################
		#    Trabalho desenvolvido na disciplina de Redes de Computadores    #
		#               Pelos alunos: João Fernando                          #
		#                             Matheus Saggioro                       #
		#                             Luiz Arruda                            #
		#                                                                    # 
		#    Proposta: Desenvolver um servidor HTTP com a linguagem python   #
		######################################################################

import socket 							# Importa a biblioteca socket
 
HOST,PORT = '192.168.100.4',8080                                # Define o IP do host e a PORTA do servidor
meu_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # Cria o socket do servidor
meu_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # Faz com que ao fechar o servidor por exemplo, não de o erro do host e a port ja estarem sendo usados
meu_socket.bind((HOST,PORT))                                    # Define para qual porta e ip o servidor ira estabelecer a conexão
meu_socket.listen(1)                                            # Estabelece o limente de conexões
print('Servidor rodando no IP:',HOST, 'e na PORTA:',PORT)

while True:
    clienteConec, address = meu_socket.accept() # Retorna duas variaveis, uma com informações da conexão do cliente com o servidor e a segunda retorna somente o ip e a porta do cliente (O servidor fica esperando uma conexão)
    request = clienteConec.recv(1024).decode('utf-8')
    string_list = request.split(' ')    	# Corta os a requisição pelos espaçoes em branco separando em um vetor
    method = string_list[0]              	# Passa o método da requisição, que está na posição 0 do vetor
    requesting_file = string_list[1]     	# Passa o arquivo requisitado que está na posição zero do vetor

### Informações importantes para o servidor ###
    print('Endereço do Cliente: ',address)
    print('O Cliente requisitou:',requesting_file)
    print('Requisicao:',request)
###############################################

    arquivo = requesting_file.split('?')[0] 	# Corta após o '?'
    arquivo = arquivo.lstrip('/')     		# apaga tudo antes do '/' na string (Left Strip)
    if(arquivo == ''):               		# Quando o usuario digita somento HOST:PORT arquivo fica com ''
        arquivo = 'index.html'    		# Carrega o arquivo no diretório em que o servidor está salvo

    try:
        pagina = open(arquivo,'rb')        	# Abre o arquivo HTML , 'r' de read , 'b' de byte format
        response = pagina.read()            	# Faz a leitura do arquivo
        pagina.close()                      	# Após salvo o valor, pode fechar a leitura do arquivo
        header = 'HTTP/1.1 200 OK\n'        	# Cabeçalho de sucesso 
        if(arquivo.endswith(".jpg")):       	# Se o final do nome do arquivo terminar com .jpg
            mimetype = 'image/jpg'
        elif(arquivo.endswith(".css")):     	# Se o final do nome do arquivo terminar com .css
            mimetype = 'text/css'	
        else:
            mimetype = 'text/html'         	# Se não ele será text ou html
        header += 'Content-Type: '+str(mimetype)+'\n\n' # Atribui ao campo 'Content-Type' o tipo do arquivo

    except Exception as e:                  	# Caso ele nao encontre o arquivo requisitado dentro do try, ele abre a exceção
        header = 'HTTP/1.1 404 Not Found\n\n'	# Cabeçalho de falha ao encontrar o arquivo
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Servidor Python HTTP</p></center></body></html>'.encode('utf-8')                       # Transforma um texto em html com encode e envia como resposta o erro

    final_response = header.encode('utf-8')  	# Codifica os cabeçalhos de sucesso ou erro
    final_response += response               	# Adiciona a página de resposta, seja de erro ou sucesso
    clienteConec.send(final_response)        	# Pega a conexão entre cliente e servidor e envia o cabeçalho e a página
    clienteConec.close()                     	# Fecha conexão entre cliente e servidor


