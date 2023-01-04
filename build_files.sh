echo "BUILD START"
pip install -r requirment.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"