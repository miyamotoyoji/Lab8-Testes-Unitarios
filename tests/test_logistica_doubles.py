"""EXERCÍCIO 7.2 — TEST DOUBLES (seção 8 do Moodle).

DUMMY: SessaoDummy — preenche o parâmetro de sessão, sem participar da lógica.
STUB: ServicoLogisticaStub — devolve a taxa fixa de R$23,50, sem acessar rede.
MOCK: notificacao_mock — verifica chamada única e ID correto do pedido.

Os três são usados juntos no teste test_confirmacao_com_dummy_stub_e_mock.
"""

from unittest.mock import create_autospec

import pytest

from logistica import ServicoNotificacao, confirmar_frete


# 1. DUMMY: objeto fictício que apenas preenche a assinatura.
class SessaoDummy:
    """Sessão sem dados ou comportamento: a unidade testada não a utiliza."""

    pass


# 2. STUB: substitui o serviço externo por uma resposta previamente definida.
class ServicoLogisticaStub:
    """Substitui ServicoLogisticaAPI; não faz nenhuma chamada de rede.

    A lista de eventos é somente instrumentação para verificar a ordem.
    O papel de Stub vem da resposta fixa, independente do pedido recebido.
    """

    def __init__(self, eventos):
        self.eventos = eventos

    def consultar_taxa(self, pedido_id):
        self.eventos.append("taxa_confirmada")
        return 23.50


class ServicoLogisticaComFalhaStub:
    """Stub alternativo: simula indisponibilidade do serviço externo."""

    def consultar_taxa(self, pedido_id):
        raise TimeoutError("Serviço indisponível")


def test_confirmacao_com_dummy_stub_e_mock():
    # ARRANGE — prepara os três papéis de Test Double.
    pedido_id = "PED-008"
    eventos = []

    # DUMMY: é passado, mas não deve ser consultado pela lógica de frete.
    sessao_dummy = SessaoDummy()

    # STUB: fornece a taxa programada de R$23,50 no lugar da API real.
    logistica_stub = ServicoLogisticaStub(eventos)

    # 3. MOCK: substitui o serviço de notificação e registra suas chamadas.
    # autospec/spec_set restringem o objeto à interface real do serviço.
    notificacao_mock = create_autospec(
        ServicoNotificacao, instance=True, spec_set=True
    )
    notificacao_mock.enviar_notificacao_rastreio.side_effect = (
        lambda pedido: eventos.append("notificado")
    )

    # ACT — executa a unidade real com as dependências substituídas.
    taxa_confirmada = confirmar_frete(
        pedido_id=pedido_id,
        usuario_sessao=sessao_dummy,
        logistica=logistica_stub,
        notificacao=notificacao_mock,
    )

    # ASSERT — resultado fornecido pelo Stub.
    assert taxa_confirmada == 23.50

    # ASSERT — expectativa do Mock: exatamente UMA chamada com o ID correto.
    notificacao_mock.enviar_notificacao_rastreio.assert_called_once_with("PED-008")

    # ASSERT — a notificação ocorre somente após a confirmação da taxa.
    assert eventos == ["taxa_confirmada", "notificado"]


def test_nao_notifica_quando_consulta_falha():
    # ARRANGE — Dummy de sessão, Stub de falha e Mock de notificação.
    sessao_dummy = SessaoDummy()
    logistica_stub = ServicoLogisticaComFalhaStub()
    notificacao_mock = create_autospec(
        ServicoNotificacao, instance=True, spec_set=True
    )

    # ACT / ASSERT — falha na consulta impede confirmação e notificação.
    with pytest.raises(TimeoutError, match="Serviço indisponível"):
        confirmar_frete(
            pedido_id="PED-009",
            usuario_sessao=sessao_dummy,
            logistica=logistica_stub,
            notificacao=notificacao_mock,
        )
    notificacao_mock.enviar_notificacao_rastreio.assert_not_called()
