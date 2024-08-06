Docker and Python:


Rutas dónde se almacena en Docker en Windows10:
===============================================

C:/ProgramData/Docker
C:/ProgramData/DockerDesktop
C:\ProgramData\Microsoft\Windows\Hyper-V
Nota: quitarles "Compress..." a estas rutas en Windows, sino da un error.

Comandos:
=========

docker ps  # lists containers (images that have been executed)
docker images  # lists images (not containers)
docker rmi <img id> -f   # forced container deletion
docker run <img id>  # runs containers
docker system prune  # prune of all types of objects-sometime does not reclaim space??????
docker image prune -a  # really deletes images (all that may exist) not in use by any container/reclaims disk space
docker container prune --filter "test1"

Attribute File: this may help to use python*slim versions and reduce container's size
%programdata%\docker\config\daemon.json'
experimental=true if OS=windows and want to try python slim versions....????


Dónde parecen quedar las imágenes físicas en windows?:
======================================================
R.- c:\ProgramData\Docker\*


Cuando da el error:
===================
PS C:\ALEX\SW\Coding\Python\SelfTests\docker_tests\test2> docker build -t t5sep19.4 . --compress --rm
Sending build context to Docker daemon     951B
Step 1/4 : FROM python:3.8-slim-bullseye
3.8-slim-bullseye: Pulling from library/python
7d97e254a046: Extracting [==================================================>]  31.42MB/31.42MB
b48a7335bd4c: Download complete                                                   
...
1f80b77e725b: Download complete 
failed to register layer: rename C:\ProgramData\Docker\image\lcow\layerdb\tmp\write-set-688413486 C:\ProgramData\Docker\image\lcow\layerdb\sha256\6e3b92711bf1028e9565d1f7bdae6de5d1323597de24629c27d757060eaa3019: Access is denied.
R.- Desactivar el antivirus (parece que bloquea el acceso a archivos locales)


rename C:\ProgramData\Docker\image\lcow\layerdb\tmp\write-set-224625335 C:\ProgramData\Docker\image\lcow\layerdb\sha256\7f896e5b7e653199f98f774604e37f21bada4c0d786482209a6559d88e4f3045: Access is denied.
R.- Activate the experimental mode (at settings/Daemon) and restart