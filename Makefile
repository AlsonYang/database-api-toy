install: 
	pip install --upgrade pip &&\
		pip install -r requirements.txt

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

all_fastapi: install init_db host_fastapi
all_flask: install init_db host_flask