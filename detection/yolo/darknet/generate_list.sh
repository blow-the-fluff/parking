#!/bin/bash

# $1 file directory
# $2 text file

cd $1

ROOTDIR=$(pwd)

ls | grep png | sed -e 's/\(.*\)/$ROOTDIR\/\1/g' >> $2

cd -
mv $1/$2 ./
