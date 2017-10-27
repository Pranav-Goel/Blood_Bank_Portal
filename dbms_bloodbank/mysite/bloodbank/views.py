from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from .models import User
from django.contrib import auth

import re
from datetime import datetime
import MySQLdb

def home(request):
    template = loader.get_template('bloodbank/home.html')
    return render(request, 'bloodbank/home.html')

def aboutus(request):
    template = loader.get_template('bloodbank/aboutus.html')
    return render(request, 'bloodbank/aboutus.html')

def emplogin(request):
    template = loader.get_template('bloodbank/emplogin.html')
    return render(request, 'bloodbank/emplogin.html')

def donorlogin(request):
    template = loader.get_template('bloodbank/donorlogin.html')
    return render(request, 'bloodbank/donorlogin.html')

def donatehome(request):
    template = loader.get_template('bloodbank/donatehome.html')
    return render(request, 'bloodbank/donatehome.html')

def adminlogin(request):
    template = loader.get_template('bloodbank/adminlogin.html')
    return render(request, 'bloodbank/adminlogin.html')
	
def adminauth(request):
    if(request.POST):
	password = request.POST.get('password')
    	if(password=='admin123'):
		LOW=''
		ss = "select blood_group from Blood_Inventory where quantity<=20.00;"
		cursor = connection.cursor()
		cursor.execute(ss)
		row=cursor.fetchall()
		print(row)
		cursor.close()
		if row=='':
			LOW=''
		else:
			LOW='warning'
			lll=[]
			for x in row:
			    lll.append(x[0])
		if(LOW==''):
	        	return render(request, 'bloodbank/admindash.html')
		else:
			return render(request, 'bloodbank/admindash.html', {'row':lll, })
	else:
	    return render(request, 'bloodbank/adminlogin.html', {'error':"Incorrect Password",})
    else:
	return HttpResponse("Invalid Request")

def admindash(request):
	LOW=''
	ss = "select blood_group from Blood_Inventory where quantity<=20.00;"
	cursor = connection.cursor()
	cursor.execute(ss)
	row=cursor.fetchall()
	print(row)
	cursor.close()
	if row=='':
		LOW=''
	else:
		LOW='warning'
		lll=[]
		for x in row:
		    lll.append(x[0])
	if(LOW==''):
		return render(request, 'bloodbank/admindash.html')
	else:
		return render(request, 'bloodbank/admindash.html', {'row':lll, })
	

def emplist(request):
    sql="select * from Employee;"
    cursor = connection.cursor()
    cursor.execute(sql)
    row=cursor.fetchall()
    print(row)
    cursor.close()
    l=[]
    for x in row:
	l.append(list(x[:-1]))
    return render(request,'bloodbank/emplist.html',{'row':l, })

def empupdate(request):
    sql = "select employee_ID from Employee;"
    cursor = connection.cursor()
    cursor.execute(sql)
    row=cursor.fetchall()
    print(row)
    cursor.close()
    l=[]
    for r in row:
	l.append(r[0])
    print(l)
    return render(request,'bloodbank/empupdate.html',{'row':l, })

