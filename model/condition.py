class Condition:
    def to_dict(self):
        raise NotImplementedError


class VariableCondition(Condition):
    def __init__(self, name, operator, value):
        self.type = "VARIABLE"
        self.name = name
        self.operator = operator
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "operator": self.operator,
            "value": self.value
        }


class LogicalCondition(Condition):
    def __init__(self, op):
        self.type = op  # "AND", "OR", "NOT"
        self.conditions = []

    def to_dict(self):
        return {
            "type": self.type,
            "conditions": [c.to_dict() for c in self.conditions]
        }
    
class GenericCondition(Condition):
    def __init__(self, condition_type, params=None):
        self.type = condition_type
        self.params = params or {}

    def to_dict(self):
        return {
            "type": self.type,
            "params": self.params
        }

