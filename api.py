from flask import *
from database import *
import uuid
from datetime import datetime
from date1 import *


api=Blueprint("api",__name__)



        
@api.route("/user_home",methods=['get','post'])
def user_home():
        
    return render_template('user_home.html')


from voice import *
@api.route("/chat",methods=['get','post'])
def chat():
    """Render chat page and handle chat messages"""
    if request.method == 'POST':
        # Get the message from the user
        user_message = request.form.get("user_message")
        role = request.form.get("role")
        
        # Get the model's response
        answer = get_answer(user_message, role)
        
        # Return the answer as a JSON response
        return jsonify({"answer": answer})
    
    # For GET request, render the chat page
    return render_template('chat.html')





        
@api.route("/userreg",methods=['get','post'])
def userreg():
        
    if  'add' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        username=request.form['username']
        pwd=request.form['pass']

        qry="insert into login values(null,'%s','%s','user')"%(username,pwd)
        print(qry)
        id=insert(qry)

        qry1="insert into user values(null,'%s','%s','%s','%s')"%(id,fname,lname,place)
        res=insert(qry1)
        print(res)


        if res:
                return render_template_string(
                    "<script>alert('Registration successful'); window.location='/';</script>"
                )

    return render_template('user_registration.html')
    



    

@api.route('/viewdisease')
def viewdisease():

    data={}

    qry="select * from disease"
    res=select(qry)
    data['view']=res
    print(res)


    return render_template('user_viewdisease.html',data=data)


@api.route('/viewdsymptoms')
def viewdsymptoms():
    data={}
    diseaseid=request.args['diseaseid']
    qry="select * from symptoms where disease_id='%s'"%(diseaseid)
    res=select(qry)
    data['view']=res

    return render_template('user_viewsymptoms.html',data=data)

@api.route('/viewdmedicine')
def viewdmedicine():
    data={}
    diseaseid=request.args['diseaseid']

    qry="select * from medicine where disease_id='%s'"%(diseaseid)
    res=select(qry)
    data['view']=res
    print(res)


    return render_template('user_viewmedicine.html',data=data)

@api.route('/sendenquiry',methods=['get','post'])
def usersendenquiry():
    data={}
    userid=session['user_id']
    qry="select * from enquiry where user_id='%s'"%(userid)
    res=select(qry)
    data['view']=res
    print(res)

    userid=session['user_id']

    if 'add' in request.form:

        enquiry=request.form['enquiry']
        
        qry="insert into enquiry values(null,'%s','%s','pending',curdate())"%(userid,enquiry)
        res=insert(qry)
        
        print(res)
   
    return render_template('user_enquiry.html',data=data)




@api.route('/viewdoctors')
def viewdoctors():

    data={}
    qry="select * from doctors"
    res=select(qry)
    data['view']=res
    
    return render_template('user_viewdoctors.html',data=data)



# @api.route('/user_uploads_images',methods=['POST'])
# def user_uploads_images():
#     data={}
#     path=request.files['image']
    
#     img="static/images/"+str(uuid.uuid4())+path.filename
#     path.save(img)
#     id=request.form['user_id']
#     qry="insert into uploads values(null,(select user_id from user where login_id='%s'),'%s','pending')"%(id,img)

#     up_id=insert(qry)
#     session['up_id']=up_id
#     print("up_id:",up_id)

#     out=predict(img)
#     predicted_class = out[0]
#     print("///////////",out)
#     if out==1:
#         qry1="UPDATE uploads SET `out`='%s' WHERE `uploads_id`='%s'"%(predicted_class,up_id)
#         res=update(qry1)
#     elif out==0:
#         qry2="UPDATE uploads SET `out`='%s' WHERE `uploads_id`='%s'"%(predicted_class,up_id)
#         res=update(qry2)
        
    
#     data['status']="success"
    
#     return str(data)



@api.route('/user_make_appointment',methods=['get','post'])
def user_make_appointment():
    id=session['user_id']
    doctors_id=request.args['doctors_id']
    if 'add' in request.form:
        path=request.files['image']
        img="static/appointmentimages/"+str(uuid.uuid4())+path.filename
        path.save(img)
        date=request.form['date']
        print(date)
        
        qry="insert into uploads values(null,'%s','%s','pending',now())"%(id,img)
        uploadid=insert(qry)

        qry2="insert into appointment values(null,'%s','%s','%s','%s','pending')"%(doctors_id,id,uploadid,date)
        res=insert(qry2)

        print(res) 

        return render_template_string(
        "<script>alert('appointment booked successful'); window.location='/viewappointment';</script>"
    )


    return render_template('user_make_appointment.html')


@api.route('/viewappointment')
def viewappointment():
    data={}

    id=session['user_id']

    qry= "SELECT * FROM appointment INNER JOIN  uploads USING(uploads_id)  WHERE  appointment.user_id='%s'"%(id)
    res=select(qry)
    print(res,"//////////////////////////")
    data['view']=res
   
    return render_template('user_viewappointment.html',data=data)




@api.route('/viewappointment_image')
def viewappointment_image():
    data={}

    up_id=request.args['up_id']

    qry="select * from uploads where uploads_id='%s'"%(up_id)
    res=select(qry)
    data['view']=res
    print(res)  
    return render_template('user_viewappointment_image.html',data=data)




@api.route('/viewprescription')
def viewprescription():
    data={}
    id=request.args['id']
    qry="SELECT * FROM prescription INNER JOIN appointment USING(appointment_id)  WHERE appointment_id='%s'"%(id)
    res=select(qry)
    print(res)
    data['view']=res
    return render_template('user_viewprescription.html',data=data)



@api.route('/user_add_review',methods=['get','post'])
def user_add_review():

    id=session['user_id']
    doctors_id=request.args['doctors_id']
    print(doctors_id)
    if 'add' in request.form:
        review=request.form['review']
        rating=request.form['rating']

        qry="insert into review values(null,'%s','%s','%s','%s',now())"%(id,doctors_id,review,rating)
        res=insert(qry)
        print(res)
    return render_template('user_add_review.html')





# //////////////////////////////////////////////////////////////



