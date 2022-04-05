import pickle
import os
from Comic import Comic


def get_data_from_txt(file_name, data):
    """Función para obtener los datos serializados de un archivo txt.

    Args:
        file_name (str): nombre del archivo txt donde conseguir los datos.
        data (dict): datos a actualizar con los datos que se encuentran en el archivo.

    Returns:
        dict: datos obtenidos del archivo.
    """

    while True:

        try:

            read_binary = open(file_name, 'rb')
            # chequea si hay algún dato registrado que leer (es decir, si su 'size' es distinto a 0)
            if os.stat(file_name).st_size != 0:
                data = pickle.load(read_binary)
            read_binary.close()
            del read_binary
            return data

        # si el file no existe, se crea. y como se está en un loop, se vuelve nuevamente a intentar la operación de lectura.
        except FileNotFoundError:
            file = open(file_name, 'w')
            file.close()
            del file


def load_data_to_txt(file_name, data):
    """Función para cargar datos a un archivo txt mediante serialización.

    Args:
        file_name (str): nombre del archivo txt donde cargar los datos.
        data (dict): datos a cargar.
    """

    write_binary = open(file_name, 'wb')
    data = pickle.dump(data, write_binary)
    write_binary.close()
    del write_binary
    del data


# Funciones para organizar las estructuras de indexing por el método de merge sort
def merge_sort(array, left_index, right_index):
    if left_index >= right_index:
        return
    middle = (left_index + right_index) // 2
    merge_sort(array, left_index, middle)
    merge_sort(array, middle+1, right_index)
    merge(array, left_index, right_index, middle)


def merge(array, left_index, right_index, middle):
    left_copy = array[left_index:middle+1]
    right_copy = array[middle+1:right_index+1]
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left_index
    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if left_copy[left_copy_index][0] <= right_copy[right_copy_index][0]:
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
        sorted_index += 1

    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        left_copy_index += 1
        sorted_index += 1

    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        right_copy_index += 1
        sorted_index += 1


def register(comics, serial_indexing, title_indexing):
    """Función de registro de historietas.
    Se pide al usuario (y se validan) los datos necesarios de la historieta a registrar
    y luego se guarda al final de la lista de historietas pasada como parámetro.
    Se actualizan los índices correspondientes.

    Args:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título

    Returns:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título
    """
    os.system('clear')
    print("\n-----Registro------------------------------------------------------------\n")
    while True:

        print("\n-----SERIAL--------------------------------------------------------------")
        while True:
            try:
                serial = input(
                    "\nIntroduzca el serial de la historieta a registrar (8 dígitos numéricos. Debe ser único)\n> ")
                if len(serial) != 8:
                    raise Exception  # el serial debe tener 8 caracteres, si no no es válido
                # el serial debe ser un número entero, si hay una excepción al hacerse esta transformación, es un serial inválido
                int(serial)
                if int(serial) < 0:
                    raise Exception  # el serial no puede ser un número negativo
                if binary_search_by_serial(serial_indexing, serial) != None:
                    raise Exception  # el serial introducido no es único, ya existe una historieta con el mismo
                break  # si se llegó aquí sin excepciones, el serial introducido es válido y se sale del loop de validación
            except:
                # luego, como se está en un loop se vuelve a pedir el serial.
                print("Ingreso inválido. Intente otra vez.\n")

        print(
            "\n\n-----TÍTULO--------------------------------------------------------------")
        while True:
            title = input(
                "\nIntroduzca el título de la historieta a registrar (40 caracteres máximo)\n> ")
            if (len(title) == 0 or len(title) > 40 or title.isspace()):
                print("Ingreso inválido. Intente otra vez.\n")
                continue  # se vuelve a repetir el bucle de validación porque el título puede tener máximo 40 caracteres y no puede ser vacío
            break  # si el título es válido se sale del loop de validación

        print(
            "\n\n-----PRECIO DE VENTA-----------------------------------------------------")
        while True:
            try:
                price = int(input(
                    "\nIntroduzca el precio de venta de la historieta en dólares (número entero positivo de no más de 3 dígitos)\n> "))
                # el número debe ser mayor que 0 y de máximo tres dígitos
                if (price <= 0 or price >= 1000):
                    raise Exception
                break  # se sale del loop de validación si el precio es válido
            except:
                print("Ingreso inválido. Intente otra vez.\n")

        print(
            "\n\n-----STOCK ACTUAL--------------------------------------------------------")
        while True:
            try:
                stock = int(input(
                    "\nIntroduzca la cantidad de ejemplares disponibles en el inventario (número entero positivo de no más de 2 dígitos)\n>"))
                if (stock < 0 or stock >= 100):
                    raise Exception
                break
            except:
                print("Ingreso inválido. Intente otra vez.\n")

        # se crea un nuevo objeto Comic con los datos introducidos por el usuario
        newComic = Comic(serial, title, price, stock)
        # se agrega la nueva historieta al final de la lista comics de historietas registradas en el inventario
        comics.append(newComic)
        # como la nueva historieta se agrega al final de la lista comics, su RRN sería el largo de la lista - 1
        rrn = len(comics)-1

        # se agrega al final de serial_indexing el serial de la nueva historieta en conjunto con su relative record number
        serial_indexing.append([serial, rrn])
        # se ordena serial_indexing por el método de merge sort de menor a mayor por serial
        merge_sort(serial_indexing, 0, len(serial_indexing)-1)

        # title_words guarda una lista de cada palabra del título
        title_words = title.split(" ")
        for word in title_words:
            # se agrega al final de title_indexing una palabra del título a la vez, con el relative record number correspondiente a la nueva historieta
            title_indexing.append([word, rrn])
            # se ordena title_indexing por el método de merge sort de menor a mayor por palabra de título
            merge_sort(title_indexing, 0, len(title_indexing)-1)

        print("\n\n\nHISTORIETA REGISTRADA EXITOSAMENTE.\n")

        if (input("\nIngrese [s] si quiere seguir registrando historietas. Cualquier otro caracter para salir del registro.\n> ") != "s"):
            break

        os.system('clear')
    return (comics, serial_indexing, title_indexing)


