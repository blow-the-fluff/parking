#!/bin/bash
git clone https://github.com/timotdsantos/darknet.git
cd darknet
make clean all
wget https://pjreddie.com/media/files/darknet53.conv.74 

cd ..

cp Field\ Extraction\ -\ experiments.ipynb darknet/
cp Field\ Extraction\ -\ 23\ Fields.ipynb darknet/
