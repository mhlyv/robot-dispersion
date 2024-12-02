while true
do
				./main.py &
				sleep 10
				pkill -f "python3 ./main.py"
done
