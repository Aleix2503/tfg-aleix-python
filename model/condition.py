class Condition:
    def to_dict(self):
        raise NotImplementedError


class GenericCondition(Condition):
    """
    Condición simple.
    Ejemplos:
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
    Condición lógica.
    Puede contener condiciones simples u otras condiciones lógicas.
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
    """Reconstruye una condición desde su representación en diccionario"""
    if not data:
        return None
    
    condition_type = data.get("type")
    
    # Si tiene 'conditions', es una condición lógica
    if "conditions" in data:
        logical_cond = LogicalCondition(condition_type, [])
        for child_data in data.get("conditions", []):
            child_cond = condition_from_dict(child_data)
            if child_cond:
                logical_cond.conditions.append(child_cond)
        return logical_cond
    
    # Si tiene 'params', es una condición genérica
    elif "params" in data:
        return GenericCondition(condition_type, data.get("params", {}))
    
    return None