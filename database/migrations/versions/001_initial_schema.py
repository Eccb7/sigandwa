"""
Initial database schema for Biblical Cliodynamic Analysis System.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-01-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create chronology_era enum
    chronology_era_enum = sa.Enum(
        'CREATION_TO_FLOOD', 'FLOOD_TO_ABRAHAM', 'PATRIARCHS', 'EGYPTIAN_BONDAGE',
        'EXODUS_TO_JUDGES', 'UNITED_MONARCHY', 'DIVIDED_KINGDOM', 'EXILE',
        'POST_EXILE', 'INTERTESTAMENTAL', 'NEW_TESTAMENT', 'EARLY_CHURCH',
        'ROMAN_EMPIRE', 'MEDIEVAL', 'REFORMATION', 'COLONIAL', 'MODERN', 'CONTEMPORARY',
        name='chronologyera'
    )
    chronology_era_enum.create(op.get_bind(), checkfirst=True)

    # Create event_type enum
    event_type_enum = sa.Enum(
        'POLITICAL', 'ECONOMIC', 'RELIGIOUS', 'MILITARY', 'SOCIAL', 'NATURAL', 'PROPHETIC',
        name='eventtype'
    )
    event_type_enum.create(op.get_bind(), checkfirst=True)

    # Create fulfillment_type enum
    fulfillment_type_enum = sa.Enum(
        'COMPLETE', 'PARTIAL', 'REPEATED', 'CONDITIONAL', 'PENDING', 'SYMBOLIC',
        name='fulfillmenttype'
    )
    fulfillment_type_enum.create(op.get_bind(), checkfirst=True)

    # Create chronology_events table
    op.create_table(
        'chronology_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('year_start', sa.Integer(), nullable=False),
        sa.Column('year_end', sa.Integer(), nullable=True),
        sa.Column('year_start_min', sa.Integer(), nullable=True),
        sa.Column('year_start_max', sa.Integer(), nullable=True),
        sa.Column('year_end_min', sa.Integer(), nullable=True),
        sa.Column('year_end_max', sa.Integer(), nullable=True),
        sa.Column('era', chronology_era_enum, nullable=False),
        sa.Column('event_type', event_type_enum, nullable=False),
        sa.Column('biblical_source', sa.String(length=255), nullable=True),
        sa.Column('historical_source', sa.Text(), nullable=True),
        sa.Column('extra_data', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_chronology_events_id', 'chronology_events', ['id'])
    op.create_index('ix_chronology_events_name', 'chronology_events', ['name'])
    op.create_index('ix_chronology_events_year_start', 'chronology_events', ['year_start'])
    op.create_index('ix_chronology_events_era', 'chronology_events', ['era'])
    op.create_index('ix_chronology_events_event_type', 'chronology_events', ['event_type'])

    # Create actors table
    op.create_table(
        'actors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('actor_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('year_start', sa.Integer(), nullable=True),
        sa.Column('year_end', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_actors_id', 'actors', ['id'])
    op.create_index('ix_actors_name', 'actors', ['name'])
    op.create_index('ix_actors_actor_type', 'actors', ['actor_type'])

    # Create patterns table
    op.create_table(
        'patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('pattern_type', sa.String(length=100), nullable=False),
        sa.Column('typical_duration_years', sa.Integer(), nullable=True),
        sa.Column('preconditions', JSON, nullable=True),
        sa.Column('indicators', JSON, nullable=True),
        sa.Column('outcomes', JSON, nullable=True),
        sa.Column('biblical_basis', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_patterns_id', 'patterns', ['id'])
    op.create_index('ix_patterns_name', 'patterns', ['name'])
    op.create_index('ix_patterns_pattern_type', 'patterns', ['pattern_type'])

    # Create event_actors association table
    op.create_table(
        'event_actors',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['chronology_events.id']),
        sa.ForeignKeyConstraint(['actor_id'], ['actors.id']),
        sa.PrimaryKeyConstraint('event_id', 'actor_id')
    )

    # Create event_patterns association table
    op.create_table(
        'event_patterns',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('pattern_id', sa.Integer(), nullable=False),
        sa.Column('strength', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['chronology_events.id']),
        sa.ForeignKeyConstraint(['pattern_id'], ['patterns.id']),
        sa.PrimaryKeyConstraint('event_id', 'pattern_id')
    )

    # Create prophecy_texts table
    op.create_table(
        'prophecy_texts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=255), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('prophet', sa.String(length=100), nullable=True),
        sa.Column('year_declared', sa.Integer(), nullable=True),
        sa.Column('prophecy_type', sa.String(length=100), nullable=True),
        sa.Column('scope', sa.String(length=100), nullable=True),
        sa.Column('elements', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_prophecy_texts_id', 'prophecy_texts', ['id'])
    op.create_index('ix_prophecy_texts_reference', 'prophecy_texts', ['reference'])
    op.create_index('ix_prophecy_texts_prophet', 'prophecy_texts', ['prophet'])

    # Create prophecy_fulfillments table
    op.create_table(
        'prophecy_fulfillments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prophecy_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('fulfillment_type', fulfillment_type_enum, nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('elements_fulfilled', JSON, nullable=True),
        sa.ForeignKeyConstraint(['prophecy_id'], ['prophecy_texts.id']),
        sa.ForeignKeyConstraint(['event_id'], ['chronology_events.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_prophecy_fulfillments_id', 'prophecy_fulfillments', ['id'])
    op.create_index('ix_prophecy_fulfillments_prophecy_id', 'prophecy_fulfillments', ['prophecy_id'])
    op.create_index('ix_prophecy_fulfillments_event_id', 'prophecy_fulfillments', ['event_id'])
    op.create_index('ix_prophecy_fulfillments_fulfillment_type', 'prophecy_fulfillments', ['fulfillment_type'])

    # Create prophetical_patterns table
    op.create_table(
        'prophetical_patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('condition', sa.Text(), nullable=False),
        sa.Column('predicted_outcome', sa.Text(), nullable=False),
        sa.Column('foundational_texts', JSON, nullable=True),
        sa.Column('historical_instances', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_prophetical_patterns_id', 'prophetical_patterns', ['id'])
    op.create_index('ix_prophetical_patterns_name', 'prophetical_patterns', ['name'])

    # Create world_indicators table
    op.create_table(
        'world_indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator_name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('data_source', sa.String(length=255), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('extra_data', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_world_indicators_id', 'world_indicators', ['id'])
    op.create_index('ix_world_indicators_indicator_name', 'world_indicators', ['indicator_name'])
    op.create_index('ix_world_indicators_category', 'world_indicators', ['category'])
    op.create_index('ix_world_indicators_timestamp', 'world_indicators', ['timestamp'])

    # Create simulation_scenarios table
    op.create_table(
        'simulation_scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('input_indicators', JSON, nullable=False),
        sa.Column('assumptions', JSON, nullable=True),
        sa.Column('matched_patterns', JSON, nullable=True),
        sa.Column('historical_analogs', JSON, nullable=True),
        sa.Column('trajectory', JSON, nullable=False),
        sa.Column('risk_vectors', JSON, nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('parameters', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_simulation_scenarios_id', 'simulation_scenarios', ['id'])
    op.create_index('ix_simulation_scenarios_name', 'simulation_scenarios', ['name'])
    op.create_index('ix_simulation_scenarios_created_at', 'simulation_scenarios', ['created_at'])


def downgrade() -> None:
    # Drop tables
    op.drop_index('ix_simulation_scenarios_created_at', table_name='simulation_scenarios')
    op.drop_index('ix_simulation_scenarios_name', table_name='simulation_scenarios')
    op.drop_index('ix_simulation_scenarios_id', table_name='simulation_scenarios')
    op.drop_table('simulation_scenarios')

    op.drop_index('ix_world_indicators_timestamp', table_name='world_indicators')
    op.drop_index('ix_world_indicators_category', table_name='world_indicators')
    op.drop_index('ix_world_indicators_indicator_name', table_name='world_indicators')
    op.drop_index('ix_world_indicators_id', table_name='world_indicators')
    op.drop_table('world_indicators')

    op.drop_index('ix_prophetical_patterns_name', table_name='prophetical_patterns')
    op.drop_index('ix_prophetical_patterns_id', table_name='prophetical_patterns')
    op.drop_table('prophetical_patterns')

    op.drop_index('ix_prophecy_fulfillments_fulfillment_type', table_name='prophecy_fulfillments')
    op.drop_index('ix_prophecy_fulfillments_event_id', table_name='prophecy_fulfillments')
    op.drop_index('ix_prophecy_fulfillments_prophecy_id', table_name='prophecy_fulfillments')
    op.drop_index('ix_prophecy_fulfillments_id', table_name='prophecy_fulfillments')
    op.drop_table('prophecy_fulfillments')

    op.drop_index('ix_prophecy_texts_prophet', table_name='prophecy_texts')
    op.drop_index('ix_prophecy_texts_reference', table_name='prophecy_texts')
    op.drop_index('ix_prophecy_texts_id', table_name='prophecy_texts')
    op.drop_table('prophecy_texts')

    op.drop_table('event_patterns')
    op.drop_table('event_actors')

    op.drop_index('ix_patterns_pattern_type', table_name='patterns')
    op.drop_index('ix_patterns_name', table_name='patterns')
    op.drop_index('ix_patterns_id', table_name='patterns')
    op.drop_table('patterns')

    op.drop_index('ix_actors_actor_type', table_name='actors')
    op.drop_index('ix_actors_name', table_name='actors')
    op.drop_index('ix_actors_id', table_name='actors')
    op.drop_table('actors')

    op.drop_index('ix_chronology_events_event_type', table_name='chronology_events')
    op.drop_index('ix_chronology_events_era', table_name='chronology_events')
    op.drop_index('ix_chronology_events_year_start', table_name='chronology_events')
    op.drop_index('ix_chronology_events_name', table_name='chronology_events')
    op.drop_index('ix_chronology_events_id', table_name='chronology_events')
    op.drop_table('chronology_events')

    # Drop enums
    sa.Enum(name='fulfillmenttype').drop(op.get_bind())
    sa.Enum(name='eventtype').drop(op.get_bind())
    sa.Enum(name='chronologyera').drop(op.get_bind())
