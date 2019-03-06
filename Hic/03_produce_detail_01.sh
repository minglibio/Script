for i in `ls  ~/xiaoming/tianxiaomeng/data/1000000/*_1000000_ord.bed`
do 
export a=`basename  $i _1000000_ord.bed`
echo python2  /home/jiangyu/xiaoming/tianxiaomeng/shell/01_novelTOchr_HIC.py   --bed  /home/jiangyu/xiaoming/tianxiaomeng/data/1000000/$a"_1000000_abs.bed"  --matrix /home/jiangyu/xiaoming/tianxiaomeng/data/1000000/$a"_1000000.matrix"  --output /home/jiangyu/xiaoming/tianxiaomeng/out/$a"_raw_position" >/home/jiangyu/xiaoming/tianxiaomeng/shell/new/$a"raw_position.sh"
done
