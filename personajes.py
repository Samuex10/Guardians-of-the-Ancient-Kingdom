"""Clases del sistema de combate Guardians of the Ancient Kingdom."""

from abc import ABC, abstractmethod
from math import floor


class Personaje(ABC):
    """Clase base abstracta para todos los guardianes."""

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.__nombre = valor.strip()

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La vida debe ser un número entero.")
        if not 0 <= valor <= 100:
            raise ValueError("La vida debe estar entre 0 y 100.")
        self.__vida = valor

    @property
    def ataque(self):
        return self.__ataque

    @ataque.setter
    def ataque(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El ataque debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El ataque debe ser un entero positivo.")
        self.__ataque = valor

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La defensa debe ser un número entero.")
        if valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self.__defensa = valor

    def recibir_danio(self, cantidad: int) -> int:
        """Resta el daño calculado y devuelve cuánto daño se aplicó realmente."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise TypeError("La cantidad de daño debe ser un entero.")
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        efectivo = min(cantidad, self.vida)
        self.__vida -= efectivo
        return efectivo

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def mostrar_estado(self) -> str:
        return (
            f"{self.nombre} | Vida: {self.vida} | "
            f"Ataque: {self.ataque} | Defensa: {self.defensa}"
        )

    def _validar_ataque(self, objetivo):
        if not self.esta_vivo():
            raise ValueError(f"{self.nombre} está derrotado y no puede atacar.")
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un personaje válido.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo) -> int:
        """Ataca al objetivo y devuelve el daño efectivamente recibido."""
        raise NotImplementedError


class Guerrero(Personaje):
    """Guerrero: potencia su ataque un 20 % y luego resta la defensa."""

    def atacar(self, objetivo) -> int:
        self._validar_ataque(objetivo)
        ataque_potenciado = floor(self.ataque * 1.20)
        danio = max(0, ataque_potenciado - objetivo.defensa)
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    """Mago: su hechizo ignora por completo la defensa del objetivo."""

    def atacar(self, objetivo) -> int:
        self._validar_ataque(objetivo)
        return objetivo.recibir_danio(self.ataque)


class Arquero(Personaje):
    """Arquero: duplica el daño base si su ataque supera la defensa rival."""

    def atacar(self, objetivo) -> int:
        self._validar_ataque(objetivo)
        if self.ataque > objetivo.defensa:
            danio = 2 * (self.ataque - objetivo.defensa)
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    """Administra los turnos de dos personajes creados independientemente."""

    MAX_RONDAS = 50

    def __init__(self, personaje1: Personaje, personaje2: Personaje):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise TypeError("Combate requiere dos objetos Personaje.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        self.participantes = [personaje1, personaje2]
        self.indice_turno = 0
        self.rondas = 0
        self.ganador = None
        self.empate = False
        self.terminado = False

    def cambiar_turno(self):
        """Alterna al siguiente participante."""
        self.indice_turno = 1 - self.indice_turno

    def verificar_ganador(self):
        """Devuelve el ganador si un participante cayó derrotado."""
        vivos = [p for p in self.participantes if p.esta_vivo()]
        if len(vivos) == 1:
            self.ganador = vivos[0]
            self.terminado = True
            return self.ganador
        if len(vivos) == 0:
            self.empate = True
            self.terminado = True
        return None

    def mostrar_resultado(self):
        if self.ganador:
            return f"Ganador: {self.ganador.nombre}"
        if self.empate:
            return "Empate."
        return "El combate todavía no ha terminado."

    def iniciar(self, mostrar: bool = True):
        """Ejecuta hasta 50 rondas; cada ronda permite atacar a ambos personajes."""
        if self.terminado:
            return self.mostrar_resultado()

        if mostrar:
            print("\n=== INICIO DEL COMBATE ===")
            for personaje in self.participantes:
                print(personaje.mostrar_estado())

        while not self.terminado and self.rondas < self.MAX_RONDAS:
            danio_ronda = 0
            for _ in range(2):
                atacante = self.participantes[self.indice_turno]
                objetivo = self.participantes[1 - self.indice_turno]

                if atacante.esta_vivo() and objetivo.esta_vivo():
                    danio = atacante.atacar(objetivo)
                    danio_ronda += danio
                    if mostrar:
                        print(
                            f"{atacante.nombre} ataca a {objetivo.nombre} "
                            f"y causa {danio} de daño."
                        )
                        for personaje in self.participantes:
                            print("  " + personaje.mostrar_estado())

                self.verificar_ganador()
                self.cambiar_turno()
                if self.terminado:
                    break

            self.rondas += 1
            if not self.terminado and danio_ronda == 0:
                self.empate = True
                self.terminado = True
                if mostrar:
                    print("Empate técnico: ambos personajes completaron la ronda sin daño.")

        if not self.terminado and self.rondas >= self.MAX_RONDAS:
            self.empate = True
            self.terminado = True
            if mostrar:
                print("Empate: se alcanzó el límite de 50 rondas.")

        if mostrar:
            print(self.mostrar_resultado())
        return self.mostrar_resultado()
