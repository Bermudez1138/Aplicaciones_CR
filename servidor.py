import pickle
import socket
import random

#HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
#PORT = 9999  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
d1 = 'Principiante'
d2 = 'Avanzado'

tablero_n = ("       0      1      2      3 ")
tablero_nums = [[0, "-", "-", "-", "-"],
                [1, "-", "-", "-", "-"],
                [2, "-", "-", "-", "-"],
                [3, "-", "-", "-", "-"]]

listas = [["M", "M", "A", "A"],
          ["B", "B", "C", "C"],
          ["E", "E", "K", "K"],
          ["N", "N", "L", "L"]]

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

# función que imprime los resultados de ambos jugadores
def resultado(par1, par2):
    if par1 > par2:
        m=1
    elif par1 < par2:
        m=2
    else:
        m=3
    return m

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    # Servidor de conexión
    HOST = input("Introduzca la dirección IP para el servidor: ")
    # El puerto a utilizar (el servidor debe estar escuchando en este puerto)
    PORT = int(input("Introduzca el puerto de conexión: "))
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    Client_conn, Client_addr = TCPServerSocket.accept()

    with Client_conn:
        print("Conectado a", Client_addr)
        print("Esperando a recibir datos... ")

        data = Client_conn.recv(buffer_size)
        dec = data.decode()

        if dec == d1:
            Client_conn.sendall(pickle.dumps(tablero_nums))# tablero de 4x4
        if dec == d2:
            Client_conn.sendall(pickle.dumps(tablero_avan))#va el de 6x6

        if d1 == dec: #Principiante
            random.shuffle(listas)
            random.shuffle(listas[0])
            random.shuffle(listas[1])
            random.shuffle(listas[2])
            random.shuffle(listas[3])
            pairs_1 = 0
            pairs_2 = 0
            # varibles usadas para determinar si el juego concluye o no
            tabl_check = [[0], [1], [2], [3]]
            for a in listas[0]:
                tabl_check[0].append(a)
            for b in listas[1]:
                tabl_check[1].append(b)
            for c in listas[2]:
                tabl_check[2].append(c)
            for d in listas[3]:
                tabl_check[3].append(d)
            data = Client_conn.recv(buffer_size)
            player = data.decode()
            player = int(player)

            print(listas)

            # el ciclo infinito hasta que se determine un alto
            while True:
                # variables para comparar las elecciones hechas por los jugadores
                choice_1 = 0
                choice_2 = 0
                # checa el turno del jugador y lo imprime al usuario
                if player % 2 != 0: #Jugador
                    # si todos los números han sido adivinados, se imprimen los resultados y se acaba el código
                    if tabl_check == tablero_nums:
                        r = resultado(pairs_1, pairs_2)
                        Client_conn.sendall(str(r).encode())
                        print(r)
                        break

                    Client_conn.sendall(b"Turno del jugador")

                    prueba = Client_conn.recv(buffer_size)
                    if not prueba:
                        break
                    posi = prueba.decode()
                    print(posi)
                    pos_y_1 = int(posi[1])
                    pos_x_1 = int(posi[4])
                    pos_y_2 = int(posi[7])
                    pos_x_2 = int(posi[10])

                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_1 = listas[pos_y_1][pos_x_1]
                    tablero_nums[pos_y_1][pos_x_1 + 1] = choice_1
                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_2 = listas[pos_y_2][pos_x_2]
                    tablero_nums[pos_y_2][pos_x_2 + 1] = choice_2
                    # si los números no son iguales, cambiar el tablero a su valor inicial
                    if choice_1 != choice_2:
                        tablero_nums[pos_y_1][pos_x_1 + 1] = "-"
                        tablero_nums[pos_y_2][pos_x_2 + 1] = "-"
                        Client_conn.sendall(b"Fallaste")
                        player += 1
                    # si ambos números adivinados son iguales, se aumenta el valor de "pairs" al respectivo jugador
                    if choice_1 == choice_2:
                        pairs_1 += 1
                        Client_conn.sendall(b"Jugador +1 punto")
                        Client_conn.recv(buffer_size)
                        Client_conn.sendall(pickle.dumps(tablero_nums))

                #----------------------------------------------------
                if player % 2 == 0:
                    # si todos los números han sido adivinados, se imprimen los resultados y se acaba el código
                    if tabl_check == tablero_nums:
                        resultado(pairs_1, pairs_2)
                        r = resultado(pairs_1, pairs_2)
                        Client_conn.sendall(str(r).encode())
                        print(r)
                        break

                    Client_conn.sendall(b"Turno del servidor")
                    Client_conn.recv(buffer_size)

                    pos_y_1 = random.randint(0, 3)
                    pos_x_1 = random.randint(0, 3)

                    # checar si no han sido adivinados
                    while tablero_nums[pos_y_1][pos_x_1 + 1] != "-":
                        pos_y_1 = random.randint(0, 2)
                        pos_x_1 = random.randint(2, 3)

                    # igualar la primera elección al número de "listas"
                    choice_1 = listas[pos_y_1][pos_x_1]
                    tablero_nums[pos_y_1][pos_x_1 + 1] = choice_1

                    pos_y_2 = random.randint(0, 3)
                    pos_x_2 = random.randint(0, 3)

                    # checar si no han sido adivinados y si no son iguales a la elección anterior
                    while tablero_nums[pos_y_2][pos_x_2 + 1] != "-" or (pos_x_2 == pos_x_1 and pos_y_2 == pos_y_1):
                        if tablero_nums[pos_y_2][pos_x_2 + 1] != "-":
                            pos_y_2 = random.randint(2, 3)
                            pos_x_2 = random.randint(0, 1)
                        if pos_x_2 == pos_x_1 and pos_y_2 == pos_y_1:
                            pos_y_2 = random.randint(2, 3)
                            pos_x_2 = random.randint(0, 1)

                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_2 = listas[pos_y_2][pos_x_2]
                    tablero_nums[pos_y_2][pos_x_2 + 1] = choice_2

                    # si los números no son iguales, cambiar el tablero a su valor inicial
                    if choice_1 != choice_2:
                        tablero_nums[pos_y_1][pos_x_1 + 1] = "-"
                        tablero_nums[pos_y_2][pos_x_2 + 1] = "-"
                        Client_conn.sendall(b'Fallo el servidor')
                        player +=1
                    # si ambos números adivinados son iguales, se aumenta el valor de "pairs" al respectivo jugador
                    if choice_1 == choice_2:
                        pairs_2 += 1
                        Client_conn.sendall(b'Servidor +1 punto')
                        Client_conn.recv(buffer_size)
                        Client_conn.sendall(pickle.dumps(tablero_nums))

        if d2 == dec: #Avanzado
            random.shuffle(listasava)
            random.shuffle(listasava[0])
            random.shuffle(listasava[1])
            random.shuffle(listasava[2])
            random.shuffle(listasava[3])
            random.shuffle(listasava[4])
            random.shuffle(listasava[5])
            pairs_1 = 0
            pairs_2 = 0
            # varibles usadas para determinar si el juego concluye o no
            tabl_check = [[0], [1], [2], [3], [4], [5]]
            for a in listasava[0]:
                tabl_check[0].append(a)
            for b in listasava[1]:
                tabl_check[1].append(b)
            for c in listasava[2]:
                tabl_check[2].append(c)
            for d in listasava[3]:
                tabl_check[3].append(d)
            for e in listasava[4]:
                tabl_check[4].append(e)
            for f in listasava[5]:
                tabl_check[5].append(f)
            data = Client_conn.recv(buffer_size)
            player = data.decode()
            player = int(player)

            print(listasava)

            # el ciclo infinito hasta que se determine un alto
            while True:
                # variables para comparar las elecciones hechas por los jugadores
                choice_1 = 0
                choice_2 = 0
                # checa el turno del jugador y lo imprime al usuario
                if player % 2 != 0:  # Jugador
                    # si todos los números han sido adivinados, se imprimen los resultados y se acaba el código
                    if tabl_check == tablero_avan:
                        r = resultado(pairs_1, pairs_2)
                        Client_conn.sendall(str(r).encode())
                        print(r)
                        break

                    Client_conn.sendall(b"Turno del jugador")

                    prueba = Client_conn.recv(buffer_size)
                    if not prueba:
                        break
                    posi = prueba.decode()
                    print(posi)
                    pos_y_1 = int(posi[1])
                    pos_x_1 = int(posi[4])
                    pos_y_2 = int(posi[7])
                    pos_x_2 = int(posi[10])

                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_1 = listasava[pos_y_1][pos_x_1]
                    tablero_avan[pos_y_1][pos_x_1 + 1] = choice_1
                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_2 = listasava[pos_y_2][pos_x_2]
                    tablero_avan[pos_y_2][pos_x_2 + 1] = choice_2
                    # si los números no son iguales, cambiar el tablero a su valor inicial
                    if choice_1 != choice_2:
                        tablero_avan[pos_y_1][pos_x_1 + 1] = "-"
                        tablero_avan[pos_y_2][pos_x_2 + 1] = "-"
                        Client_conn.sendall(b"Fallaste")
                        player += 1
                    # si ambos números adivinados son iguales, se aumenta el valor de "pairs" al respectivo jugador
                    if choice_1 == choice_2:
                        pairs_1 += 1
                        Client_conn.sendall(b"Jugador +1 punto")
                        Client_conn.recv(buffer_size)
                        Client_conn.sendall(pickle.dumps(tablero_avan))

                # ----------------------------------------------------
                if player % 2 == 0:
                    # si todos los números han sido adivinados, se imprimen los resultados y se acaba el código
                    if tabl_check == tablero_avan:
                        resultado(pairs_1, pairs_2)
                        r = resultado(pairs_1, pairs_2)
                        Client_conn.sendall(str(r).encode())
                        print(r)
                        break
                    Client_conn.sendall(b"Turno del servidor")
                    Client_conn.recv(buffer_size)
                    pos_y_1 = random.randint(0, 5)
                    pos_x_1 = random.randint(0, 5)
                    # checar si no han sido adivinados
                    while tablero_avan[pos_y_1][pos_x_1 + 1] != "-":
                        pos_y_1 = random.randint(2, 5)
                        pos_x_1 = random.randint(0, 4)
                    # igualar la primera elección al número de "listas"
                    choice_1 = listasava[pos_y_1][pos_x_1]
                    tablero_avan[pos_y_1][pos_x_1 + 1] = choice_1
                    pos_y_2 = random.randint(0, 5)
                    pos_x_2 = random.randint(0, 5)
                    # checar si no han sido adivinados y si no son iguales a la elección anterior
                    while tablero_avan[pos_y_2][pos_x_2 + 1] != "-" or (pos_x_2 == pos_x_1 and pos_y_2 == pos_y_1):
                        if tablero_avan[pos_y_2][pos_x_2 + 1] != "-":
                            pos_y_2 = random.randint(0, 5)
                            pos_x_2 = random.randint(0, 5)
                        if pos_x_2 == pos_x_1 and pos_y_2 == pos_y_1:
                            pos_y_2 = random.randint(1, 4)
                            pos_x_2 = random.randint(0, 5)
                    # igualar la primera elección al número de "listas" y mostrar que número se eligió
                    choice_2 = listasava[pos_y_2][pos_x_2]
                    tablero_avan[pos_y_2][pos_x_2 + 1] = choice_2
                    # si los números no son iguales, cambiar el tablero a su valor inicial
                    if choice_1 != choice_2:
                        tablero_avan[pos_y_1][pos_x_1 + 1] = "-"
                        tablero_avan[pos_y_2][pos_x_2 + 1] = "-"
                        Client_conn.sendall(b'Fallo el servidor')
                        player += 1
                    # si ambos números adivinados son iguales, se aumenta el valor de "pairs" al respectivo jugador
                    if choice_1 == choice_2:
                        pairs_2 += 1
                        Client_conn.sendall(b'Servidor +1 punto')
                        Client_conn.recv(buffer_size)
                        Client_conn.sendall(pickle.dumps(tablero_avan))
