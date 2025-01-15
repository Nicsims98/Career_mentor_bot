"""Add new tables for internships, chat, recommendations, and mentorship

Revision ID: 80385a1070cf
Revises: d99cc5fdd4d0
Create Date: 2025-01-12 20:31:06.743795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80385a1070cf'
down_revision = 'd99cc5fdd4d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=200), nullable=True),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('advice', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('internship_listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('company_name', sa.String(length=200), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('duration', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('requirements', sa.Text(), nullable=True),
    sa.Column('compensation', sa.String(length=200), nullable=True),
    sa.Column('application_deadline', sa.Date(), nullable=True),
    sa.Column('contact_email', sa.String(length=120), nullable=True),
    sa.Column('industry', sa.String(length=100), nullable=True),
    sa.Column('industry_type', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mentorship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('method_of_contact', sa.String(length=100), nullable=False),
    sa.Column('expertise', sa.Text(), nullable=False),
    sa.Column('experience', sa.Text(), nullable=False),
    sa.Column('availability', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommendations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('courses', sa.Text(), nullable=True),
    sa.Column('companies', sa.Text(), nullable=True),
    sa.Column('career_paths', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('work_type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('education', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('work_experience', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('short_term_career_goals', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('long_term_career_goals', sa.Text(), nullable=True))
        batch_op.drop_column('username')
        batch_op.drop_column('career_goals')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('career_goals', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('long_term_career_goals')
        batch_op.drop_column('short_term_career_goals')
        batch_op.drop_column('work_experience')
        batch_op.drop_column('education')
        batch_op.drop_column('location')
        batch_op.drop_column('work_type')
        batch_op.drop_column('age')

    op.drop_table('recommendations')
    op.drop_table('mentorship')
    op.drop_table('internship_listings')
    op.drop_table('chat_log')
    # ### end Alembic commands ###