def binary_search_by_serial(serial_indexing, serial):
    """Búsqueda binaria para conseguir el RRN de una historieta en la estructura de indexing pasada como parámetro.

    Args:
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        serial (str): serial de una historieta buscada por el usuario, cuyo RRN se retorna (si es conseguida)

    Returns:
        int: relative record number de la historieta cuyo serial se pasó como parámetro o None si no se consiguió
    """
    if len(serial_indexing) == 0:
        return None
    mid = len(serial_indexing) // 2
    if serial_indexing[mid][0] == serial:
        return serial_indexing[mid][1]
    elif serial < serial_indexing[mid][0]:
        return binary_search_by_serial(serial_indexing[0:mid], serial)
    else:
        return binary_search_by_serial(serial_indexing[mid+1:], serial)


def binary_search_by_word(title_indexing, word):
    """Función para buscar binariamente una(s) historieta(s) por una palabra de su(s) título(s)

    Args:
        title_indexing (list): lista de listas que representa la estructura de indexing por título
        word (str): palabra por la cual se busca una(s) historieta(s)

    Returns:
        list: lista con los relative record numbers de las historietas que tienen en su título la palabra pasada como parámetro, o None si no se consiguió ninguno
    """
    if len(title_indexing) == 0:
        return None
    mid = len(title_indexing) // 2
    if title_indexing[mid][0] == word:
        # se agrega a la lista de relative record numbers el rrn encontrado
        rrn_list = [title_indexing[mid][1]]

        index = mid-1
        while index >= 0:  # loop para revisar si antes del índice revisado hay otro elemento que coincida con lo buscado
            if title_indexing[index][0] == word:
                # se consiguió otro elemento que coincidía con la búsqueda, se agrega este nuevo rrn en la lista rrn_list
                rrn_list.append(title_indexing[index][1])
            else:  # si no se consigue otro elemento que coincida con lo buscado, se sale del loop
                break
            index = index - 1

        index = mid+1
        while index <= len(title_indexing)-1:
            if title_indexing[index][0] == word:
                # se consiguió otro elemento que coincidía con la búsqueda, se agrega este nuevo rrn en la lista rrn_list
                rrn_list.append(title_indexing[index][1])
            else:  # si no se consigue otro elemento que coincida con lo buscado, se sale del loop
                break
            index = index + 1

        # con esta operación se eliminan los duplicados de rrn (puede ocurrir que una historieta tenga un título que repite palabras y por tanto al buscar una de esas palabras devolvería más de una vez el mismo rrn)
        rrn_list = set(rrn_list)

        # se devuelve la lista con los relative record numbers conseguidos
        return list(rrn_list)

    elif word < title_indexing[mid][0]:
        return binary_search_by_word(title_indexing[0:mid], word)
    else:
        return binary_search_by_word(title_indexing[mid+1:], word)


