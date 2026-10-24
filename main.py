"""Punto de entrada: demostraciones y pruebas manuales del proyecto."""

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def demostrar_habilidades():
    print("=== PRUEBA DE HABILIDADES ===")
    guerrero = Guerrero("Arthas", 100, 30, 20)
    rival = Mago("Rival", 80, 10, 10)
    danio = guerrero.atacar(rival)
    print(f"Guerrero: daño esperado 26, daño aplicado {danio}")

    mago = Mago("Gandalf", 80, 40, 10)
    rival2 = Guerrero("Defensor", 100, 10, 20)
    danio = mago.atacar(rival2)
    print(f"Mago: ignora defensa; daño esperado 40, daño aplicado {danio}")

    arquero = Arquero("Legolas", 90, 35, 10)
    rival3 = Guerrero("Objetivo", 100, 10, 15)
    danio = arquero.atacar(rival3)
    print(f"Arquero: daño esperado 40, daño aplicado {danio}")


def demostrar_validaciones():
    print("\\n=== PRUEBA DE VALIDACIONES ===")
    casos = [
        ("vida superior a 100", lambda: Guerrero("Inválido", 101, 10, 0)),
        ("vida negativa", lambda: Mago("Inválido", -1, 10, 0)),
        ("nombre vacío", lambda: Arquero("   ", 50, 10, 0)),
        ("ataque cero", lambda: Guerrero("Inválido", 50, 0, 0)),
        ("defensa negativa", lambda: Mago("Inválido", 50, 10, -1)),
    ]
    for nombre, crear in casos:
        try:
            crear()
        except (ValueError, TypeError) as error:
            print(f"Correcto: {nombre} rechazado ({error})")
        else:
            print(f"ERROR: {nombre} fue aceptado")


def demostrar_combate():
    print("\\n=== COMBATE COMPLETO ===")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    Combate(arthas, gandalf).iniciar()


# Pruebas compatibles con pytest: ejecutar con `pytest -q main.py`.
def test_creacion_de_personajes():
    assert Guerrero("A", 100, 10, 0).esta_vivo()
    assert Mago("B", 80, 20, 5).esta_vivo()
    assert Arquero("C", 60, 15, 3).esta_vivo()


def test_rechaza_valores_invalidos():
    import pytest
    with pytest.raises(ValueError):
        Guerrero("A", 101, 10, 0)
    with pytest.raises(ValueError):
        Mago("", 50, 10, 0)
    with pytest.raises(ValueError):
        Arquero("C", 50, 0, 0)
    with pytest.raises(ValueError):
        Guerrero("A", 50, 10, -1)


def test_habilidades_especiales():
    objetivo = Mago("Rival", 100, 10, 10)
    assert Guerrero("G", 100, 30, 0).atacar(objetivo) == 26

    objetivo = Guerrero("Rival", 100, 10, 20)
    assert Mago("M", 100, 40, 0).atacar(objetivo) == 40

    objetivo = Guerrero("Rival", 100, 10, 15)
    assert Arquero("A", 100, 35, 0).atacar(objetivo) == 40


def test_vida_no_es_negativa_y_daño_efectivo():
    objetivo = Mago("Rival", 10, 10, 0)
    assert Guerrero("G", 100, 30, 0).atacar(objetivo) == 10
    assert objetivo.vida == 0


def test_personaje_derrotado_no_ataca():
    import pytest
    derrotado = Guerrero("Caído", 0, 30, 0)
    objetivo = Mago("Rival", 50, 10, 0)
    with pytest.raises(ValueError):
        derrotado.atacar(objetivo)


def test_empate_tecnico_sin_danio():
    # Ambos ataques quedan bloqueados por la defensa; nadie recibe daño.
    a = Arquero("A", 50, 5, 5)
    b = Arquero("B", 50, 5, 5)
    combate = Combate(a, b)
    assert combate.iniciar(mostrar=False) == "Empate."
    assert combate.empate is True


def test_combate_identifica_ganador():
    a = Mago("Mago", 100, 50, 0)
    b = Guerrero("Guerrero", 10, 1, 0)
    combate = Combate(a, b)
    assert combate.iniciar(mostrar=False) == "Ganador: Mago"


if __name__ == "__main__":
    demostrar_habilidades()
    demostrar_validaciones()
    demostrar_combate()
