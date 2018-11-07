#!/bin/sh

#Arrange files like this:
#    hoge/${student number}/fuga.c
#And execute below at hoge:
#    ./extract.sh fuga.c

assignment_name=${1%.c}
mkdir ./${assignment_name}_again

for file in $(ls ./*/*${assignment_name}*.c); do
	base_name=$(basename ${file})
	dir_name=$(dirname ${file})
    parent_name=${dir_name##*/}

    if [ ! -d ./${assignment_name}_again/${parent_name} ]; then
        mkdir ./${assignment_name}_again/${parent_name}
    else
        :
    fi

    cp -v ${file} ./${assignment_name}_again/${parent_name}/${base_name}
done

echo "Done!"