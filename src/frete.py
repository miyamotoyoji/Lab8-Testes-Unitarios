"""Cálculo mínimo de frete conforme specs/checkout_frete.md."""


def calcular_frete(subtotal: float, regiao: str | None = None) -> float:
    """REQ-01 e REQ-02: tarifa padrão com isenção por subtotal."""
    base = 0.00 if subtotal >= 250.00 else 15.00
    if regiao in ("Norte", "Nordeste") and subtotal <= 300.00:
        return base + 10.00
    return base


def calcular_total(subtotal: float, regiao: str | None = None) -> float:
    """REQ-01: total é a soma do subtotal com o frete aplicável."""
    return subtotal + calcular_frete(subtotal, regiao)
