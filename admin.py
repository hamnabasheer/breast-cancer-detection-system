from flask import *

from database  import *

admin=Blueprint("admin",__name__)



@admin.route("/adminhome",methods=['get','post'])
def adminhome():
    return render_template("adminhome.html")


@admin.route("/adm_view_user",methods=['get','post'])
def adm_view_user():
    data={}
    z="select * from user"
    data['view']=select(z)
    return render_template("adm_view_users.html",data=data)


@admin.route("/adm_view_doc",methods=['get','post'])
def adm_view_doc():
    data={}
    z="select * from doctors inner join login using(login_id)"
    data['view']=select(z)

    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
    
    else:
        act=None
    
    if act=='accept':
        x="update login set usertype='doctor' where login_id='%s'"%(id)
        update(x)
        return """<script>alert('Accepted');window.location="/adm_view_doc"</script>"""
    if act=='reject':
        x="update login set usertype='reject' where login_id='%s'"%(id)
        update(x)
        return """<script>alert('Rejected');window.location="/adm_view_doc"</script>"""
    return render_template("adm_view_doc.html",data=data)


@admin.route("/managedisease",methods=['get','post'])
def managedisease():
    if 'sub' in request.form:
        disease=request.form['des']
        qry="insert into disease values(null,'%s')"%(disease)
        insert(qry)
        return ("<script>alert('Add successfull');window.location='/managedisease'</script>")
    
    data={}
    qry1="select * from disease"
    res=select(qry1)
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None

    if action=='delete':
        qry2="delete from disease where disease_id='%s'"%(id)
        delete(qry2)
        return ("<script>alert('Delete successfull');window.location='/managedisease'</script>")
    if action=='update':
        data={}
        qry3="select * from disease where disease_id='%s'"%(id)
        res=select(qry3)
        data['up']=res

    if 'up' in request.form:
        disease=request.form['des']
        qry="update disease set disease='%s' where disease_id='%s' "%(disease,id)
        update(qry)
        return ("<script>alert('update successfull');window.location='/managedisease'</script>")

    return render_template("admin_managedisease.html",data=data)




@admin.route("/managesymptoms",methods=['get','post'])
def managesymptoms():
    if 'id' in request.args:
        id=request.args['id']
    data={}
    qry1="select * from symptoms where disease_id='%s'"%(id)
    res=select(qry1)
    data['view']=res

    if 'sub' in request.form:
        symptoms=request.form['des']
        qry="insert into symptoms values(null,'%s','%s')"%(id,symptoms)
        insert(qry)
        return ("<script>alert('Add successfull');window.location='/managedisease'</script>")
  
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None

    if action=='delete':
        qry2="delete from symptoms where symptoms_id='%s'"%(id)
        delete(qry2)
        return ("<script>alert('Delete successfull');window.location='/managedisease'</script>")
    if action=='update':
        data={}
        qry3="select * from symptoms where symptoms_id='%s'"%(id)
        res=select(qry3)
        data['up']=res

    if 'up' in request.form:
        symptoms=request.form['des']
        qry="update symptoms set symptoms='%s' where symptoms_id='%s'"%(symptoms,id)
        update(qry)
        return ("<script>alert('update successfull');window.location='/managedisease'</script>")

    return render_template("admin_managesymptoms.html",data=data)



@admin.route("/managemedicine",methods=['get','post'])
def managemedicine():
    if 'id' in request.args:
        id=request.args['id']
    data={}
    qry1="select * from medicine where disease_id='%s'"%(id)
    res=select(qry1)
    data['view']=res

    if 'sub' in request.form:
        age=request.form['age']
        medicine=request.form['des']
        qry="insert into medicine values(null,'%s','%s','%s')"%(id,age,medicine)
        insert(qry)
        return ("<script>alert('Add successfull');window.location='/managedisease'</script>")
  
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None

    if action=='delete':
        qry2="delete from medicine where medicine_id='%s'"%(id)
        delete(qry2)
        return ("<script>alert('Delete successfull');window.location='/managedisease'</script>")
    if action=='update':
        data={}
        qry3="select * from medicine where medicine_id='%s'"%(id)
        res=select(qry3)
        data['up']=res

    if 'up' in request.form:
        medicine=request.form['des']
        age=request.form['age']
        qry="update medicine set  age='%s', medicine='%s'  where medicine_id='%s'"%(age,medicine,id)
        update(qry)
        return ("<script>alert('update successfull');window.location='/managedisease'</script>")

    return render_template("admin_managemedicine.html",data=data)



@admin.route("/adminviewenquiry",methods=['get','post'])
def adminviewenquiry():
    data={}
    qry="select * from enquiry inner join user using(user_id)"
    res=select(qry)
    data['view']=res

    return render_template("admin_view_enquiry.html",data=data)

@admin.route("/adminsendenquiry",methods=['get','post'])
def adminsendenquiry():
    id=request.args['id']
    if 'sed' in request.form:
        reply=request.form['reply']
        qry="update enquiry set reply='%s' where enquiry_id='%s'"%(reply,id)
        update(qry)
        return ("<script>alert('Send successfull');window.location='/adminviewenquiry'</script>")
 
    return render_template("admin_send_enquiryreply.html")




@admin.route("/admin_view_uploads",methods=['get','post'])
def adminviewuploads():
    data={}
    qry="select * from uploads inner join user using (user_id)" 
    res=select(qry)
    data['view']=res
    
    return render_template("admin_view_uploads.html",data=data)