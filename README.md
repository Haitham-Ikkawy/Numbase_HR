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

1) git clone git@github.com:Haitham-Ikkawy/Numbase_HR.git
2) run "pip install -r requirements.txt"
3) run "py manage.py makemigrations"
4) run "py manage.py migrate"
5) run "py manage.py loaddata DB_dump.json"
6) run "py manage.py runserver"


Credentials:

1)admin:
        email:admin@test.com
        password:admin
        
2)employee user:
        email:haithamikkawy@outlook.com
        password:test@test
        
  



