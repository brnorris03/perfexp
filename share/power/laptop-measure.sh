#!/bin/bash

#
# this is a MIC specific script
#

if [ -z "$1" ] ; then
    echo "Usage: measure.sh mode"
    exit 0
fi

mode=$1
prepoh=0

case $mode in 
    0)
	L='memcopy-L1'
	A="-m m -s 16384"
	;;
    1)
	L='memcopy-L2'
	A="-m m -s 131072"
	;;
    2)
	L='memcopy-L3'
	A="-m m -s 786432"
	;;
    3)
	L='memcopy-DRAM'
	A="-m m -s 8388608"
	;;
    4)
	L='random-L1'
	A="-m r -s 16384"
	prepoh=11
	;;
    5)
	L='random-L2'
	A="-m r -s 131072"
	prepoh=11
	;;
    6)
	L='random-L3'
	A="-m r -s 786432"
	prepoh=11
	;;
    7)
	L='random-DRAM'
	A="-m r -s 8388608"
	prepoh=20
	;;
    *)
	echo "unknown:" $mode
	exit 1
	;;
esac

make

FN=result-${L}.txt

if [ -f  $FN ] ; then
    echo "Remove $FN first"
    exit 1
fi

TMP1=/tmp/measure1.$$.txt
TMP2=/tmp/measure2.$$.txt
rm -f $TMP1 $TMP2

./laptop-watt.py 2 0  > /dev/null

sleep 1

echo "Start measurement.. wait a while..."

touch $TMP1 $TMP2

echo "measurement time: " `expr 30 + ${prepoh}`
./laptop-watt.py  `expr 30 + ${prepoh}` 0 >> $TMP1  &

echo "./manycore-heater -t 10 ${A}" 
./manycore-heater -t 10 ${A}  >> $TMP2

wait 

cat $TMP2 | egrep 'HEATER' > $FN
preptime=`cat $TMP2 | ./getpreptime.pl`
cat $TMP1 | ./offsettime.pl $preptime >> $FN

echo "Check $FN"

rm -f $TMP1 $TMP2

echo "done"
