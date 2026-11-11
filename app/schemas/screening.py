from marshmallow import Schema, fields


class ScreeningQuerySchema(Schema):
    date = fields.Date(required=False)
    film_id = fields.Int(required=False)
    