class Nodo:
    def __init__(self, dado=0, proximo_nodo=None):
        self.dado = dado
        self.proximo = proximo_nodo

    def __repr__(self):
        return '%s -> %s' % (self.dado, self.proximo)


class Fila:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def __repr__(self):
        return "[" + str(self.primeiro) + "]"

    def insere(self, novo_dado):
        # Cria um novo nodo com o dado
        novo_nodo = Nodo(novo_dado)

        # Se a fila for vazia
        if self.primeiro is None:
            self.primeiro = novo_nodo
            self.ultimo = novo_nodo
        else:  # Se não for
            self.ultimo.proximo = novo_nodo
            self.ultimo = novo_nodo

    def remove(self):
        if self.primeiro is None:
            self.ultimo = None
        else:
            self.primeiro = self.primeiro.proximo

    def vazia(self):
        return self.primeiro is None
