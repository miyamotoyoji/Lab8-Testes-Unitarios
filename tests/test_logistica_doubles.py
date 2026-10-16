from unittest.mock import create_autospec

import pytest

from logistica import ServicoNotificacao, confirmar_frete


class SessaoDummy:

    pass


class ServicoLogisticaStub:

    def __init__(self, eventos):
        self.eventos = eventos

    def consultar_taxa(self, pedido_id):
        self.eventos.append("taxa_confirmada")
        return 23.50


class ServicoLogisticaComFalhaStub:

    def consultar_taxa(self, pedido_id):
        raise TimeoutError("Serviço indisponível")


def test_confirmacao_com_dummy_stub_e_mock():
    pedido_id = "PED-008"
    eventos = []

    sessao_dummy = SessaoDummy()

    logistica_stub = ServicoLogisticaStub(eventos)

    notificacao_mock = create_autospec(
        ServicoNotificacao, instance=True, spec_set=True
    )
    notificacao_mock.enviar_notificacao_rastreio.side_effect = (
        lambda pedido: eventos.append("notificado")
    )

    taxa_confirmada = confirmar_frete(
        pedido_id=pedido_id,
        usuario_sessao=sessao_dummy,
        logistica=logistica_stub,
        notificacao=notificacao_mock,
    )

    assert taxa_confirmada == 23.50

    notificacao_mock.enviar_notificacao_rastreio.assert_called_once_with("PED-008")

    assert eventos == ["taxa_confirmada", "notificado"]


def test_nao_notifica_quando_consulta_falha():
    sessao_dummy = SessaoDummy()
    logistica_stub = ServicoLogisticaComFalhaStub()
    notificacao_mock = create_autospec(
        ServicoNotificacao, instance=True, spec_set=True
    )

    with pytest.raises(TimeoutError, match="Serviço indisponível"):
        confirmar_frete(
            pedido_id="PED-009",
            usuario_sessao=sessao_dummy,
            logistica=logistica_stub,
            notificacao=notificacao_mock,
        )
    notificacao_mock.enviar_notificacao_rastreio.assert_not_called()
