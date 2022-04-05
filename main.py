import functions
import os


def main():
    """Función main para el programa de manejo de historietas.
    Contiene el menú principal para las distintas acciones que el usuario puede realizar.
    """
    comics = []
    # se leen los datos del disco duro
    comics = functions.get_data_from_txt("inventario.txt", comics)

    # será lista de listas (estas últimas listas tendrán como primer elemento el serial y el segundo elemento el RRN correspondiente)
    serial_indexing = []
    serial_indexing = functions.get_data_from_txt(
        "indice-serial.txt", serial_indexing)

    # será lista de listas (estas últimas listas tendrán como primer elemento el título y el segundo elemento el RRN correspondiente)
    title_indexing = []
    title_indexing = functions.get_data_from_txt(
        "indice-titulo.txt", title_indexing)

    os.system('clear')  # 'limpia' todo lo que hay en la terminal.
    print("\n¡Bienvenido a su inventario de historietas!")

    while True:
        print("\n-----Menú Principal---------------------------------------------")
        print("""\nINGRESE:
        \n\t(1) Para registrar una nueva historieta.
        \n\t(2) Para consultar una historieta.
        \n\t(3) Para comprar historietas.
        \n\t(4) Para reabastecer el inventario de historietas.
        \n\t(5) Para eliminar una historieta del inventario.
        \n\t(6) Para compactar el inventario.
        \n\t(7) Para salir.""")

        user_input = input("> ")
        if user_input == "1":
            (comics, serial_indexing, title_indexing) = functions.register(
                comics, serial_indexing, title_indexing)
        elif user_input == "2":
            functions.consult(comics, serial_indexing, title_indexing)
        elif user_input == "3":
            functions.buy(comics, serial_indexing, title_indexing)
        elif user_input == "4":
            functions.restock(comics, serial_indexing, title_indexing)
        elif user_input == "5":
            functions.delete(comics, serial_indexing, title_indexing)
        elif user_input == "6":
            (comics, serial_indexing, title_indexing) = functions.pack(
                comics)
        elif user_input == "7":
            # se guardan los datos en el disco duro
            functions.load_data_to_txt("inventario.txt", comics)
            functions.load_data_to_txt("indice-serial.txt", serial_indexing)
            functions.load_data_to_txt("indice-titulo.txt", title_indexing)

            print("\nLos datos han sido guardados.\n\nGracias por usar la aplicación.\n")
            break
        else:
            print("\nIngreso inválido. Intente otra vez.")
            input("\nPresione enter para seguir.\n▶️")

        os.system('clear')


if __name__ == '__main__':
    main()
