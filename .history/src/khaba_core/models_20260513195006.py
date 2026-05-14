from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(frozen=True)
class DecisionContext:
    """Entrada normalizada que todas las capas reciben como contrato comun."""

    situation: str
    normalized_text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_situation(
        cls,
        situation: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "DecisionContext":
        if not situation.strip():
            raise ValueError("KhabaCore.process requiere una situacion no vacia.")
        return cls(
            situation=situation,
            normalized_text=situation.lower(),
            metadata=dict(metadata or {}),
        )


@dataclass(frozen=True)
class KeywordSignalSet:
    benefit_words: Sequence[str]
    risk_words: Sequence[str]
    impulse_words: Sequence[str]
    truth_risk_words: Sequence[str]


@dataclass(frozen=True)
class TraceEvent:
    step: str
    layer: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EgoOutput:
    layer: str
    recommendation: str
    urgency: float
    perceived_benefit: float
    perceived_risk: float
    motives: List[str]
    influence: Dict[str, float]


@dataclass(frozen=True)
class MemoryPattern:
    name: str
    markers: Sequence[str]
    bias: str
    weight: float
    lesson: str


@dataclass(frozen=True)
class CognitiveProfile:
    """Configuration inyectable para adaptar el nucleo sin cambiar el codigo."""

    signals: KeywordSignalSet
    memory_patterns: Sequence[MemoryPattern]
    conflict_threshold: float = 0.7

    @classmethod
    def default(cls) -> "CognitiveProfile":
        return cls(
            signals=KeywordSignalSet(
                benefit_words=("ganar", "dinero", "oportunidad", "rapido", "beneficio", "client"),
                risk_words=("peligro", "amenaza", "perder", "rechazo", "urgente", "presion"),
                impulse_words=("ahora", "ya", "inmediato", "lanzar", "responder", "hoy"),
                truth_risk_words=(
                    "mentir",
                    "ocultar",
                    "manipular",
                    "enganar",
                    "no podemos demostrar",
                ),
            ),
            memory_patterns=(
                MemoryPattern(
                    name="promesa bajo presion",
                    markers=("prometer", "resultados", "urgente", "presion"),
                    bias="caution",
                    weight=0.85,
                    lesson="Las promesas hechas bajo presion suelen romper coherencia futura.",
                ),
                MemoryPattern(
                    name="oportunidad con client",
                    markers=("client", "oferta", "venta", "dinero"),
                    bias="confidence",
                    weight=0.55,
                    lesson="Las oportunidades comerciales funcionan mejor con alcance claro.",
                ),
                MemoryPattern(
                    name="limit personal",
                    markers=("agotado", "cansado", "limite", "ansiedad"),
                    bias="boundary",
                    weight=0.75,
                    lesson="Ignorar limites internos produce decisions reactivas.",
                ),
                MemoryPattern(
                    name="riesgo de verdad",
                    markers=("mentir", "ocultar", "manipular", "enganar", "no podemos demostrar"),
                    bias="integrity",
                    weight=0.95,
                    lesson="La falta de verdad erosiona direccion y confianza.",
                ),
            ),
        )


@dataclass(frozen=True)
class SubconsciousOutput:
    layer: str
    matched_patterns: List[str]
    bias: str
    confidence: float
    modulation: str
    reasons: List[str]
    influence: Dict[str, float]


@dataclass(frozen=True)
class Conflict:
    name: str
    layers: Sequence[str]
    description: str
    severity: float


@dataclass(frozen=True)
class FinalDecision:
    final_action: str
    authority: str
    confidence: float
    justification: List[str]
    conflicts: List[Conflict] = field(default_factory=list)
    trace: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
