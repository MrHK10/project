echo "BUILD START"
Python 3.12.2 -m pip install requirements.txt
Python 3.12.2 manage.py collectstatic --noinput --clear
echo "BUILD END"