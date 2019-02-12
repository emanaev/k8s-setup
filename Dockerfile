FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y \
    libssl-dev python-dev sshpass apt-transport-https jq \
    ca-certificates curl gnupg2 software-properties-common python-pip
#RUN  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
#     add-apt-repository \
#     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#     $(lsb_release -cs) \
#     stable" \
#     && apt update -y && apt-get install docker-ce -y
RUN mkdir /ansible
WORKDIR /ansible
COPY requirements.txt requirements.txt
RUN /usr/bin/python -m pip install pip -U && python -m pip install -r requirements.txt
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.13.2/bin/linux/amd64/kubectl \
    && chmod a+x kubectl && cp kubectl /usr/local/bin/kubectl

COPY . .

ARG  ID_RSA
# Prepare key using 
#--build-arg ID_RSA="`cat ~/.ssh/id_rsa|paste -sd ';' -`"
#RUN  echo $ID_RSA | sed 's/;/\n/g' >/id_rsa && chmod 400 /id_rsa
#RUN  echo "    IdentityFile /id_rsa" >> /etc/ssh/ssh_config
#CMD ["ansible-playbook", "-i", "hosts.ini", "install.yml"]
ENTRYPOINT ["./ansible.sh"]
