import datetime as dt

from marshmallow import Schema, fields

class PacienteSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    rut = fields.Str()
    apellido = fields.Str()
    email = fields.Email()
    fecha_nacimiento = fields.Str()
    
    """
    @post_load
    def build_Paciente(self, data):
        return Paciente(**data)
    """
