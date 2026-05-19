class Action:
    def __init__(self, name):
        self.name = name
        self.params = []  # Lista de {"key": "", "value": ""}

    def add_parameter(self, key, value):
        """Agregar un parámetro a la acción"""
        # Evitar duplicados
        for param in self.params:
            if param.get("key") == key:
                param["value"] = value
                return
        self.params.append({"key": key, "value": value})

    def get_parameter(self, key):
        """Obtener un parámetro específico"""
        for param in self.params:
            if param.get("key") == key:
                return param.get("value")
        return None

    def remove_parameter(self, key):
        """Eliminar un parámetro"""
        self.params = [p for p in self.params if p.get("key") != key]

    def to_dict(self):
        return {
            "action": self.name,
            "params": self.params
        }

    def __str__(self):
        params_str = ", ".join([f"{p.get('key')}={p.get('value')}" for p in self.params])
        return f"{self.name} [{params_str}]"
