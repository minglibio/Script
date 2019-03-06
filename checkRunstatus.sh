if [ $# -ne 1 ]; then
 echo "error.. need args"
 echo "command:$0 <dir>"
 exit 1
else
for arg in "$@"
do
 echo $arg
done
 echo "Checking .o files..."
 grep "exit" $1/*.o
 echo "Checking .jsub files... (No jsub.sh should exit if the job is finished.)"
 ls -l $1/*.jsub.sh
 echo "These .e files are not empty..."
for i in `ls $1/*.e`
do
 if [ -s $i ]; then
   ls -l $i
 fi
done
fi

