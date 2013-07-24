#!/bin/bash

#
# this is a MIC specific script
#

if [ -z "$1" ] ; then
    echo "Usage: measure.sh mode [cardno]"
    exit 0
fi

cardno=1

if [ ! -z "$2" ] ; then
    cardno=$2
fi

echo cardno: $cardno

MIC=root@192.168.0.20${cardno}  # XXX: this is site-specific

stressduration=20  # sec

mode=$1
prepoh=0

case $mode in 
    0)
	L='FPU'
	A='-m f'
	;;
    1)
	L='FPUARCH'
	A='-m F'
	;;
    2)
	L='memcopy-L1'
	A="-m m -s 8192"
	;;
    3)
	L='memcopy-L2'
	A="-m m -s 65536"
	;;
    4)
	L='memcopy-DRAM'
	A="-m m -s 262144"
	;;
    5)
	L='random-L1'
	A="-m r -s 8192"
	prepoh=10
	;;
    6)
	L='random-L2'
	A="-m r -s 65536"
	prepoh=30
	;;
    7)
	L='random-DRAM'
	A="-m r -s 262144"
	prepoh=60
	;;
    8)
	L='memcopy-DRAM-huge'
	A="-m m -s 262144 -H /huge/"
	;;
    *)
	echo "unknown:" $mode
	exit 1
	;;
esac

#make

FN=result-${L}.txt

if [ -f  $FN ] ; then
    echo "Remove $FN first"
    exit 1
fi

TMP1=/tmp/measure1.$$.txt
TMP2=/tmp/measure2.$$.txt
rm -f $TMP1 $TMP2


./micwatt.py $cardno 2  0 > /dev/null  # warm-up 4 secs

echo "Copy the heater.."
scp manycore-heater $MIC:/tmp 

sleep 2

touch $TMP1 $TMP2

totalmeasure=`expr ${prepoh} + ${stressduration} \* 2` 

printf "Start measurement..  total=%3d sec => prepoh=%2d sleep=%d stress=%d sleep=%d\n" \
$totalmeasure \
${prepoh} \
`expr ${stressduration} / 2` \
${stressduration} \
`expr ${stressduration} / 2` 

# start the power profiling and the stress code.  there may be a
# slight differnce in the start time but probably won't be an issue.


./micwatt.py $cardno `expr $totalmeasure + ${stressduration}` 2 >> $TMP1  &

echo "/tmp/manycore-heater -t $stressduration ${A}" 
ssh $MIC "/tmp/manycore-heater -t $stressduration ${A}"  >> $TMP2

wait 

cat $TMP2 | egrep 'HEATER' > $FN
echo "# CARDNO=$cardno" >> $FN
echo "# DURATION=$stressduration" >> $FN
preptime=`cat $FN | ./getpreptime.pl`
cat $TMP1 | ./offsettime.pl $preptime >> $FN

echo "Check $FN"

#rm -f $TMP1 $TMP2

echo "done"
