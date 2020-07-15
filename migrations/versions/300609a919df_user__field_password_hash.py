"""user__field_password_hash

Revision ID: 300609a919df
Revises: cc697cdbfe82
Create Date: 2020-07-15 19:53:46.869416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '300609a919df'
down_revision = 'cc697cdbfe82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=228), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###