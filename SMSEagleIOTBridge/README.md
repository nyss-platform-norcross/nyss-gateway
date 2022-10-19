# Setup SMSEagle device

    mkdir -p /etc/apt/keyrings && chmod -R 0755 /etc/apt/keyrings
    curl -fsSL "https://download.docker.com/linux/raspbian/gpg" | gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/raspbian stretch stable" > /etc/apt/sources.list.d/docker.list

    do-not-use_apt install -y docker-ce

    docker run -d --privileged --hostname container --net host \
      --name=iot-handler \
      --restart=always \
      --env IOT_HUB_CONNECTIONSTRING='<azure_device_key>' \
      --env SMSEAGLE_USERNAME='azure-iot-pakistan' \
      --env SMSEAGLE_PWD='1234!@#$qwerQWER' \
      giskou/smseagle-iot-handler:latest