def updateauth(request):
    if(request.POST):
	sql1 = "select employee_ID from Employee;"
	cursor = connection.cursor()
	cursor.execute(sql1)
	row=cursor.fetchall()
	print(row)
	cursor.close()
	l=[]
	for r in row:
	    l.append(r[0])
	print(l)
	employee_ID = request.POST.get('employee_ID')
	name = request.POST.get('name')
	age = request.POST.get('age')
	salary = request.POST.get('salary')
	contact_no = request.POST.get('contact_no')
	email_id = request.POST.get('email_id')
    	if(not name.replace(' ','').isalpha()):
	    ename = "Invalid name. Please enter valid details"
	    return render(request, 'bloodbank/empupdate.html', {'ename':ename, 'row':l, })
	if(int(age)<18 or int(age)>55):
	    eage = "Invalid age - Note that the allowed employee age is from 18 upto 55 years. Please enter valid details"
	    return render(request, 'bloodbank/empupdate.html', {'eage':eage, 'row':l, })
	if(int(salary)<10000 or int(salary)>50000):
	    esal = "Please recheck the salary - It ought to range from 10000 to 50000 (per month)"
	    return render(request, 'bloodbank/empupdate.html', {'esal':esal, 'row':l, })
	if(not re.match(r'[\+]?[0-9].',contact_no)):
	    eno = "Please recheck the contact number entered"
	    return render(request, 'bloodbank/empupdate.html', {'eno':eno, 'row':l, })
	if(not re.match(r'[^@]+@[^@]+\.[^@]+',email_id)):
	    emid = "Please enter a valid Email id !!"
	    return render(request, 'bloodbank/empupdate.html', {'emid':emid, 'row':l, })
				
        sql="update Employee set name=(%s),age=(%s),salary=(%s),contact_no=(%s),email_id=(%s) where employee_ID=(%s);"
	try:
		cursor = connection.cursor()
		cursor.execute(sql, [name, age, salary, contact_no, email_id, employee_ID])	
	except Exception as e:
		print(e)			
	finally:
		cursor.close()
	return render(request, 'bloodbank/succupdate.html', {'eid':employee_ID, })

    else:
	return HttpResponse("Invalid Request")

def bbstatus(request):
    sql="select * from Blood_Inventory;"
    cursor = connection.cursor()
    cursor.execute(sql)
    row=cursor.fetchall()
    print(row)
    cursor.close()
    l=[]
    for x in row:
	l.append(list(x))
    return render(request, 'bloodbank/bbstatus.html', {'row':l, })

def withdraw(request):
    return render(request,'bloodbank/withdraw.html')

def withdrawal(request):
    if(request.POST):
	
	quantity = request.POST.get('quantity')
	blood_group = request.POST.get('blood_group')
	sql1 = "select quantity from Blood_Inventory where blood_group=(%s);"
	cursor=connection.cursor()
	cursor.execute(sql1, [blood_group])
	orig=cursor.fetchall()[0][0]
	orig=float(orig)
	newq = orig - float(quantity)
	if newq<0.00:
		return render(request,'bloodbank/withdraw.html', {'error':'Insufficient quantity: Cannot make this withdrawal'})
	newq = str(newq)
	sql2 = "UPDATE Blood_Inventory set quantity=(%s) where blood_group=(%s);"	
	cursor = connection.cursor()
	cursor.execute(sql2, [newq,blood_group])
	cursor.close()
	return render(request, 'bloodbank/wsucc.html', {'blood_group':blood_group, 'quantity':quantity, })
    else:
	return HttpResponse("Invalid Request")     

def hist(request):
    return render(request, 'bloodbank/hist.html')

def histdisplay(request):
    if(request.POST):
	blood_group = request.POST.get('blood_group')
	sql1 = "select donor_ID,last_donation from donate_info where blood_group=(%s);"
	try:
		cursor=connection.cursor()
		cursor.execute(sql1, [blood_group])
		row = cursor.fetchall()
	except:
		return render(request, 'bloodbank/hist.html', {error:'No history of donations for this blood group'})
	print(row)
	cursor.close()
	l=[]
	for x in row:
		l.append(list(x))
	return render(request, 'bloodbank/histsucc.html', {'blood_group':blood_group, 'row':l, })
    else:
	return HttpResponse("Invalid Request") 

def equipstatus(request):
    sql="select * from Equipment;"
    cursor = connection.cursor()
    cursor.execute(sql)
    row=cursor.fetchall()
    print(row)
    cursor.close()
    l=[]
    for x in row:
	l.append(list(x))
    return render(request, 'bloodbank/equipstatus.html', {'row':l, })

def empnew(request):
    template = loader.get_template('bloodbank/empnew.html')
    return render(request, 'bloodbank/empnew.html')

def empnewauth(request):
    if(request.POST):
	password = request.POST.get('password')
    	if(password=='admin123'):
	    return render(request, 'bloodbank/empnewsignup.html')
	else:
	    return render(request, 'bloodbank/empnew.html', {'error':"Incorrect Password",})
    else:
	return HttpResponse("Invalid Request")

