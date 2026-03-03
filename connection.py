from sqlalchemy import create_engine, text
from utils.config import DATABASE_URL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import subprocess
import os
from pathlib import Path

engine = create_engine(DATABASE_URL)


def apply_schema_via_psql(schema_path: str):
	"""
	Apply a SQL schema file using the `psql` CLI.
	"""
	schema_path = Path(schema_path)
	env = os.environ.copy()
	env["PGPASSWORD"] = DB_PASSWORD

	conn_uri = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/postgres"
	cmd = ["psql", conn_uri, "-f", str(schema_path)]
	subprocess.run(cmd, check=True, env=env)


def apply_schema_sqlalchemy(schema_path: str):
	"""
	Apply the SQL schema using SQLAlchemy. This will:
	- connect to the default `postgres` database and create the target DB if missing
	- execute the CREATE TABLE statements from the schema file against the target DB

	This does not require `psql` to be installed.
	"""
	schema_path = Path(schema_path)

	sql = schema_path.read_text()
	# Remove lines that create the database or change connection (psql meta-commands)
	lines = [l for l in sql.splitlines() if not l.strip().lower().startswith("create database") and not l.strip().startswith("\\c")]
	sql_clean = "\n".join(lines)

	# If DATABASE_URL is sqlite, run the statements directly against sqlite file
	if DATABASE_URL.startswith("sqlite"):
		target_engine = create_engine(DATABASE_URL)
		with target_engine.begin() as conn:
			for stmt in sql_clean.split(";"):
				s = stmt.strip()
				if not s:
					continue
				conn.execute(text(s))
		return

	# Otherwise ensure database exists by connecting to 'postgres'
	admin_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
	admin_engine = create_engine(admin_uri)
	with admin_engine.connect() as conn:
		exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :d"), {"d": DB_NAME}).fetchone()
		if not exists:
			conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))

	# Execute statements against the target Postgres DB
	target_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
	target_engine = create_engine(target_uri)
	with target_engine.begin() as conn:
		for stmt in sql_clean.split(";"):
			s = stmt.strip()
			if not s:
				continue
			conn.execute(text(s))