echo "BUILD START"
pip3 install -r requirment.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"