def get_alive_comics(comics, rrn):
    """Función para agregar la información de los comics vivos cuyos rrn se guardan en la lista rrn
    a un string.

    Args:
        comics (list): lista que contiene objetos de clase Comic
        rrn (list): lista con los relative record numbers de historietas

    Returns:
        string: cadena que contiene la información de las historietas no eliminadas
    """

    alive_comics = ""
    for i in range(len(rrn)):
        if not comics[rrn[i]].get_dead():  # no se imprimen las eliminadas
            alive_comics += f"---{rrn[i]}----------"
            alive_comics += comics[rrn[i]].get_attributes()
            alive_comics += "\n"
    return alive_comics


def consult(comics, serial_indexing, title_indexing):
    """Función de consulta de historietas.
    Permite al usuario buscar (con índices) una historieta por serial o 1 - 2 palabras del título.
    Luego se le muestra la información de la historieta buscada (si es que se consigue).

    Args:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título
    """
    os.system('clear')
    print("\n-----Consulta------------------------------------------------------------\n")
    rrn = search_comic(serial_indexing, title_indexing)
    if rrn == None:
        print(
            "Lo introducido no corresponde a ninguna historieta guardada en el inventario.")
    elif type(rrn) == int:  # si se devolvió un int, entonces fue sólo una historieta buscada por serial
        if not comics[rrn].dead:
            print(f"\nCon la búsqueda se consiguió:\n{comics[rrn]}\n")
        else:
            print(
                "El serial introducido no corresponde a ninguna historieta guardada en el inventario.")
    # si no se devolvió None, ni un entero, se devolvió una lista con el/los rrn de la(s) historieta(s) buscadas por una o dos palabras del título
    else:
        alive_comics = get_alive_comics(comics, rrn)
        if alive_comics:
            print(f"\nCon la búsqueda se consiguió:\n")
            print(alive_comics)
        else:
            print(
                "Lo introducido no coincide con ninguna historieta guardada en el inventario.")

    input("\nPresione enter para volver al menú principal.\n▶️")


def search_comic(serial_indexing, title_indexing):
    while True:
        print("""\nINGRESE:
            \n\t(1) Para buscar una historieta por serial.
            \n\t(2) Para buscar una historieta por una o dos palabras de su título.""")
        user_input = input("> ")

        if user_input == "1":
            while True:
                try:
                    serial = input(
                        "\nIntroduzca el serial de la historieta a buscar.\n> ")
                    if len(serial) != 8:
                        raise Exception  # el serial debe tener 8 caracteres, si no no es válido
                    # el serial debe ser un número entero, si hay una excepción al hacerse esta transformación, es un serial inválido
                    int(serial)
                    if int(serial) < 0:
                        raise Exception  # el serial no puede ser un número negativo
                    # si se llegó aquí sin excepciones, el serial introducido es válido y se retorna lo que consiga la búsqueda binaria
                    return binary_search_by_serial(serial_indexing, serial)
                except:
                    print("\nIngreso inválido. Intente otra vez.\n")

        elif user_input == "2":
            while True:
                title = input(
                    "\nIntroduzca una o dos palabras del título de la historieta a buscar.\n> ")
                if (len(title) == 0 or len(title) > 40 or title.isspace() or len(title.split(" ")) > 2):
                    print("\nIngreso inválido. Intente otra vez.\n")
                    continue  # se vuelve a repetir el bucle de validación por ser un ingreso inválido
                break  # si lo introducido es válido se sale del loop de validación
            words = title.split(" ")
            rrn_lists = []
            for word in words:
                rrn = binary_search_by_word(title_indexing, word)
                if rrn:  # si lo que devolvió binary_search_by_word no es None se agrega la lista de relative record numbers en rrn_lists, de lo contrario se retorna None
                    rrn_lists.append(rrn)
                else:
                    return None
            if len(rrn_lists) == 1:
                return rrn_lists[0]
            else:
                rrn_set = set(rrn_lists[0])
                # se tiene la intersección entre las dos listas de relative record numbers en rrn_intersection
                rrn_intersection = list(rrn_set.intersection(rrn_lists[1]))
                if rrn_intersection:  # si la intersección no es vacía, se devuelve la intersección, de lo contrario se devuelve None
                    return rrn_intersection
                else:
                    return None
        else:
            print("\nIngreso inválido. Intente otra vez.\n")


