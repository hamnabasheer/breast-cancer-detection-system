import uuid
from flask import *
from database import *
import os
from cnnpredict import predict



doctor=Blueprint("doctor",__name__)

@doctor.route("/doctorhome")
def doctorshome():

    return render_template("doctorhome.html")

@doctor.route("/doctor_view_appointment",methods=['get','post'])
def doctorvirwappointment():
    data={}
    qry="SELECT * FROM USER INNER JOIN appointment USING(user_id) INNER JOIN uploads USING(uploads_id) WHERE doctors_id='%s'"%(session['did'])
    res=select(qry)
    data['view']=res
    
    return render_template("doctor_view_appointment.html",data=data)

@doctor.route('/doctor_add_prescription',methods=['get','post'])
def doctoraddprescrption():
    data={}
    qry3="select * from medicine"


    id=request.args['id']
    if 'add' in request.form:
        prescription=request.form['pre']
        medicine=request.form['med']
        qry="insert into prescription values(null,'%s','%s','%s',curdate())"%(id,prescription,medicine)
        insert(qry)
        qry2="update appointment set status='Prescription Added' where appointment_id='%s'"%(id)
        update(qry2)
        return ("<script>alert('Add successfull');window.location='/doctor_view_appointment'</script>")

    return render_template('doctor_add_prescription.html')



# @doctor.route('/doctor_add_voice_report',methods=['get','post'])
# def doctor_add_voice_report():
#     id=request.args['id']
#     audio=request.args['img']
#     if 'add' in request.form:

#         # x,y=predict_audio(audio)
#         # print(x,y,"//////////////*****************")

#         qry2 = "UPDATE uploads SET `out`='%s' WHERE uploads_id='%s'" % (id)
#         update(qry2)

#         return ("<script>alert('Add successfull');window.location='/doctorhome'</script>")

    
#     return render_template('doctor_add_voice_report.html')




# Route to handle image upload and prediction
@doctor.route('/doctor_add_image_report', methods=['GET', 'POST'])
def doctor_add_report():
    if 'add' in request.form:
        id = request.args['id']  # Get ID from the form
      
        file = request.args['img']
    
        res = predict(file)

        print(res,"''''''''//////////////////////")


        if res[0]== 0:
            result="benign"
            qry="UPDATE uploads SET `out`='%s' WHERE uploads_id='%s'"%(result,id)  
            insert(qry)
        elif res[0]== 1:
            result="Malignant"
            qry="UPDATE uploads SET `out`='%s' WHERE uploads_id='%s'"%(result,id)  
            insert(qry)
        elif res[0]== 2:
            result="Normal"
            qry="UPDATE uploads SET `out`='%s' WHERE uploads_id='%s'"%(result,id)  
            insert(qry)


        return "<script>alert('Prediction: %s');window.location='/doctor_view_appointment'</script>" % res

    return render_template('doctor_add_image_report.html')


