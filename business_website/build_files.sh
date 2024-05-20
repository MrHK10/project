echo "BUILD START"
 Python 3.12 -m pip install -r requirements.txt
 Python 3.12 manage.py collectstatic --noinput --clear
 echo "BUILD END"