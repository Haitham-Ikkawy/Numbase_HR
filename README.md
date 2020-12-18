Project Requirements:

We need to build a small web application that can help employees to facilitate and manage their information.


Once the employee login, he can:

See his current title and in which department he belongs to
Check In/Out (He cannot check out if did not check in first in same day)
See his remaining vacation days (15 days).
Mark a day as OFF if possible(off days will be counted as he works full time)
Change personal information (First name, last name, email, phone number)
See his previous attendance records
See his salary auto calculated based on his hours attendance (An hour rate is set for each employee by the administrator) for the current month only.


Added Features:

Registration form (not active)
Password reset by email
Password change
Vacation addition from date to date
Calculate salary based on working hourse and off days separately


Usecase Diagram:

![NM -HR](https://user-images.githubusercontent.com/71630560/102553291-5398e580-40cb-11eb-8866-c9a2965024aa.png)


Steps to run the project:
1) create a virtual environment via "virtualenv -p <python version>  <venv_name>" command
2) run "git clone git@github.com:Haitham-Ikkawy/Numbase_HR.git" command (inside the virtualenv root directory)
3) create a mysql database with "numbase" name
4) run "Scripts\activate" command, within the project root directory
5) run "pip install -r requirements.txt" command (inside Numbase_HR/src)
6) run "py manage.py makemigrations" command
7) run "py manage.py migrate" command
8) run "py manage.py loaddata DB_dump.json" command
9) run "py manage.py runserver"


Credentials:

1)admin:
        email:admin@test.com
        password:admin
        
2)employee user:
        email:haithamikkawy@outlook.com
        password:test@test
        
  



