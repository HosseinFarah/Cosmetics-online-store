"""subcategories3rd

Revision ID: 3432479b125c
Revises: 3da23f76a62e
Create Date: 2024-11-14 17:24:05.586045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3432479b125c'
down_revision = '3da23f76a62e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('third_subcategory_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categories', ['third_subcategory_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('third_subcategory_id')

    # ### end Alembic commands ###