#!/bin/bash

while true; do
    sleep 60
    mysqldump -u root -p${MYSQL_ROOT_PASSWORD} -h ${MYSQL_HOSTNAME} --databases ${MYSQL_DATABASE} > ${BACKUP_FILE_NAME}
    aws s3 cp ${BACKUP_FILE_NAME} ${BACKUP_S3_FILE_PATH}
done
