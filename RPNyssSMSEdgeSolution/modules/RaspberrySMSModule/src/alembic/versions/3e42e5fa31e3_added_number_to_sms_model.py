"""Added Number to SMS Model

Revision ID: 3e42e5fa31e3
Revises: 
Create Date: 2019-12-01 19:25:30.374511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e42e5fa31e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sms', sa.Column('Number', sa.String))

def downgrade():
    op.remove_column('sms', 'Number')
