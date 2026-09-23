install:
	pip install uv fastapi[standard] polars
api:
	uv run fastapi dev api.py
test_data:
	python generate_test_df.py
