import pickle
import socket
import time

#HOST = "127.0.0.1"  # The server's hostname or IP address #192.168.1.81
#PORT = 9999  # The port used by the server
buffer_size = 1024
m = 1
play = 'Turno del jugador'
serv = 'Turno del servidor'

tablero_n = ("       0      1      2      3 ")
tablero_nums = [[0, "-", "-", "-", "-"],
                [1, "-", "-", "-", "-"],
                [2, "-", "-", "-", "-"],
                [3, "-", "-", "-", "-"]]
tablero_a = ("       0      1      2      3      4      5 ")
tablero_avan = [[0, "-", "-", "-", "-", "-", "-",],
                [1, "-", "-", "-", "-", "-", "-",],
                [2, "-", "-", "-", "-", "-", "-",],
                [3, "-", "-", "-", "-", "-", "-",],
                [4, "-", "-", "-", "-", "-", "-",],
                [5, "-", "-", "-", "-", "-", "-",]]
listasava = [["M", "M", "A", "A","B", "B"],
          ["N", "N", "C", "C", "E", "E"],
          ["F", "F", "K", "K", "S", "S",],
          ["D", "D", "H", "H", "W", "W",],
          ["R", "R", "Z", "Z", "P", "P",],
          ["G", "G", "Y", "Y", "J", "J",]]

# función que imprime el tablero
def table_prin(listas):
    print("\n")
    print(tablero_n)
    print(*listas[0], sep="      ")
    print(*listas[1], sep="      ")
    print(*listas[2], sep="      ")
    print(*listas[3], sep="      ")

