URL="http://0.0.0.0:5006/thor-igot/image/upload"
b=200
count=0
path="$PWD/images"
declare -a INPUT=( "${path}"/* )
for i in "${INPUT[@]}"
do
    TEST="curl -X POST -F image=@$i $URL"
    RESPONSE=`$TEST`
    VALUE=$( jq -r  '.code' <<< "${RESPONSE}" )
    if [ $VALUE == $b ]
    then
        count=$((count+1))
        echo "Test $count Passed!"
        continue
    fi
    count=$((count+1))
    echo "Test $count Failed!"
done
