## Сервис классификации сгенерированных текстов

Для работы сервиса необходимо установить Docker и docker-compose с поддержкой nvidia-container-runtime, чтобы использовать CUDA нужно установить драйвера NVIDIA:

`sudo apt update`
`sudo apt install -y nvidia-driver-418`

Для билда сервиса выполните команду:

`docker-compose up -d --build`

Для запуска и перезапуска сервиса выполните команду:

`docker-compose up -d --force-recreate`

Сервис поднимается по умолчанию на 5020 порту, база данных на 5060 порту, веса модели хранятся в папке `checkpoints/`.