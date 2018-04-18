from photogal.database import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    # TODO: "title"?
    name = db.Column(db.String)
    description = db.Column(db.String)
    # TODO: "path"? "filename"? "file"?
    location = db.Column(db.String)
    # TODO: not sure if we need width + height
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    creation_day = db.Column(db.Integer)
    creation_month = db.Column(db.Integer)
    creation_year = db.Column(db.Integer)

    # TODO galleries collection
    # TODO keywords collection

    def __repr__(self):
        return "<Image (id={}, name='{}')>".format(self.id, self.name)
