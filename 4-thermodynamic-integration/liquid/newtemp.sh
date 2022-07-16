mytemp=$1
cp -r BASE ${mytemp}K
cd ${mytemp}K
sed -i "s/MYTEMP/${mytemp}/g" job.sh
sed -i "s/MYTEMP/${mytemp}/g" start.lmp
