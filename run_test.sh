set -x

pwd
ls ./*dcm

for dcm in `ls *dcm`
do
    ./test_dcm.py $dcm
done
