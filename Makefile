install:
	pip install uv fastapi[standard] fastapi-middleware duckdb polars pyarrow
run:
	uv run fastapi dev melete.py
