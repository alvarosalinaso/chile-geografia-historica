"""Tests de la escala de color de coropléticos estáticos (personas exactas)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from color_scale import population_intensity


def test_zero_population_is_zero():
    assert population_intensity(0, 7112808) == 0.0
    assert population_intensity(-5, 7112808) == 0.0


def test_max_population_is_one():
    assert population_intensity(7112808, 7112808) == 1.0


def test_scales_linearly_with_data_range():
    assert population_intensity(500000, 1000000) == 0.5
    assert population_intensity(100000, 1000000) == 0.1


def test_values_above_max_saturate():
    assert population_intensity(8000000, 7112808) == 1.0


def test_official_2017_persons_not_saturated():
    # RM 2017 (máximo) = 1.0; Aysén 2017 (mínimo con población) queda en 0 < x < 1
    assert population_intensity(7112808, 7112808) == 1.0
    aysen = population_intensity(103158, 7112808)
    assert 0 < aysen < 0.1
