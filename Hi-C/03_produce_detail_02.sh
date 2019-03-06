for i in `ls  ~/xiaoming/tianxiaomeng/data/1000000/*_1000000_ord.bed`
do 
export a=`basename  $i _1000000_ord.bed`
bash /home/jiangyu/xiaoming/tianxiaomeng/shell/02_dealwith_novelTOchr_infro.sh ~/xiaoming/tianxiaomeng/out/$a"_raw_position"   ~/xiaoming/tianxiaomeng/out/$a"_accuracy_position" ~/xiaoming/tianxiaomeng/out/$a"_rough_position"
done
