FROM python:alpine

ARG USER=django
ENV HOME /home/$USER

# install sudo as root
RUN apk add --update sudo

# add new user
RUN adduser -D $USER \
        && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        && chmod 0440 /etc/sudoers.d/$USER

USER $USER
WORKDIR $HOME

COPY ./requirements.txt .
COPY ./entrypoint.sh .
COPY ./app app

RUN sudo chown $USER:$USER app -R
RUN pip install -r requirements.txt --no-cache-dir

RUN sudo chmod +x $HOME/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]