def buy(comics, serial_indexing, title_indexing):
    """Función para comprar historietas.
    Se busca la historieta que quiera comprar el usuario, llamando a la función search_comic,
    y si hay suficiente stock permite al usuario comprar cuantas quiera. Finalmente se le
    muestra el precio total de su compra.

    Args:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título
    """
    os.system('clear')
    print("\n-----Compra------------------------------------------------------------\n")
    rrn = search_comic(serial_indexing, title_indexing)
    if rrn == None:
        print(
            "Lo introducido no corresponde a ninguna historieta guardada en el inventario.")
    elif type(rrn) == int:  # si se devolvió un int, entonces fue sólo una historieta buscada por serial
        if comics[rrn].dead:
            print(
                "Lo introducido no conrresponde a ninguna historieta guardada en el inventario.")
        else:
            if comics[rrn].stock > 0:
                print(f"\nCon la búsqueda se consiguió:\n{comics[rrn]}\n")
                # COMO SOLO ES UNA HISTORIETA, DE UNA VEZ SE LE LLEVA A LA COMPRA
                payment(comics, rrn)
            else:
                print(
                    "\nLa historieta buscada no tiene unidades disponibles para su venta.\n")

    # si no se devolvió None, ni un entero, se devolvió una lista con el/los rrn de la(s) historieta(s) buscadas por una o dos palabras del título
    else:
        # aquí guardaremos la información de los comics que están vivos y tienen algo en stock
        alive_comics = ""
        for i in range(len(rrn)):
            # no se añaden las eliminadas ni las de stock igual a cero
            if not comics[rrn[i]].get_dead() and comics[rrn[i]].stock > 0:
                alive_comics += f"---{rrn[i]}----------"
                alive_comics += comics[rrn[i]].get_attributes()
                alive_comics += "\n"

        if alive_comics:
            print(f"\nCon la búsqueda se consiguió:\n")
            print(alive_comics)

            while True:
                try:

                    user_select = int(
                        input("Ingrese el número correspondiente a la historieta que desea comprar\n> "))
                    # VALIDAR SI EL NUMERO INGRESADO ESTA EN EL ARRAY
                    if user_select not in rrn or comics[user_select].get_dead() or comics[user_select].stock == 0:
                        raise Exception

                    payment(comics, user_select)
                    break

                except:
                    print("\nIngreso inválido. Intente otra vez.\n")

        else:
            print(
                "Lo introducido no corresponde a ninguna historieta con unidades disponibles para vender.")

    input("\nPresione enter para volver al menú principal.\n▶️")


def payment(comics, index_comic):
    """
    Función para el pago. Preguntar la cantidad de historietas que se desean comprar,
    validar si excede la cantidad disponible: Si lo hace --> solicitar otra vez. Si no --> Mostrar precio y confirmar pago

    Args:
        comics (list): lista que contiene objetos de clase Comic
        index_comic (int): valor del indice de la historieta seleccionada por el usuario
    """
    price = comics[index_comic].price
    stock = comics[index_comic].stock

    # MOSTRAR PRECIO Y CONFIRMAR COMPRA
    while True:
        try:
            amount = int(
                input("\nIngrese la cantidad de historietas que desea adquirir\n> "))

            if amount <= 0 or amount > stock:
                raise Exception

            total_price = amount*price

            print("\nEl precio total a pagar es: ${}\n".format(total_price))

            while True:
                confirm = input(
                    "¿Desea realizar el pago? [s] = sí, [n] = no.\n>")

                if confirm.lower() == "s":
                    print("\n---------- PAGO REALIZADO CON ÉXITO ------------\n")
                    # se actualiza la cantidad en stock
                    comics[index_comic].stock = stock - amount
                    break
                elif confirm.lower() == "n":
                    print("\nLa compra fue cancelada.\n")
                    break
                else:
                    print("\nIngreso inválido. Intente otra vez.\n")
                    continue
            break

        except:
            print("\nIngreso inválido: debe ingresar un número de historietas menor o igual a la cantidad en stock (y mayor a cero). Intente otra vez.\n")


