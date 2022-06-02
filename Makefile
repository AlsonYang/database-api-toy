install: 
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black server/*.py

lint:
	pylint --extension-pkg-whitelist='pydantic' --disable=R,C server/*.py

test:
	echo 'Echoing fake test done'
	# python -m pytest -vv --cov=<fn name> <test script>.py

init_db:
	python server/db_init_cli.py --force True

host_fastapi:
	python server/app_fastapi.py &

host_flask:
	python server/app_flask.py &
	
curl_request:
	bash client/post_member.sh
	bash client/get_members.sh
	bash client/get_member.sh
	bash client/put_member.sh
	bash client/get_members.sh
	bash client/delete_member.sh
	bash client/get_members.sh 
all_for_build: install format lint test 
all_fastapi: install init_db host_fastapi
all_flask: install init_db host_flask
