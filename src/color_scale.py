"""Escala de color para coropléticos estáticos (personas exactas, INE)."""


def population_intensity(pop: int, pop_max: int) -> float:
    """Intensidad 0-1 relativa al máximo regional del año en personas.

    Reemplaza el antiguo ``pop / 3000`` calibrado para miles: con personas
    exactas la rampa se normaliza contra el máximo real del año para que el
    degradado use todo el rango (sin saturación mágica).
    """
    if pop <= 0 or pop_max <= 0:
        return 0.0
    return min(pop / pop_max, 1.0)
