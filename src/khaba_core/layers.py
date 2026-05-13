import logging
from typing import Dict, Iterable, List, Optional, Sequence

from khaba_core.models import Conflict, EgoOutput, FinalDecision, MemoryPattern, SubconsciousOutput

LOGGER = logging.getLogger(__name__)


def _keyword_hits(text: str, keywords: Iterable[str]) -> List[str]:
    return [keyword for keyword in keywords if keyword in text]


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


class Ego:
    """Capa reactiva: busca beneficio inmediato, proteccion e impulso."""

    BENEFIT_WORDS = ("ganar", "dinero", "oportunidad", "rapido", "beneficio", "cliente")
    RISK_WORDS = ("peligro", "amenaza", "perder", "rechazo", "urgente", "presion")
    IMPULSE_WORDS = ("ahora", "ya", "inmediato", "lanzar", "responder")

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or LOGGER.getChild("ego")

    def response(self, situation: str) -> EgoOutput:
        text = situation.lower()
        benefit_hits = _keyword_hits(text, self.BENEFIT_WORDS)
        risk_hits = _keyword_hits(text, self.RISK_WORDS)
        impulse_hits = _keyword_hits(text, self.IMPULSE_WORDS)

        perceived_benefit = _clamp(0.25 + 0.18 * len(benefit_hits))
        perceived_risk = _clamp(0.2 + 0.2 * len(risk_hits))
        urgency = _clamp(0.25 + 0.2 * len(impulse_hits) + 0.1 * len(risk_hits))

        if perceived_risk > perceived_benefit:
            recommendation = "protegerse y reducir exposicion inmediata"
            motives = ["proteccion", "control de dano", "evitar perdida"]
        elif perceived_benefit > 0.55 or urgency > 0.6:
            recommendation = "actuar rapido para capturar beneficio inmediato"
            motives = ["beneficio", "impulso", "aprovechar ventana"]
        else:
            recommendation = "responder rapido con una accion reversible"
            motives = ["respuesta inmediata", "bajo compromiso"]

        output = EgoOutput(
            layer="ego",
            recommendation=recommendation,
            urgency=urgency,
            perceived_benefit=perceived_benefit,
            perceived_risk=perceived_risk,
            motives=motives,
            influence={
                "beneficio": perceived_benefit,
                "proteccion": perceived_risk,
                "impulso": urgency,
            },
        )
        self.logger.debug("Ego.response input=%r output=%s", situation, output)
        return output


