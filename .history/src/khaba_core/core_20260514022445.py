import logging
import os
from dataclasses import asdict
from typing import Any, Dict, List, Optional
from collections.abc import Mapping

from khaba_core.layers import Ego, MaestroInterior, Subconsciente
from khaba_core.models import CognitiveProfile, Conflict, DecisionContext, FinalDecision, TraceEvent


class ConflictDetector:
    """Servicio de dominio que identifica tensions entre capas."""

    def __init__(
        self,
        conflict_threshold: float = 0.7,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.conflict_threshold = conflict_threshold
        self.logger = logger or logging.getLogger("khaba_core.conflict_detector")

    def detect(self, ego_output, subconscious_output) -> List[Conflict]:
        conflicts: List[Conflict] = []

        if ego_output.urgency >= self.conflict_threshold and subconscious_output.bias in {
            "caution",
            "integrity",
        }:
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
                    name="protection_vs_confianza",
                    layers=("ego", "subconsciente"),
                    description="El ego percibe amenaza mientras la memoria reconoce oportunidad.",
                    severity=0.65,
                )
            )

        self.logger.debug(
            "ConflictDetector.detect ego=%s subconsciente=%s conflicts=%s",
            ego_output,
            subconscious_output,
            conflicts,
        )
        return conflicts


class KhabaCore:
    """Orquestador del flujo: ego -> subconsciente -> maestro interior -> decision final."""

    def __init__(
        self,
        ego: Optional[Ego] = None,
        subconsciente: Optional[Subconsciente] = None,
        maestro: Optional[MaestroInterior] = None,
        conflict_detector: Optional[ConflictDetector] = None,
        profile: Optional[CognitiveProfile] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or logging.getLogger("khaba_core")
        self.profile = profile or CognitiveProfile.default()
        self.ego = ego or Ego(self.profile.signals, self.logger.getChild("ego"))
        self.subconsciente = subconsciente or Subconsciente(
            patterns=self.profile.memory_patterns,
            logger=self.logger.getChild("subconsciente"),
        )
        self.maestro = maestro or MaestroInterior(
            truth_risk_words=self.profile.signals.truth_risk_words,
            logger=self.logger.getChild("maestro_interior"),
        )
        self.conflict_detector = conflict_detector or ConflictDetector(
            conflict_threshold=self.profile.conflict_threshold,
            logger=self.logger.getChild("conflict_detector"),
        )

    def process(
        self,
        situation: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> FinalDecision:
        context = DecisionContext.from_situation(situation, metadata)
        execution_log: List[TraceEvent] = []

        self._record(execution_log, "input", "khaba_core", "Situacion recibida.", {"metadata": dict(context.metadata)})  # noqa: E501
        self.logger.info("KhabaCore input=%r", context.situation)

        ego_output = self.ego.response(context)
        self._record(
            execution_log,
            "ego.response",
            "ego",
            "Respuesta reactiva calculada.",
            {
                "recommendation": ego_output.recommendation,
                "influence": dict(ego_output.influence),
            },
        )
        self.logger.info("Capa ego completada: %s", ego_output.recommendation)

        subconscious_output = self.subconsciente.evaluate(context, ego_output)
        self._record(
            execution_log,
            "subconsciente.evaluate",
            "subconsciente",
            "Patrons de memoria evaluados.",
            {
                "bias": subconscious_output.bias,
                "matched_patterns": list(subconscious_output.matched_patterns),
                "modulation": subconscious_output.modulation,
            },
        )
        self.logger.info("Capa subconsciente completada: %s", subconscious_output.modulation)

        conflicts = self.conflict_detector.detect(ego_output, subconscious_output)
        self._record(
            execution_log,
            "conflicts.detect",
            "khaba_core",
            "Conflicts entre capas detectados.",
            {"conflicts": [asdict(conflict) for conflict in conflicts]},
        )
        self.logger.info("Conflicts detectados: %s", len(conflicts))

        decision = self.maestro.decide(
            situation=context,
            ego_output=ego_output,
            subconscious_output=subconscious_output,
            conflicts=conflicts,
        )
        self._record(
            execution_log,
            "maestro_interior.decide",
            "maestro_interior",
            "Decision final emitida con autoridad del maestro interior.",
            {
                "final_action": decision.final_action,
                "confidence": decision.confidence,
                "authority": decision.authority,
            },
        )
        decision.trace["context"] = context
        decision.trace["execution_log"] = execution_log
        self.logger.info("Decision final: %s", decision.final_action)
        return decision

    def _record(
        self,
        execution_log: List[TraceEvent],
        step: str,
        layer: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        event = TraceEvent(step=step, layer=layer, message=message, data=data or {})
        execution_log.append(event)
        self.logger.debug("TraceEvent %s", event)


def configure_logging() -> None:
    level_name = os.getenv("KHABA_CORE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
