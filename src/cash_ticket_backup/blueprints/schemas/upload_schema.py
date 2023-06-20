from marshmallow import fields, Schema, validates, ValidationError


class UploadSchema(Schema):
    xml_data = fields.String(required=True)
    filename = fields.String(required=True)
    client_name = fields.String(required=True)

    @validates('client_name')
    def validate_client_name(self, value):
        if not isinstance(value, str):
            raise ValidationError('The client name must be a string.')

        if len(value) < 3 or len(value) > 63:
            raise ValidationError('The client name must have a length between 3 and 63 characters.')

        if not value[0].isalnum():
            raise ValidationError('The client name must start with a letter or a digit.')

        if not all(c.islower() or c.isdigit() or c == '_' or c == '-' for c in value):
            raise ValidationError('The client name can only contain lowercase letters, digits, '
                                  'underscore (_) or hyphen (-).')
