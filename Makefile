install:
	pip install uv fastapi[standard] polars
run:
	uv run fastapi dev melete.py
test_data:
	python generate_test_df.py
