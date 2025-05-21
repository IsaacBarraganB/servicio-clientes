from project.views.users import users

def add_routes(app):
    views = (
        users,
    )

    for view in views:
        view(app)