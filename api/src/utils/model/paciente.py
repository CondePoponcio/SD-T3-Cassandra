import datetime as dt

from marshmallow import Schema, fields, post_load


class Paciente(object):
    def __init__(self, id, comentario, doctor, farmacos, id_paciente):
        self.id = id
        self.comentario = comentario
        self.doctor = doctor
        self.farmacos = farmacos
        self.id_paciente = id_paciente

    def __repr__(self):
        return '<Paciente(name={self.id!r})>'.format(self=self)


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
