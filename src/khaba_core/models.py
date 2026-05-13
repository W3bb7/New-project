from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence


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
