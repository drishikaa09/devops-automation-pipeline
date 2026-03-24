#!/bin/bash
echo "ENTER PROJECT NAME:"
read project_name
if [ -d "$project_name" ]; then
echo "Project already exist!"
exit 1
fi

echo "How many files do you want?"
read num
mkdir $project_name
cd $project_name
echo "Project $project_name created at $(date)" > log.txt
for(( i=1;i<=num;i++))
do
touch file$i.txt
echo "created file$i.txt at$(date)" >> log.txt
done
echo "setup completed successfullyy!!!"
