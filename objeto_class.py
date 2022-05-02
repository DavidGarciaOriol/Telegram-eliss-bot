class Objeto:

    def __init__(self, id_objeto, nombre:str, precio:int, descripcion:str):

        self.id_objeto = id_objeto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion

    def __str__(self):
        output = f"""
            \033[1m{self.nombre}\033[0m
            \033[1mPrecio: \033[0m{self.precio}\n
            \x1B[3m{self.descripcion}
        
        """
        return output

    