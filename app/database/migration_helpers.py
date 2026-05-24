"""Helpers reutilizáveis em migrations Alembic."""

from alembic import op

UPDATED_AT_FUNCTION = """
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

UPDATED_AT_FUNCTION_DROP = "DROP FUNCTION IF EXISTS set_updated_at();"

TABLES_WITH_TIMESTAMPS = ("usuarios", "marcas", "modelos", "carros")


def create_updated_at_triggers() -> None:
    op.execute(UPDATED_AT_FUNCTION)
    for table in TABLES_WITH_TIMESTAMPS:
        op.execute(
            f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE PROCEDURE set_updated_at();
            """
        )


def drop_updated_at_triggers() -> None:
    for table in TABLES_WITH_TIMESTAMPS:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};")
    op.execute(UPDATED_AT_FUNCTION_DROP)