# función que imprime el tablero
def table_ava(listas):
    print("\n")
    print(tablero_a)
    print(*listas[0], sep="      ")
    print(*listas[1], sep="      ")
    print(*listas[2], sep="      ")
    print(*listas[3], sep="      ")
    print(*listas[4], sep="      ")
    print(*listas[5], sep="      ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    # Servidor de conexión
    HOST = input("Introduzca la dirección IP del servidor: ")
    # El puerto a utilizar (el servidor debe estar escuchando en este puerto)
    PORT = int(input("Introduzca el puerto de conexión: "))
    TCPClientSocket.connect((HOST, PORT))

    print("------------------Memorama------------------")
    print("**Niveles de dificultad**")
    print("-Principiante")
    print("-Avanzado")
    difi = input("Escoge la dificultad del juego: ")
    didec = difi.encode()
    TCPClientSocket.sendall(didec)
    # Marca de tiempo al inicio del programa
    inicio = time.time()
    
    #Tablero escogido
    tabla = TCPClientSocket.recv(buffer_size)
    respuesta = pickle.loads(tabla)
    
    if(difi == 'Principiante'):
        TCPClientSocket.sendall(b'1')
        table_prin(tablero_nums)

        v = True
        while v:
            while m == 1:
                #TCPClientSocket.sendall(b'1')
                #iden = TCPClientSocket.recv(buffer_size)
                #print(iden.decode())

                iden = TCPClientSocket.recv(buffer_size)

                if iden.decode() == 'Turno del jugador':
                    print("\n",iden.decode())

                if iden.decode() == '1':
                    print("\nGano el jugador\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if iden.decode() == '2':
                    print("\nGano el servidor\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if iden.decode() == '3':
                    print("\nEmpate\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break

                cartas = []
                cartas.clear()
                print("Escoge primera carta")
                num1 = int(input("Primer renglón de 0 a 3: "))
                cartas.append(num1)
                num2 = int(input("Primera columna de 0 a 3: "))
                cartas.append(num2)
                print("Escoge segunda carta")
                num3 = int(input("Segundo renglón de 0 a 3: "))
                cartas.append(num3)
                num4 = int(input("Segunda columna de 0 a 3: "))
                cartas.append(num4)
                env = str(cartas).encode()
                TCPClientSocket.sendall(str(cartas).encode())
                
                dato = TCPClientSocket.recv(buffer_size)

                if dato.decode() == 'Fallaste':
                    print("\n",dato.decode())
                    m = 2
                
                if dato.decode() == 'Jugador +1 punto':
                    print("\n",dato.decode())
                    TCPClientSocket.sendall(b'ok')
                    tabla = TCPClientSocket.recv(buffer_size)
                    respuesta = pickle.loads(tabla)
                    table_prin(respuesta)

            while m == 2:
                iden = TCPClientSocket.recv(buffer_size)
                """
                if iden.decode() == 'Turno del servidor':
                    print(iden.decode())
                    TCPClientSocket.sendall(b'ok')
                """
                if iden.decode() == 'Turno del servidor':
                    print("\n",iden.decode())
                    TCPClientSocket.sendall(b'ok')
                    dato = TCPClientSocket.recv(buffer_size)

                if dato.decode() == '1':
                    print("\nGano el jugador\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == '2':
                    print("\nGano el servidor\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == '3':
                    print("\nEmpate\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == 'Fallo el servidor':
                    print("\n",dato.decode())
                    m = 1
                if dato.decode() == 'Servidor +1 punto':
                    print("\n",dato.decode())
                    TCPClientSocket.sendall(b'ok')
                    tabla = TCPClientSocket.recv(buffer_size)
                    respuesta = pickle.loads(tabla)
                    table_prin(respuesta)

    if (difi == 'Avanzado'):
        TCPClientSocket.sendall(b'1')
        table_ava(tablero_avan)
        v = True
        while v:
            while m == 1:
                # TCPClientSocket.sendall(b'1')
                # iden = TCPClientSocket.recv(buffer_size)
                # print(iden.decode())
                iden = TCPClientSocket.recv(buffer_size)

                if iden.decode() == 'Turno del jugador':
                    print("\n", iden.decode())
                if iden.decode() == '1':
                    print("\nGano el jugador\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if iden.decode() == '2':
                    print("\nGano el servidor\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if iden.decode() == '3':
                    print("\nEmpate\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break

                cartas = []
                cartas.clear()
                print("Escoge primera carta")
                num1 = int(input("Primer renglón de 0 a 3: "))
                cartas.append(num1)
                num2 = int(input("Primera columna de 0 a 3: "))
                cartas.append(num2)
                print("Escoge segunda carta")
                num3 = int(input("Segundo renglón de 0 a 3: "))
                cartas.append(num3)
                num4 = int(input("Segunda columna de 0 a 3: "))
                cartas.append(num4)
                env = str(cartas).encode()
                TCPClientSocket.sendall(str(cartas).encode())

                dato = TCPClientSocket.recv(buffer_size)

                if dato.decode() == 'Fallaste':
                    print("\n", dato.decode())
                    m = 2
                if dato.decode() == 'Jugador +1 punto':
                    print("\n", dato.decode())
                    TCPClientSocket.sendall(b'ok')
                    tabla = TCPClientSocket.recv(buffer_size)
                    respuesta = pickle.loads(tabla)
                    table_ava(respuesta)

            while m == 2:
                iden = TCPClientSocket.recv(buffer_size)
                """
                if iden.decode() == 'Turno del servidor':
                    print(iden.decode())
                    TCPClientSocket.sendall(b'ok')
                """
                if iden.decode() == 'Turno del servidor':
                    print("\n", iden.decode())
                    TCPClientSocket.sendall(b'ok')
                    dato = TCPClientSocket.recv(buffer_size)
                if dato.decode() == '1':
                    print("\nGano el jugador\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == '2':
                    print("\nGano el servidor\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == '3':
                    print("\nEmpate\n")
                    v = False
                    # Marca de tiempo al final del programa
                    fin = time.time()
                    tiempo_total = fin - inicio
                    print("El programa tardó", tiempo_total, "segundos en ejecutarse.")
                    TCPClientSocket.close()
                    break
                if dato.decode() == 'Fallo el servidor':
                    print("\n", dato.decode())
                    m = 1
                if dato.decode() == 'Servidor +1 punto':
                    print("\n", dato.decode())
                    TCPClientSocket.sendall(b'ok')
                    tabla = TCPClientSocket.recv(buffer_size)
                    respuesta = pickle.loads(tabla)
                    table_ava(respuesta)
    #TCPClientSocket.close()