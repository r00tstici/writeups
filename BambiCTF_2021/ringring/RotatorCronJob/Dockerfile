FROM alpine:3.3

# Copy hello-cron file to the cron.d directory
COPY RotatorCronJob/log_rotator.cron /log_rotator.cron
COPY RotatorCronJob/rotate_files.sh /rotate_files.sh
COPY RotatorCronJob/entry.sh /entry.sh
RUN chmod 755 /rotate_files.sh /entry.sh
RUN /usr/bin/crontab /log_rotator.cron

CMD ["/entry.sh"]

