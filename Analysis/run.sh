#!/bin/bash

cp RunAll.py RunAll_1.py
sed -ie "s/range(0, 17)/range(0, 4)/g" RunAll_1.py

cp RunAll.py RunAll_2.py
sed -ie "s/range(0, 17)/range(4, 8)/g" RunAll_2.py

cp RunAll.py RunAll_3.py
sed -ie "s/range(0, 17)/range(8, 12)/g" RunAll_3.py

cp RunAll.py RunAll_4.py
sed -ie "s/range(0, 17)/range(12, 17)/g" RunAll_4.py

nohup nice python RunAll_1.py > RunAll_1.log &
nohup nice python RunAll_2.py > RunAll_2.log &
nohup nice python RunAll_3.py > RunAll_3.log &
nohup nice python RunAll_4.py > RunAll_4.log &
