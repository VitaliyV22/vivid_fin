from flask_migrate import Migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    from flask.cli import main
    main(as_module=True)
