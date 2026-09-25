install:
	pip install uv fastapi[standard] duckdb polars pyarrow
run:
	uv run fastapi dev melete.py
test_data:
	python generate_test_df.py
