class Condition:
    def to_dict(self):
        raise NotImplementedError


class GenericCondition(Condition):
    """
    Simple condition.
    Examples:
    - HasTarget
    - TargetInRange
    - HealthBelow
    - VariableCompare
    """
    def __init__(self, condition_type, params=None):
        self.type = condition_type
        self.params = params or {}

    def to_dict(self):
        return {
            "type": self.type,
            "params": self.params
        }


class LogicalCondition(Condition):
    """
    Logical condition.
    Can contain simple conditions or other logical conditions.
    """
    def __init__(self, op, conditions=None):
        self.type = op  # AND / OR / NOT
        self.conditions = conditions or []

    def to_dict(self):
        return {
            "type": self.type,
            "conditions": [c.to_dict() for c in self.conditions]
        }


def condition_from_dict(data):
    """Reconstructs a condition from its dictionary representation"""
    if not data:
        return None

    condition_type = data.get("type")

    # If it has 'conditions', it is a logical condition
    if "conditions" in data:
        logical_cond = LogicalCondition(condition_type, [])
        for child_data in data.get("conditions", []):
            child_cond = condition_from_dict(child_data)
            if child_cond:
                logical_cond.conditions.append(child_cond)
        return logical_cond
    
    # If it has 'params', it is a generic condition
    elif "params" in data:
        return GenericCondition(condition_type, data.get("params", {}))
    
    return None