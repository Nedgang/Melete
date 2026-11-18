install:
	pip install uv fastapi[standard] duckdb polars pyarrow
run:
	uv run fastapi dev melete.py
