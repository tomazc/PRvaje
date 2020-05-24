docker build --rm -t pr-vaje -f Dockerfile-run .
docker run --rm -i -p 8888:8888 -v "$PWD":/home/jovyan/work -w /home/jovyan/work pr-vaje