def restock(comics, serial_indexing, title_indexing):
    """Función para reabastecer historietas.
    Se busca con search_comic una historieta que el usuario quiera reabastecer.
    El usuario ingresa la cantidad de historietas que se agregan a la cantidad existente
    de la historieta (y se valida que la cantidad total sea válida).

    Args:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título
    """
    os.system('clear')
    print("\n-----Reabastecimiento------------------------------------------------------------\n")

    rrn = search_comic(serial_indexing, title_indexing)
    if rrn == None:
        print(
            "Lo introducido no corresponde a ninguna historieta guardada en el inventario.")
    elif type(rrn) == int:  # si se devolvió un int, entonces fue sólo una historieta buscada por serial
        if comics[rrn].dead:
            print(
                "Lo introducido no conrresponde a ninguna historieta guardada en el inventario.")
        else:
            print(f"\nCon la búsqueda se consiguió:\n{comics[rrn]}\n")
            # COMO SOLO ES UNA HISTORIETA, DE UNA VEZ SE LE LLEVA AL RESTOCK
            validate_restock(comics, rrn)

    # si no se devolvió None, ni un entero, se devolvió una lista con el/los rrn de la(s) historieta(s) buscadas por una o dos palabras del título
    else:
        alive_comics = get_alive_comics(comics, rrn)

        if alive_comics:
            print("\nCon la búsqueda se consiguió:\n")
            print(alive_comics)

            while True:
                try:
                    user_select = int(input(
                        "Ingrese el número correspondiente a la historieta que desea reabastecer\n> "))
                    # VALIDAR SI EL NUMERO INGRESADO ESTA EN EL ARRAY
                    if user_select not in rrn or comics[user_select].get_dead():
                        raise Exception

                    validate_restock(comics, user_select)
                    break
                except:
                    print("\nIngreso inválido. Intente otra vez.\n")
        else:
            print(
                "Lo introducido no corresponde a ninguna historieta guardada en el inventario.")

    input("\nPresione enter para volver al menú principal.\n▶️")


def validate_restock(comics, rrn):
    """
    Función para el reabastecimiento de historietas. Preguntar la cantidad de historietas que se desean aumentar al stock,
    validar si excede el límite de stock: Si lo hace --> solicitar otra vez. Sino --> Mostrar cambio y confirmar

    Args:
        comics (list): lista que contiene objetos de clase Comic
        rrn (int): valor del rrn de la historieta seleccionada por el usuario
    """
    if comics[rrn].stock == 99:
        print("La historieta escogida ya tiene el número máximo de copias en stock que es posible.")
    else:
        while True:
            try:
                amount = int(
                    input("Ingrese la cantidad de historietas que desea añadir\n> "))

                new_stock = comics[rrn].stock + amount

                if amount <= 0 or new_stock > 99:
                    raise Exception

                comics[rrn].stock = new_stock
                print("\n¡Se reabasteció la historieta correctamente!\n")
                break

            except:
                print("\nIngreso inválido. Intente otra vez.\n")


