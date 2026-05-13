import json

from khaba_core import KhabaCore
from khaba_core.core import configure_logging


def main() -> None:
    configure_logging()
    situation = (
        "Mi socio quiere lanzar hoy una oferta a un cliente grande. "
        "Necesitamos dinero urgente, pero tendriamos que prometer resultados "
        "que aun no podemos demostrar."
    )

    core = KhabaCore()
    decision = core.process(situation)
    print(json.dumps(decision.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
