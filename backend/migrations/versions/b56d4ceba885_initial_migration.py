"""Initial migration.

Revision ID: b56d4ceba885
Revises: 
Create Date: 2024-04-24 00:01:22.023179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56d4ceba885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('counterstrats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fact_combinations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facts', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('facts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('language', sa.Enum('ENG', 'EST', 'RUS', name='language_types'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('primary_narratives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fact_combination_id', sa.Integer(), nullable=False),
    sa.Column('narrative_text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('strat_id', sa.Integer(), nullable=False),
    sa.Column('news', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['fact_combination_id'], ['fact_combinations.id'], ),
    sa.ForeignKeyConstraint(['strat_id'], ['strats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strategy_effectiveness',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strategy_id', sa.Integer(), nullable=False),
    sa.Column('counter_strategy_id', sa.Integer(), nullable=False),
    sa.Column('effectiveness', sa.Enum('weak', 'medium', 'strong', name='effectiveness_types'), nullable=False),
    sa.ForeignKeyConstraint(['counter_strategy_id'], ['counterstrats.id'], ),
    sa.ForeignKeyConstraint(['strategy_id'], ['strats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('narrative_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('narrative_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_outcome_text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['narrative_id'], ['primary_narratives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('secondary_narratives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_narrative_id', sa.Integer(), nullable=False),
    sa.Column('updated_fact_combination_id', sa.Integer(), nullable=False),
    sa.Column('narrative_text', sa.Text(), nullable=False),
    sa.Column('counterstrat_id', sa.Integer(), nullable=False),
    sa.Column('news', sa.JSON(), nullable=False),
    sa.Column('outcome_text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['counterstrat_id'], ['counterstrats.id'], ),
    sa.ForeignKeyConstraint(['original_narrative_id'], ['primary_narratives.id'], ),
    sa.ForeignKeyConstraint(['updated_fact_combination_id'], ['fact_combinations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('secondary_narratives')
    op.drop_table('narrative_events')
    op.drop_table('strategy_effectiveness')
    op.drop_table('primary_narratives')
    op.drop_table('users')
    op.drop_table('strats')
    op.drop_table('facts')
    op.drop_table('fact_combinations')
    op.drop_table('events')
    op.drop_table('counterstrats')
    op.drop_table('actors')
    # ### end Alembic commands ###