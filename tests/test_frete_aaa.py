"""Laboratório 8 / atividade 7.1 no Moodle: padrão Arrange, Act, Assert."""

import pytest
from frete import calcular_frete


@pytest.mark.parametrize("subtotal,esperado", [(150, 15), (249.99, 15), (250, 0), (300, 0)])
def test_frete_padrao_e_gratuidade_aaa(subtotal, esperado):
    # Arrange: prepara os dados de entrada e a expectativa independente.
    valor_carrinho = subtotal
    frete_esperado = esperado

    # Act: executa uma única ação da unidade sob teste.
    frete_calculado = calcular_frete(valor_carrinho)

    # Assert: verifica o resultado observado.
    assert frete_calculado == frete_esperado
