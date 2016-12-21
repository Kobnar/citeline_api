from stackcite import data as db


def create_user(email, password, groups=(), save=False):
    user = db.User()
    user.email = email
    user.set_password(password)
    for g in groups:
        user.add_group(g)
    if save:
        user.save()
    return user


def create_source(title, save=False):
    source = db.Source()
    source.title = title
    if save:
        source.save()
    return source


def create_citation(source, save=False):
    citation = db.Citation()
    citation.source = source
    if save:
        citation.save()
    return citation
