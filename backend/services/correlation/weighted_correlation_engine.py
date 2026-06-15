from typing import List, Optional
from datetime import datetime, timedelta, timezone
from backend.core.interfaces.icorrelation_engine import ICorrelationEngine
from backend.core.models.threat_event import ThreatEvent
from backend.core.models.correlation_result import CorrelationResult

class WeightedCorrelationEngine(ICorrelationEngine):
    def correlate(self, event: ThreatEvent, recent_events: List[ThreatEvent]) -> Optional[CorrelationResult]:
        # Exclude unknown brands
        if not event.brand or event.brand.lower() == "unknown":
            return None
        
        if event.risk_score < 0.40:
            return None

        # Filter eligible events
        eligible_events = []
        for recent_event in recent_events:
            # Avoid duplicating the current event if it's already in the recent_events list
            if recent_event.event_id == event.event_id:
                continue

            if not recent_event.brand or recent_event.brand.lower() == "unknown":
                continue
                
            if recent_event.risk_score < 0.40:
                continue
                
            if recent_event.brand != event.brand:
                continue
                
            # Time delta check - support naive or aware datetimes
            if event.timestamp.tzinfo is not None and recent_event.timestamp.tzinfo is None:
                # If event is aware and recent is naive, make recent aware
                event_time = event.timestamp
                recent_time = recent_event.timestamp.replace(tzinfo=timezone.utc)
            elif event.timestamp.tzinfo is None and recent_event.timestamp.tzinfo is not None:
                # If event is naive and recent is aware, make event aware
                event_time = event.timestamp.replace(tzinfo=timezone.utc)
                recent_time = recent_event.timestamp
            else:
                event_time = event.timestamp
                recent_time = recent_event.timestamp

            # calculate absolute difference
            # check if recent event is within 24 hours
            diff = abs(event_time - recent_time)
            if diff > timedelta(hours=24):
                continue
                
            eligible_events.append(recent_event)
            
        # Limit to 20 eligible recent events
        # Note: the input list is usually sorted by descending timestamp
        eligible_events = eligible_events[:20]
        
        if not eligible_events:
            return None
            
        # Campaign members includes the current event
        campaign_events = [event] + eligible_events
        event_count = len(campaign_events)
        
        # Calculate Campaign Risk
        avg_risk = sum(e.risk_score for e in campaign_events) / event_count
        
        size_bonus = 0.0
        if event_count == 2:
            size_bonus = 0.02
        elif event_count == 3:
            size_bonus = 0.04
        elif event_count == 4:
            size_bonus = 0.06
        elif event_count >= 5:
            size_bonus = 0.10
            
        campaign_risk = min(1.0, avg_risk + size_bonus)
        
        # Generate Reasons
        reasons = []
        if event_count > 1:
            reasons.append("Same Brand")
        if event_count >= 2:
            reasons.append("Multiple Related Events")
        if campaign_risk >= 0.75:
            reasons.append("High Risk Scores")
            
        return CorrelationResult(
            campaign_risk=round(campaign_risk, 4),
            campaign_brand=event.brand,
            event_count=event_count,
            reasons=reasons
        )
