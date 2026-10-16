"""Laboratório 8 / atividade 7.4: fronteiras da regra regional por TDD."""

import pytest
from frete import calcular_frete, calcular_total


@pytest.mark.parametrize("regiao", ["Norte", "Nordeste"])
@pytest.mark.parametrize("subtotal,esperado", [(150, 25), (249.99, 25), (250, 10), (300, 10), (300.01, 0)])
def test_adicional_regional_e_excecao(subtotal, esperado, regiao):
    # Arrange
    valor_carrinho, destino = subtotal, regiao
    # Act
    resultado = calcular_frete(valor_carrinho, destino)
    # Assert
    assert resultado == esperado


@pytest.mark.parametrize("regiao", ["Sul", "Sudeste", "Centro-Oeste"])
@pytest.mark.parametrize("subtotal,esperado", [(249.99, 15), (250, 0), (300, 0)])
def test_outras_regioes_preservam_regra_base(subtotal, esperado, regiao):
    # Arrange
    valor_carrinho, destino = subtotal, regiao
    # Act
    resultado = calcular_frete(valor_carrinho, destino)
    # Assert
    assert resultado == esperado


@pytest.mark.parametrize("subtotal,esperado", [(150, 175), (250, 260), (300, 310), (300.01, 300.01)])
def test_total_inclui_frete_regional(subtotal, esperado):
    # Arrange
    destino = "Norte"
    # Act
    resultado = calcular_total(subtotal, destino)
    # Assert
    assert resultado == pytest.approx(esperado)
