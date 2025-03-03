
setup:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

start:
	docker run -p 6333:6333 -v /home/tiago/smart-story/insights/data/qdrant:/qdrant/storage:z qdrant/qdran

run-pipeline:
	. venv/bin/activate
	python drive.py
	python transcript.py
	python embedding.py