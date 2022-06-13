import datetime as dt

from marshmallow import Schema, fields, post_load


class Receta(object):
    def __init__(self, id, comentario, doctor, farmacos, id_paciente):
        self.id = id
        self.comentario = comentario
        self.doctor = doctor
        self.farmacos = farmacos
        self.id_paciente = id_paciente

    def __repr__(self):
        return '<Receta(name={self.id!r})>'.format(self=self)


class RecetaSchema(Schema):
    id = fields.UUID(required=True)
    comentario = fields.Str(required=True)
    doctor = fields.Str(required=True)
    farmacos = fields.Str(required=True)
    id_paciente = fields.UUID(required=True)
    
    """
    @post_load 
    def build_Receta(self, data, **kwargs):
        #print("build_Receta: ", data)
        return Receta(**data)
    """
