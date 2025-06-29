"""init

Revision ID: 7fac5a09ff0e
Revises: 
Create Date: 2025-06-09 12:38:13.147408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fac5a09ff0e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('platforms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('base_url', sa.String(length=255), nullable=False),
    sa.Column('search_url_template', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_platforms_name'), 'platforms', ['name'], unique=True)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('global_query_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_global_query_name'), 'products', ['global_query_name'], unique=False)
    op.create_table('regression_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('target_variable', sa.String(length=100), nullable=False),
    sa.Column('feature_variables', sa.JSON(), nullable=False),
    sa.Column('coefficients_json', sa.JSON(), nullable=False),
    sa.Column('intercept', sa.Float(), nullable=False),
    sa.Column('r_squared', sa.Float(), nullable=False),
    sa.Column('last_trained_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['platform_id'], ['platforms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_regression_models_platform_id'), 'regression_models', ['platform_id'], unique=False)
    op.create_table('scraped_product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('url_on_platform', sa.String(length=1024), nullable=False),
    sa.Column('name_on_platform', sa.String(length=512), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('reviews_count', sa.Integer(), nullable=False),
    sa.Column('availability_status', sa.String(length=100), nullable=False),
    sa.Column('search_position', sa.Integer(), nullable=False),
    sa.Column('scraped_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['platform_id'], ['platforms.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scraped_product_data_platform_id'), 'scraped_product_data', ['platform_id'], unique=False)
    op.create_index(op.f('ix_scraped_product_data_product_id'), 'scraped_product_data', ['product_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scraped_product_data_product_id'), table_name='scraped_product_data')
    op.drop_index(op.f('ix_scraped_product_data_platform_id'), table_name='scraped_product_data')
    op.drop_table('scraped_product_data')
    op.drop_index(op.f('ix_regression_models_platform_id'), table_name='regression_models')
    op.drop_table('regression_models')
    op.drop_index(op.f('ix_products_global_query_name'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_platforms_name'), table_name='platforms')
    op.drop_table('platforms')
    # ### end Alembic commands ###
