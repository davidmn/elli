now=`date +"%Y-%m-%d"`
here="$(pwd)"
echo "creating backup for $now"
echo $here
cd ~/
zip -r -q $now elli/ 
mv "$now.zip" "/home/megaslippers/Dropbox/diss-backup/$now.zip"
cd $here