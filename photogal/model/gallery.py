from photogal.database import db


class Gallery(db.Model):
    __tablename__ = "galleries"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String)
    description = db.Column(db.String)
    order_index = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    gallery_image_id = db.Column(db.Integer, db.ForeignKey("images.id"))

    # TODO: images collection

    def __repr__(self):
        return "<Gallery (id={}, name='{}')>".format(self.id, self.name)
