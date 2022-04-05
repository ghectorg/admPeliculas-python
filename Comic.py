class Comic():
    """Clase asociada a las historietas.
    """

    def __init__(self, serial, title, price, stock):
        self.serial = serial
        self.title = title
        self.price = price
        self.stock = stock
        self.dead = False

    def __str__(self):
        return f"\n\tSerial: {self.serial}\n\tTítulo: '{self.title}'\n\tPrecio: ${self.price}\n\tEn stock: {self.stock} copias\n"

    def get_attributes(self):
        return f"\n\tSerial: {self.serial}\n\tTítulo: '{self.title}'\n\tPrecio: ${self.price}\n\tEn stock: {self.stock} copias\n"

    def set_dead(self):
        self.dead = True

    def get_dead(self):
        return self.dead
