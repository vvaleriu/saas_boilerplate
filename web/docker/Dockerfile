FROM node:lts-iron

############
#
# BEST PRACTICE FOR NODEJS DOCKERFILE https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md
#
# RAPPEL : lorsqu'on monte un volume depuis l'exterieur via un docker compose,
# les donnees de l'hote ecrasent les donnees du conteneur. De faite, ca fait disparaitre
# le dossier node_modules. C'est pour cela qu'il faut creer un data volume dans le docker-compose
############


# If you need to install global npm dependencies, it is recommended to place those dependencies in the non-root user directory.
# To achieve this, add the following line to your Dockerfile
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH=$PATH:/home/node/.npm-global/bin

ENV NODE_ENV=development
ENV HTTP_APP_PORT=5173
ENV APP_PATH=/var/www/app/

# Installation de YARN
# RUN npm install --global --force yarn
RUN npm install -g pnpm

# Creation du dossier et creation du volume
RUN mkdir -p ${APP_PATH}
RUN chmod -R 775 ${APP_PATH}
RUN chown -R node:node ${APP_PATH}
RUN chown -R node:node /home/node/

VOLUME ${APP_PATH}/
# At the end, set the user to use when running this image
USER node

# COPY ../app/package.json ${APP_PATH}
# COPY ./app/package.json ${APP_PATH}

EXPOSE ${HTTP_APP_PORT}

# Installation de sveltekit
# WORKDIR /var/www
# RUN pnpm create svelte@latest app
WORKDIR ${APP_PATH}
RUN pnpm install

# ENTRYPOINT ["tail", "-f", "/dev/null"]
