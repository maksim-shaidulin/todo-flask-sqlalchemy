from .models import db


def get_all(model, order=None):
    if order is not None:
        data = model.query.order_by(order)
    else:
        data = model.query.all()
    return data


def get_instance(model, id):
    instance = model.query.filter_by(id=id).first()
    return instance


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    count = model.query.filter_by(id=id).delete()
    commit_changes()
    return count


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).first()
    if instance:
        for attr, new_value in kwargs.items():
            setattr(instance, attr, new_value)
        commit_changes()
        return 1
    return 0


def commit_changes():
    db.session.commit()
