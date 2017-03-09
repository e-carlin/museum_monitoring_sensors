#!/bin/bash
echo "****** cd to /var/www/museum_monitoring_sensors"
cd /var/www/museum_monitoring_sensors
echo "****** Removing any non saved changes"
sudo git checkout .
echo "****** Pulling the latest code"
sudo git pull
echo "****** cd into app"
cd museumWebAppRails
echo "****** bundle install"
bundle install --deployment --without development test
echo "****** assets compile"
bundle exec rake assets:precompile db:migrate RAILS_ENV=production
echo ""
echo "****** Getting secret key"
secretKey=$(bundle exec rake secret)
echo $secretKey
echo "******* Replacing scret key"
sed -ie "s/keyToBeReplaced/$secretKey/g" config/secrets.yml
echo "******** Deleting temp file"
rm config/secrets.ymle
echo "****** Once you have done this run: sudo passenger-config restart-app $(pwd)"
