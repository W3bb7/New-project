import logging
import os
from typing import List, Optional

from khaba_core.layers import Ego, MaestroInterior, Subconsciente
from khaba_core.models import Conflict, FinalDecision


class KhabaCore:
    """Orquestador del flujo: ego -> subconsciente -> maestro interior -> decision final."""

    def __init__(
        self,
        ego: Optional[Ego] = None,
        subconsciente: Optional[Subconsciente] = None,
        maestro: Optional[MaestroInterior] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or logging.getLogger("khaba_core")
        self.ego = ego or Ego(self.logger.getChild("ego"))
        self.subconsciente = subconsciente or Subconsciente(logger=self.logger.getChild("subconsciente"))
        self.maestro = maestro or MaestroInterior(self.logger.getChild("maestro_interior"))

    def process(self, situation: str) -> FinalDecision:
        if not situation.strip():
            raise ValueError("KhabaCore.process requiere una situacion no vacia.")

        self.logger.info("KhabaCore input=%r", situation)
        ego_output = self.ego.response(situation)
        self.logger.info("Capa ego completada: %s", ego_output.recommendation)

        subconscious_output = self.subconsciente.evaluate(situation, ego_output)
        self.logger.info("Capa subconsciente completada: %s", subconscious_output.modulation)

        conflicts = self._detect_conflicts(ego_output, subconscious_output)
        self.logger.info("Conflictos detectados: %s", len(conflicts))

        decision = self.maestro.decide(
            situation=situation,
            ego_output=ego_output,
            subconscious_output=subconscious_output,
            conflicts=conflicts,
        )
        self.logger.info("Decision final: %s", decision.final_action)
        return decision

    def _detect_conflicts(self, ego_output, subconscious_output) -> List[Conflict]:
        conflicts: List[Conflict] = []

        if ego_output.urgency >= 0.7 and subconscious_output.bias in {"caution", "integrity"}:
            conflicts.append(
                Conflict(
                    name="impulso_vs_memoria",
                    layers=("ego", "subconsciente"),
                    description=(
                        "El ego empuja a actuar rapido, pero la memoria detecta riesgo aprendido."
                    ),
                    severity=max(ego_output.urgency, subconscious_output.confidence),
                )
            )

        if ego_output.perceived_benefit >= 0.4 and subconscious_output.bias == "integrity":
            conflicts.append(
                Conflict(
                    name="beneficio_vs_verdad",
                    layers=("ego", "subconsciente", "maestro_interior"),
                    description=(
                        "El beneficio inmediato compite con la exigencia de verdad verificable."
                    ),
                    severity=0.95,
                )
            )

        if ego_output.perceived_risk >= 0.65 and subconscious_output.bias == "confidence":
            conflicts.append(
                Conflict(
                    name="proteccion_vs_confianza",
                    layers=("ego", "subconsciente"),
                    description="El ego percibe amenaza mientras la memoria reconoce oportunidad.",
                    severity=0.65,
                )
            )

        self.logger.debug(
            "KhabaCore._detect_conflicts ego=%s subconsciente=%s conflicts=%s",
            ego_output,
            subconscious_output,
            conflicts,
        )
        return conflicts


def configure_logging() -> None:
    level_name = os.getenv("KHABA_CORE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
