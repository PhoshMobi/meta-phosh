FROM debian:forky-slim

RUN export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y update \
   && apt-get -y install --no-install-recommends wget ca-certificates gnupg eatmydata \
   && eatmydata apt-get -y update \
   && eatmydata apt-get -y dist-upgrade \
   && cd /home/user/app \
   && eatmydata apt-get install --no-install-recommends -y markdownlint meson git python3 uncrustify intltool gettext dpkg-dev \
   && eatmydata apt-get clean
