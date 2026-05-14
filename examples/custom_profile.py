import json

from khaba_core import CognitiveProfile, KhabaCore, KeywordSignalSet, MemoryPattern
from khaba_core.core import configure_logging


def main() -> None:
    configure_logging()
    profile = CognitiveProfile(
        signals=KeywordSignalSet(
            benefit_words=("inversion", "alianza", "crecimiento"),
            risk_words=("bloqueo", "dependencia", "desgaste"),
            impulse_words=("hoy", "cerrar", "ya"),
            truth_risk_words=("falso", "sin evidencia", "no validado"),
        ),
        memory_patterns=(
            MemoryPattern(
                name="fatiga ejecutiva",
                markers=("sobrecarga", "agotado", "desgaste"),
                bias="boundary",
                weight=0.9,
                lesson="La energia limitada exige reducir compromiso antes de decidir.",
            ),
            MemoryPattern(
                name="crecimiento sin evidencia",
                markers=("crecimiento", "sin evidencia", "no validado"),
                bias="integrity",
                weight=0.95,
                lesson="El crecimiento que no puede validarse rompe verdad y direccion.",
            ),
        ),
    )
    situation = (
        "El equipo quiere cerrar hoy una alianza de crecimiento, pero el impacto "
        "aun no esta validado y hay sobrecarga operativa."
    )

    core = KhabaCore(profile=profile)
    decision = core.process(situation, metadata={"domain": "estrategia"})
    print(json.dumps(decision.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
