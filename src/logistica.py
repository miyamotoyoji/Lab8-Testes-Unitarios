"""Portas de serviços externos e confirmação de frete com injeção de dependências."""

from typing import Protocol


class ServicoLogisticaAPI(Protocol):
    def consultar_taxa(self, pedido_id: str) -> float: ...


class ServicoNotificacao(Protocol):
    def enviar_notificacao_rastreio(self, pedido_id: str) -> None: ...


def confirmar_frete(
    pedido_id: str,
    usuario_sessao: object,
    logistica: ServicoLogisticaAPI,
    notificacao: ServicoNotificacao,
) -> float:
    """Consulta a taxa e só depois notifica; sessão é reservada e não utilizada."""
    taxa = logistica.consultar_taxa(pedido_id)
    notificacao.enviar_notificacao_rastreio(pedido_id)
    return taxa
