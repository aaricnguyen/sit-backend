# SIT Profile Analyzer API

## A. Setup production environment:

- Docker docker version 20.10.8 or later (recommended)

Install docker by command

```bash
 sudo snap install docker
```

## B. Build production:

- Step 1: Create a .env file and edit it based on the environment variable in the .env.example file

- Step 2: Run command:

```bash
  docker-compose up -d --build
```

### Note:

> If your server can connect to the external internet. You just need to go to this step on your server and check the API at http://your-ip-server:4500

> If your server don't have internet connection you need to do production build on local machine and follow below steps:

1. Compress and save the Docker image with the command:

```bash
  docker save spdat_backend_sit_profile_analizer -o ./spdat_backend_sit_profile_analizer.tar
  docker save redis:latest -o ./redis.tar
```

2. Upload 2 zipped files from localhost to your server (redis.tar and ./spdat_backend_sit_profile_analizer.tar)

3. On the server at the directory containing the 2 files you just uploaded, run the following command to import the docker image into your docker server:

```bash
  docker load < ./spdat_backend_sit_profile_analizer.tar
  docker load < ./redis.tar
```

<div style="page-break-after: always;"></div>

4. To run the newly loaded docker images, we use the following command:

```bash
  docker run -dit --name cache -p 6379:6379 redis:latest
```

```bash
  docker run -dit --name spdat_backend_sit_profile_analizer_api -p 4500:4500 -v /home/bjatti/configCompareTool/project/custConfs/cfgFiles:/usr/app/src/utils/cfgFiles -e REDIS_URL=redis://10.78.96.161 -e DATABASE_USER=a1 -e DATABASE_PASSWORD=Maglev123! -e DATABASE_HOST=10.78.96.161 -e DATABASE_NAME=custConfigDB spdat_backend_sit_profile_analizer
```

Check API at http://10.78.96.161:4500

## C. References

- [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)
- [Redis](https://redis.io/documentation)
