ansible-galaxy install -r requirements.yml

docker run -d --name debian debian:latest ping google.com
docker run -d -name centos centos:latest ping google.com

ansible-playbook nginx-playbook.yml -i docker_inventory.py
