# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.politician import Politician  # noqa
from app.models.bill import Bill  # noqa
from app.models.vote import Vote  # noqa
from app.models.political_contribution import PoliticalContribution  # noqa