def empnewsignup(request):
    return render(request,'bloodbank/empnewsignup.html')

def empregister(request):
    if(request.POST):
	employee_ID = request.POST.get('employee_ID')
	name = request.POST.get('name')
	age = request.POST.get('age')
	sex = request.POST.get('sex')
	salary = request.POST.get('salary')
	contact_no = request.POST.get('contact_no')
	email_id = request.POST.get('email_id')
	password = request.POST.get('password')
	cpassword = request.POST.get('cpassword')
	if(not re.match(r'E?[0-9].',employee_ID)):
	    errorid = "Invalid Employee ID. Please enter valid details, following the naming conventions for employee ID."
	    return render(request, 'bloodbank/empnewsignup.html', {'errorid':errorid, })
	if(not name.replace(' ','').isalpha()):
	    ename = "Invalid name. Please enter valid details"
	    return render(request, 'bloodbank/empnewsignup.html', {'ename':ename, })
	if(int(age)<18 or int(age)>55):
	    eage = "Invalid age - Note that the allowed employee age is from 18 upto 55 years. Please enter valid details"
	    return render(request, 'bloodbank/empnewsignup.html', {'eage':eage, })
	if(int(salary)<10000 or int(salary)>50000):
	    esal = "Please recheck the salary - It ought to range from 10000 to 50000 (per month)"
	    return render(request, 'bloodbank/empnewsignup.html', {'esal':esal, })
	if(not re.match(r'[\+]?[0-9].',contact_no)):
	    eno = "Please recheck the contact number entered"
	    return render(request, 'bloodbank/empnewsignup.html', {'eno':eno, })
	if(not re.match(r'[^@]+@[^@]+\.[^@]+',email_id)):
	    emid = "Please enter a valid Email id !!"
	    return render(request, 'bloodbank/empnewsignup.html', {'emid':emid, })
	if(password!=cpassword):
	    epass = "Inavlid password confirmation. Try Again"
	    return render(request, 'bloodbank/empnewsignup.html', {'epass':epass, })
    	
	user = User.objects.create_user(employee_ID,employee_ID,password)
	user.save()
	
	sql="INSERT INTO Employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
	try:
		cursor = connection.cursor()
		cursor.execute(sql, [employee_ID, name, age, sex, str(datetime.now())[:10], salary, contact_no, email_id, password])	
	except Exception as e:
		print(e)				
	finally:
		cursor.close()
	return render(request, 'bloodbank/succempsignup.html', {'ename':name, })
    else:
	return HttpResponse("Invalid Request")



def emplogauth(request):
    if(request.POST):
	employee_ID = request.POST.get('employee_ID')
	password = request.POST.get('password')
	if employee_ID[0]!='E':
		return render(request, 'bloodbank/emplogin.html', {'error':"Invalid credentials."})
	user = auth.authenticate(username=employee_ID,password=password)
	
	if user is not None:
		auth.login(request,user)
		eid = str(request.user.email)
		print('eid is', eid)
		sql = "SELECT * from Employee where employee_ID=(%s);"
		try:
	    		cursor = connection.cursor()
	    		cursor.execute(sql, [eid])
		except Exception as e:
	    		return render(request, 'bloodbank/emplogin.html', {'emsg':str(e)})
		row=cursor.fetchall()
		
		return render(request, 'bloodbank/empdash.html', {'ename':row[0][1], 'empid':eid, })
	else:
		return render(request, 'bloodbank/emplogin.html', {'error':"Invalid credentials."})
    else:
	return HttpResponse("Invalid Request")

def emplogout(request):
    auth.logout(request)
    
    return render(request, 'bloodbank/home.html')

def empdash(request):
    eid = request.user.email
    s = "select name from Employee where employee_ID=(%s);"
    cursor = connection.cursor()
    cursor.execute(s, [eid])
    ename = cursor.fetchall()[0][0]
    return render(request, 'bloodbank/empdash.html', {'ename':ename, 'empid':eid, })

