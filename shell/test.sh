#!/bin/bash
#. ./test1.sh
your_name='gao'
str="hello, i know you are \"$your_name\"!\n"
echo ${#str}
array_name=(value0 value1 value2 value3)
for i in  ${array_name[@]}; do
    echo $i
done
aaa=$((2+2))
echo $aaa
a=10
b=20
if  [ $a -lt $b ]
then
    echo "$a is less than $b"
fi

#read name
#echo "you entered $name"

fun1(){
    echo "this is fun1 function"
    echo "para num is $#"
    echo "para is $*"
    return 2
}

fun1 1 2 3 4 5
echo $#
echo "in test1.sh file,url is $url "
echo "the last pid is $!"
