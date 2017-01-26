FROM msagency/msa-image-python:1.0.2

ADD harry /opt/ms/harry
ADD requirements.txt /opt/ms/

# Install the dependencies
RUN apk add --update gcc zlib-dev libconfig-dev libarchive-dev automake autoconf libtool make libc-dev python-dev \
    && cd /opt/ms/harry \
    && ./bootstrap \
    && ./configure \
    && make \
    && make install \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install -r /opt/ms/requirements.txt \
    && apk del make automake autoconf libtool python-dev \
    && rm -rf /tmp/* /var/cache/apk/*

# Override the Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Override the default endpoints
ADD README.md NAME LICENSE VERSION /opt/ms/
ADD swagger.json /opt/swagger/swagger.json

# Copy all the other application files to /opt/ms
ADD run.sh /opt/ms/
ADD app.py /opt/ms/
ADD data /opt/ms/data

# Execute the run script
CMD ["ash", "/opt/ms/run.sh"]
