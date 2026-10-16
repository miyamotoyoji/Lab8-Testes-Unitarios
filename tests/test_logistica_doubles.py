from unittest.mock import Mock, call

import pytest

from logistica import ServicoNotificacao, confirmar_frete


def test_confirmacao_com_dummy_stub_e_mock():
    pedido_id = "PED-008"
    dummy_user = Mock()
    stub = Mock()
    stub.consultar_taxa.return_value = 23.50
    notificacao_mock = Mock(spec=ServicoNotificacao)
    chamadas = Mock()
    chamadas.attach_mock(stub, "logistica")
    chamadas.attach_mock(notificacao_mock, "notificacao")

    taxa_confirmada = confirmar_frete(
        pedido_id=pedido_id,
        usuario_sessao=dummy_user,
        logistica=stub,
        notificacao=notificacao_mock,
    )

    assert taxa_confirmada == 23.50
    assert dummy_user.mock_calls == []
    stub.consultar_taxa.assert_called_once_with(pedido_id)
    notificacao_mock.enviar_notificacao_rastreio.assert_called_once_with(pedido_id)
    assert chamadas.mock_calls == [
        call.logistica.consultar_taxa(pedido_id),
        call.notificacao.enviar_notificacao_rastreio(pedido_id),
    ]


def test_nao_notifica_quando_consulta_falha():
    dummy_user = Mock()
    stub = Mock()
    stub.consultar_taxa.side_effect = TimeoutError("Serviço indisponível")
    notificacao_mock = Mock(spec=ServicoNotificacao)

    with pytest.raises(TimeoutError, match="Serviço indisponível"):
        confirmar_frete(
            pedido_id="PED-009",
            usuario_sessao=dummy_user,
            logistica=stub,
            notificacao=notificacao_mock,
        )

    assert dummy_user.mock_calls == []
    notificacao_mock.enviar_notificacao_rastreio.assert_not_called()
