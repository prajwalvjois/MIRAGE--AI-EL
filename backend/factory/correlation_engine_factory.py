from backend.core.interfaces.icorrelation_engine import ICorrelationEngine
from backend.services.correlation.weighted_correlation_engine import WeightedCorrelationEngine

class CorrelationEngineFactory:
    @staticmethod
    def get_correlation_engine(engine_type: str = "weighted") -> ICorrelationEngine:
        if engine_type == "weighted":
            return WeightedCorrelationEngine()
        raise ValueError(f"Unknown correlation engine type: '{engine_type}'")
