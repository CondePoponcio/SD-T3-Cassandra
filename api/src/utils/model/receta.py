import datetime as dt

from marshmallow import Schema, fields

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