class Subconsciente:
    """Capa de memoria: detecta patrones previos y modula al ego."""

    DEFAULT_PATTERNS = (
        MemoryPattern(
            name="promesa bajo presion",
            markers=("prometer", "resultados", "urgente", "presion"),
            bias="caution",
            weight=0.85,
            lesson="Las promesas hechas bajo presion suelen romper coherencia futura.",
        ),
        MemoryPattern(
            name="oportunidad con cliente",
            markers=("cliente", "oferta", "venta", "dinero"),
            bias="confidence",
            weight=0.55,
            lesson="Las oportunidades comerciales funcionan mejor con alcance claro.",
        ),
        MemoryPattern(
            name="limite personal",
            markers=("agotado", "cansado", "limite", "ansiedad"),
            bias="boundary",
            weight=0.75,
            lesson="Ignorar limites internos produce decisiones reactivas.",
        ),
        MemoryPattern(
            name="riesgo de verdad",
            markers=("mentir", "ocultar", "manipular", "enganar", "no podemos demostrar"),
            bias="integrity",
            weight=0.95,
            lesson="La falta de verdad erosiona direccion y confianza.",
        ),
    )

    def __init__(
        self,
        patterns: Optional[Sequence[MemoryPattern]] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.patterns = list(patterns or self.DEFAULT_PATTERNS)
        self.logger = logger or LOGGER.getChild("subconsciente")

    def evaluate(self, situation: str, ego_output: EgoOutput) -> SubconsciousOutput:
        text = situation.lower()
        matches = [
            pattern
            for pattern in self.patterns
            if any(marker in text for marker in pattern.markers)
        ]

        bias_weights: Dict[str, float] = {}
        reasons: List[str] = []
        for pattern in matches:
            bias_weights[pattern.bias] = bias_weights.get(pattern.bias, 0.0) + pattern.weight
            reasons.append(f"{pattern.name}: {pattern.lesson}")

        if bias_weights:
            bias = max(bias_weights, key=bias_weights.get)
            confidence = _clamp(bias_weights[bias])
        else:
            bias = "neutral"
            confidence = 0.35
            reasons.append("No hay patrones fuertes; se mantiene observacion neutral.")

        modulation = self._modulation_for(bias, ego_output)
        output = SubconsciousOutput(
            layer="subconsciente",
            matched_patterns=[pattern.name for pattern in matches],
            bias=bias,
            confidence=confidence,
            modulation=modulation,
            reasons=reasons,
            influence={
                "memoria": confidence,
                "sesgo_caution": bias_weights.get("caution", 0.0),
                "sesgo_confidence": bias_weights.get("confidence", 0.0),
                "sesgo_integrity": bias_weights.get("integrity", 0.0),
                "sesgo_boundary": bias_weights.get("boundary", 0.0),
            },
        )
        self.logger.debug(
            "Subconsciente.evaluate input=%r ego=%s output=%s",
            situation,
            ego_output,
            output,
        )
        return output

    def _modulation_for(self, bias: str, ego_output: EgoOutput) -> str:
        if bias == "integrity":
            return "detener impulso y verificar verdad antes de actuar"
        if bias == "caution":
            return "bajar velocidad del ego y pedir evidencia"
        if bias == "boundary":
            return "reducir compromiso y proteger energia"
        if bias == "confidence" and ego_output.perceived_risk < 0.55:
            return "permitir avance acotado con limites claros"
        return "observar sin reforzar el impulso"


class MaestroInterior:
    """Capa de criterio: evalua coherencia, verdad y direccion."""

    TRUTH_RISK_WORDS = ("mentir", "ocultar", "manipular", "enganar", "no podemos demostrar")

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or LOGGER.getChild("maestro_interior")

    def decide(
        self,
        situation: str,
        ego_output: EgoOutput,
        subconscious_output: SubconsciousOutput,
        conflicts: Optional[Sequence[Conflict]] = None,
    ) -> FinalDecision:
        conflicts = list(conflicts or [])
        criteria = self._criteria_scores(situation, ego_output, subconscious_output, conflicts)

        if subconscious_output.bias == "integrity" or criteria["truth"] < 0.55:
            final_action = (
                "no prometer lo que no puede sostenerse; reformular una opcion "
                "transparente y verificable"
            )
        elif conflicts and max(conflict.severity for conflict in conflicts) >= 0.7:
            final_action = "pausar la reaccion, aclarar hechos y decidir con condiciones explicitas"
        elif criteria["direction"] >= 0.7 and ego_output.perceived_benefit > ego_output.perceived_risk:
            final_action = "avanzar de forma acotada, reversible y coherente con el proposito"
        else:
            final_action = "tomar distancia, recopilar informacion y posponer la accion irreversible"

        confidence = _clamp(sum(criteria.values()) / len(criteria) - 0.08 * len(conflicts))
        justification = [
            f"El ego propone: {ego_output.recommendation}.",
            f"El subconsciente modula: {subconscious_output.modulation}.",
            (
                "El maestro interior decide desde coherencia, verdad y direccion; "
                f"criterios={criteria}."
            ),
        ]
        if conflicts:
            justification.append(
                "Hay conflicto entre capas; la autoridad final no queda subordinada al impulso."
            )

        decision = FinalDecision(
            final_action=final_action,
            authority="maestro_interior",
            confidence=confidence,
            justification=justification,
            conflicts=conflicts,
            trace={
                "ego": ego_output,
                "subconsciente": subconscious_output,
                "maestro_interior": {
                    "criteria": criteria,
                    "selected_action": final_action,
                    "authority": "maestro_interior",
                },
            },
        )
        self.logger.debug(
            "MaestroInterior.decide input=%r ego=%s subconsciente=%s conflicts=%s output=%s",
            situation,
            ego_output,
            subconscious_output,
            conflicts,
            decision,
        )
        return decision

    def _criteria_scores(
        self,
        situation: str,
        ego_output: EgoOutput,
        subconscious_output: SubconsciousOutput,
        conflicts: Sequence[Conflict],
    ) -> Dict[str, float]:
        text = situation.lower()
        truth_risk = bool(_keyword_hits(text, self.TRUTH_RISK_WORDS))
        coherence = 0.8
        truth = 0.8
        direction = 0.75

        if truth_risk or subconscious_output.bias == "integrity":
            truth = 0.35
            coherence -= 0.2
        if ego_output.urgency > 0.75:
            coherence -= 0.1
        if conflicts:
            coherence -= 0.1 * len(conflicts)
            direction -= 0.05 * len(conflicts)
        if subconscious_output.bias == "confidence":
            direction += 0.08
        if subconscious_output.bias in {"caution", "boundary"}:
            direction -= 0.03

        return {
            "coherence": _clamp(coherence),
            "truth": _clamp(truth),
            "direction": _clamp(direction),
        }
