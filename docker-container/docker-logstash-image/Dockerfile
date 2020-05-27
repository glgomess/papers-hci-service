# Clone the official Logstash Image Repository
FROM docker.elastic.co/logstash/logstash:7.7.0
# Install elasticsearch plugins
RUN logstash-plugin install logstash-output-elasticsearch
# Copy the default logstash file. This is only used during build.
COPY /config/logstash.conf /logstash-config/
COPY /mysql-connector-java-5.1.46/ /lib/mysql-connector-java-5.1.46/
# Run logstash config
CMD ["logstash", "-f", "/logstash-config/logstash.conf"]