def eprofile(request):
    eid = request.user.email
    sql = "SELECT * from Employee where employee_ID=(%s);"
    cursor = connection.cursor()
    cursor.execute(sql, [eid])
    row=cursor.fetchall()
    row=row[0]
    return render(request, 'bloodbank/eprofile.html', {'eid':eid, 'name':row[1], 'age':row[2], 'sex':row[3], 'join_date':row[4], 'salary':row[5], 'contact_no':row[6], 'email_id':row[7]}) 
    
def empdonorlist(request):
    eid = request.user.email
    sql1="SELECT donor_ID,registration_date FROM register_info WHERE employee_ID=(%s);"
    sql2="select * from Donor where donor_ID=(%s);"
    sql3="select blood_group from donate_info where donor_ID=(%s);"
    cursor = connection.cursor()
    cursor.execute(sql1, [eid])
    row1=cursor.fetchall()
    print(row1)
    l=[]
    for r in row1:
	i=[]
	did = r[0]
	print(did)
	reg_date = r[1]
	print(reg_date)
	cursor.execute(sql2, [did])
	row2 = cursor.fetchall()[0]
	l2 = list(row2)[1:-1]
	print(l2)
	i.append(did)
	i.extend(l2)
	cursor.execute(sql3, [did])
	blood_group = cursor.fetchall()[0][0]
	i.append(blood_group)
	i.append(reg_date)
	print(i)
	l.append(i)
    cursor.close()
    print('final list is ',l)
    return render(request,'bloodbank/empdonorlist.html',{'eid':eid, 'row':l, })

def donorsignup(request):
    
    return render(request,'bloodbank/donorsignup.html',{'eid':str(request.user.email),})

def donorregister(request):
    if(request.POST):
	
	donor_ID = request.POST.get('donor_ID')
	name = request.POST.get('name')
	age = request.POST.get('age')
	sex = request.POST.get('sex')
	address = request.POST.get('address')
	contact_no = request.POST.get('contact_no')
	email_id = request.POST.get('email_id')
	blood_group = request.POST.get('blood_group')
	employee_ID = request.user.email
	password = request.POST.get('password')
	cpassword = request.POST.get('cpassword')
	if(not re.match(r'D?[0-9].',donor_ID)):
	    errorid = "Invalid Donor ID. Please enter valid details, following the naming conventions for donor ID."
	    return render(request, 'bloodbank/donorsignup.html', {'errorid':errorid, 'eid':employee_ID, })
	if(not name.replace(' ','').isalpha()):
	    ename = "Invalid name. Please enter valid details"
	    return render(request, 'bloodbank/donorsignup.html', {'ename':ename, 'eid':employee_ID, })
	if(int(age)<18 or int(age)>65):
	    eage = "Invalid age - Note that the allowed donor age is from 18 upto 65 years. Please enter valid details"
	    return render(request, 'bloodbank/donorsignup.html', {'eage':eage, 'eid':employee_ID, })
	if(not re.match(r'[\+]?[0-9].',contact_no)):
	    eno = "Please recheck the contact number entered"
	    return render(request, 'bloodbank/donorsignup.html', {'eno':eno, 'eid':employee_ID, })
	if(not re.match(r'[^@]+@[^@]+\.[^@]+',email_id)):
	    emid = "Please enter a valid Email id !!"
	    return render(request, 'bloodbank/donorsignup.html', {'emid':emid, 'eid':employee_ID, })
	if(password!=cpassword):
	    epass = "Inavlid password confirmation. Try Again"
	    return render(request, 'bloodbank/donorsignup.html', {'epass':epass, 'eid':employee_ID, })
	user = User.objects.create_user(donor_ID,blood_group,password)
	user.save()
			
	sql1="INSERT INTO Donor VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
	sql2="INSERT INTO donate_info(donor_ID,blood_group) VALUES(%s, %s);"
	sql3="INSERT INTO register_info VALUES(%s, %s, %s);"
	try:
		cursor = connection.cursor()
		cursor.execute(sql1, [donor_ID, name, age, sex, address, contact_no, email_id, password])
		cursor.execute(sql2, [donor_ID, blood_group])
		cursor.execute(sql3, [donor_ID, employee_ID, str(datetime.now())[:10]])	
	except Exception as e:
		print (str(e))				
	finally:
		cursor.close()
	return render(request, 'bloodbank/succdonorsignup.html', {'ename':name, })
    else:
	return HttpResponse("Invalid Request")