def delete(comics, serial_indexing, title_indexing):
    """Función para eliminar (lógicamente) historietas del inventario.
    Se busca con search_comic una historieta que el usuario quiera eliminar del inventario.
    Se elimina lógicamente la historieta que quiere el usuario.

    Args:
        comics (list): lista que contiene objetos de clase Comic
        serial_indexing (list): lista de listas que representa la estructura de indexing por serial
        title_indexing (list): lista de listas que representa la estructura de indexing por título
    """

    os.system('clear')
    print("\n-----Eliminación------------------------------------------------------------\n")
    rrn = search_comic(serial_indexing, title_indexing)
    if rrn == None:
        print("El serial o nombre introducido no corresponde a ninguna historieta guardada en el inventario.")

    elif type(rrn) == int:  # si se devolvió un int, entonces fue sólo una historieta buscada por serial
        if not comics[rrn].get_dead():
            # Se comprueba que quiera eliminar esa historieta, evitando errores
            print(f"\n¿Desea eliminar?:\n{comics[rrn]}\n")
            while True:
                confirmation = input(
                    "Presione [s] si desea continuar o [n] si no desea eliminarla\n> ")  # Confirmación
                if confirmation.lower() == "s":
                    # el atributo "dead" cambia a True, eliminándolo lógicamente
                    comics[rrn].set_dead()
                    print("\nHistorieta eliminada exitosamente!\n")
                elif confirmation.lower() == "n":
                    # no ocurre nada
                    print("\nLa historieta no ha sido modificada.\n")
                else:
                    # Validación de input
                    print("\nIngreso inválido. Intente otra vez.\n")
                    continue
                break
        else:
            print(
                "El serial introducido no corresponde a ninguna historieta guardada en el inventario.")  # Si una historieta existe pero está eliminada lógicamente, caemos en este condicional

    # si no se devolvió None, ni un entero, se devolvió una lista con el/los rrn de la(s) historieta(s) buscadas por una o dos palabras del título
    else:
        alive_comics = get_alive_comics(comics, rrn)

        if alive_comics:
            print(f"\nCon la búsqueda se consiguió:\n")
            print(alive_comics)

            while True:
                try:
                    # Se verifica el input y la historieta a eliminar
                    selection = int(
                        input("\nPor favor introduzca el número de la historieta a eliminar\n> "))
                    # El número ingresado no puede ser negativo ni cero, así como no puede ser mayor a la longitud de la lista
                    if selection not in rrn or comics[selection].get_dead():
                        # Si el usuario ingresa un valor inválido, se acaba el ciclo. Evitamos ingresar números negativos, cero, caracteres distintos de un dígitos, caracteres que no se encontraran en la lista rrn así como que el número ingresado ya esté muerto.
                        raise Exception
                    else:
                        print(f"\n¿Desea eliminar?:\n{comics[selection]}\n")
                        while True:
                            confirmation = input(
                                "\nPresione [s] si desea continuar o [n] si no desea eliminarla\n> ")
                            if (confirmation.lower() == "s"):
                                # Se settea dead como True
                                comics[selection].set_dead()
                                print("\n¡Historieta eliminada exitosamente!\n")
                            elif (confirmation.lower() == "n"):
                                print("\nLa historieta no ha sido modificada.\n")
                            else:
                                print(
                                    "\nIngreso inválido. Intente otra vez.\n")
                                continue
                            break
                    break
                except:
                    print("\nIngreso inválido.\n")
        else:
            print(
                "Lo introducido no corresponde a ninguna historieta guardada en el inventario.")

    input("\nPresione enter para volver al menú principal.\n▶️")


def pack(comics):
    """Función compactadora de las historietas del inventario.
    Se eliminan físicamente las historietas eliminadas lógicamente con anterioridad.
    Se actualizan los índices correspondientemente.

    Args:
        comics (list): lista que contiene objetos de clase Comic

    Return:

    """
    os.system('clear')
    print("\n-----Compactador------------------------------------------------------------\n")

    # Reiniciamos el resto de los valores
    new_comics = []
    new_serial_indexing = []
    new_title_indexing = []

    for comic in comics:
        if not comic.get_dead():  # no se agregan a la nueva lista de comics los eliminadas
            new_comics.append(comic)
            # como la historieta se agrega al final de la lista comics, su RRN sería el largo de la lista - 1
            rrn = len(new_comics)-1
            # se agrega al final de serial_indexing el serial de la nueva historieta en conjunto con su relative record number
            new_serial_indexing.append([comic.serial, rrn])
            # se ordena serial_indexing por el método de merge sort de menor a mayor por serial
            merge_sort(new_serial_indexing, 0, len(new_serial_indexing)-1)
            # title_words guarda una lista de cada palabra del título
            title_words = comic.title.split(" ")

            for word in title_words:
                # se agrega al final de title_indexing una palabra del título a la vez, con el relative record number correspondiente a la nueva historieta
                new_title_indexing.append([word, rrn])
                # se ordena title_indexing por el método de merge sort de menor a mayor por palabra de título
                merge_sort(new_title_indexing, 0, len(new_title_indexing)-1)

    print("La compactación fue exitosa.")
    input("\nPresione enter para volver al menú principal.\n▶️")

    return new_comics, new_serial_indexing, new_title_indexing
