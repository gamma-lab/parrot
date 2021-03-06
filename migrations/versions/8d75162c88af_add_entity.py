"""add entity

Revision ID: 8d75162c88af
Revises: 443a46113be3
Create Date: 2019-03-07 10:46:32.639456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d75162c88af'
down_revision = '443a46113be3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_name', sa.String(length=64), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entities_id'), 'entities', ['id'], unique=False)
    op.create_table('user_says_examples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('intent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intent_id'], ['intents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_says_examples_id'), 'user_says_examples', ['id'], unique=False)
    op.create_table('user_says_examples_entities_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('start_index', sa.Integer(), nullable=True),
    sa.Column('end_index', sa.Integer(), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.Column('user_says_example_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.ForeignKeyConstraint(['user_says_example_id'], ['user_says_examples.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_says_examples_entities_association_id'), 'user_says_examples_entities_association', ['id'], unique=False)
    with op.batch_alter_table('intents') as batch_op:
        batch_op.drop_column('user_says')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('intents', sa.Column('user_says', sa.TEXT(), nullable=True))
    op.drop_index(op.f('ix_user_says_examples_entities_association_id'), table_name='user_says_examples_entities_association')
    op.drop_table('user_says_examples_entities_association')
    op.drop_index(op.f('ix_user_says_examples_id'), table_name='user_says_examples')
    op.drop_table('user_says_examples')
    op.drop_index(op.f('ix_entities_id'), table_name='entities')
    op.drop_table('entities')
    # ### end Alembic commands ###
