"""Laboratório 8 / atividade 7.2: Dummy, Stub e Mock isolam serviços externos."""

from unittest.mock import create_autospec
import pytest
from logistica import ServicoLogisticaAPI, ServicoNotificacao, confirmar_frete


def test_confirmacao_com_dummy_stub_e_mock():
    # Arrange
    sessao_dummy = object()  # Preenche a assinatura; não fornece comportamento.
    pedido_id = "PED-008"
    logistica_stub = create_autospec(ServicoLogisticaAPI, instance=True, spec_set=True)
    logistica_stub.consultar_taxa.return_value = 23.50  # Resposta fixa, sem rede.
    notificacao_mock = create_autospec(ServicoNotificacao, instance=True, spec_set=True)
    eventos = []
    logistica_stub.consultar_taxa.side_effect = lambda pedido: eventos.append("taxa_confirmada") or 23.50
    notificacao_mock.enviar_notificacao_rastreio.side_effect = lambda pedido: eventos.append("notificado")

    # Act
    taxa_confirmada = confirmar_frete(pedido_id, sessao_dummy, logistica_stub, notificacao_mock)

    # Assert
    assert taxa_confirmada == 23.50
    logistica_stub.consultar_taxa.assert_called_once_with(pedido_id)
    notificacao_mock.enviar_notificacao_rastreio.assert_called_once_with(pedido_id)
    assert eventos == ["taxa_confirmada", "notificado"]


def test_nao_notifica_quando_consulta_falha():
    # Arrange
    logistica_stub = create_autospec(ServicoLogisticaAPI, instance=True, spec_set=True)
    logistica_stub.consultar_taxa.side_effect = TimeoutError("Serviço indisponível")
    notificacao_mock = create_autospec(ServicoNotificacao, instance=True, spec_set=True)

    # Act / Assert: uma consulta que falha não confirma frete nem dispara alerta.
    with pytest.raises(TimeoutError, match="Serviço indisponível"):
        confirmar_frete("PED-009", object(), logistica_stub, notificacao_mock)
    notificacao_mock.enviar_notificacao_rastreio.assert_not_called()