def donorlogauth(request):
    if(request.POST):
	donor_ID = request.POST.get('donor_ID')
	password = request.POST.get('password')
	if donor_ID[0]!='D':
		return render(request, 'bloodbank/donorlogin.html', {'error':"Invalid credentials."})
	user = auth.authenticate(username=donor_ID,password=password)
	
	if user is not None:
		auth.login(request,user)
		did = str(request.user.username)
		
		sql = "SELECT * from Donor where donor_ID=(%s);"
		try:
	    		cursor = connection.cursor()
	    		cursor.execute(sql, [did])
		except Exception as e:
	    		return render(request, 'bloodbank/donorlogin.html', {'emsg':str(e)})
		row=cursor.fetchall()
		cursor.close()
		return render(request, 'bloodbank/donordash.html', {'ename':row[0][1], 'donid':did, })
	else:
		return render(request, 'bloodbank/donorlogin.html', {'error':"Invalid credentials."})
    else:
	return HttpResponse("Invalid Request")

def donorlogout(request):
    auth.logout(request)
    
    return render(request, 'bloodbank/home.html')

def donordash(request):
    sql = "SELECT * from Donor where donor_ID=(%s);"
    did = str(request.user.username)
    cursor = connection.cursor()
    cursor.execute(sql, [did])
    row=cursor.fetchall()
    cursor.close() 
    return render(request, 'bloodbank/donordash.html', {'ename':row[0][1], 'donid':did, })

def dprofile(request):
    did = request.user.username
    sql = "SELECT * from Donor where donor_ID=(%s);"
    blood = "SELECT blood_group FROM donate_info where donor_ID=(%s);"
    em = "SELECT employee_ID,registration_date FROM register_info where donor_ID=(%s);"
    cursor = connection.cursor()
    cursor.execute(sql, [did])
    row=cursor.fetchall()
    row=row[0]
    cursor.execute(blood, [did])
    blood_group=cursor.fetchall()
    print(blood_group)
    blood_group=blood_group[0][0] 
    cursor.execute(em, [did])
    r=cursor.fetchall()[0]
    employee_ID=r[0]
    print(employee_ID)
    reg_date=r[1]
    cursor.close()
    print(row)
    print(blood_group)
    print(employee_ID)
    print(reg_date)
    return render(request, 'bloodbank/dprofile.html', {'did':did, 'name':row[1], 'age':row[2], 'sex':row[3], 'address':row[4], 'contact_no':row[5], 'email_id':row[6], 'blood_group':blood_group, 'employee_ID':employee_ID, 'reg_date':reg_date})

def donate(request):
    return render(request,'bloodbank/donate.html', {'blood_group':str(request.user.email)})

def donation(request):
    if(request.POST):
	quantity = request.POST.get('quantity')
	blood_group = request.user.email
	sql1 = "select quantity from Blood_Inventory where blood_group=(%s);"
	cursor=connection.cursor()
	cursor.execute(sql1, [blood_group])
	orig=cursor.fetchall()[0][0]
	orig=float(orig)
	newq = orig + float(quantity)
	newq = str(newq)
	sql2 = "UPDATE Blood_Inventory set quantity=(%s) where blood_group=(%s);"	
	cursor = connection.cursor()
	cursor.execute(sql2, [newq,blood_group])
	sql3 = "update donate_info set last_donation=(%s) where blood_group=(%s) and donor_ID=(%s);"
	cursor = connection.cursor()
	cursor.execute(sql3, [str(datetime.now())[:10],blood_group,str(request.user.username)])
	cursor.close()
	return render(request, 'bloodbank/donsuccess.html', {'blood_group':blood_group, 'quantity':quantity, })
    else:
	return HttpResponse("Invalid Request")
