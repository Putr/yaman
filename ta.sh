source "${BASH_SOURCE%/*}/base.sh"

echo "Building profile for TA"

cd /var/www/projects/work/totalAssesment/dashboard
sudo webserverStopLocal
sleep 0.5
docker-compose start
sleep 1

createSession "dev"
createSession "logsDrush"
createSession "logsLaravel"
createSession "drush"
createSession "mysql"
createSession "lambdatest"
createSession "ta.stage"

sendCommand 1 "jump ta"
sendCommand 1 "git status"

sendCommand 2 "jump ta"
sendCommand 2 "docker-compose exec php bash"
sendCommand 2 "cd www"
sendCommand 2 "drush ws --tail"

sendCommand 3 "jump ta"
sendCommand 3 "cd api/storage/logs/"
sendCommand 3 "tail -f laravel.log"

sendCommand 4 "jump ta"
sendCommand 4 "docker-compose exec php bash"
sendCommand 4 "cd www"

sendCommand 5 "jump ta"
sendCommand 5 "docker-compose exec mysql_ta bash"
sendCommand 5 "mysql -u root -ptapass dashboard"

sendCommand 6 "cd ~/lambdatest"

sendCommand 7 "ssh ta.stage"
