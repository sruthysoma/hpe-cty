from flask import Flask, request, render_template, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
import pdf_reader_to_upload

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("cty.html")

@app.route("/uploadFile", methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('./uploadedFiles/'+secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route("/viewUploaded/<filename>")
def viewUploaded(filename):
    uploads = os.path.join(current_app.root_path, "uploadedFiles")
    print("\n",uploads, filename)
    return send_from_directory(directory=uploads, path = filename)


@app.route("/submitFile/<os>", methods = ['GET', 'POST'])
def submit_file(os):
    if(request.method == "POST"):
        # print(os)
        f = request.files['file']
        if(os == "Windows 10 - 1809"):
            # lst_spec = ['Microsoft Windows 10-1809','Microsoft Windows 10 - 1809',  "Windows 10", "Microsoft Windows 10", "Microsoft Windows10", "Win10"]
            lst_spec = "10"
        elif( os == "Windows 2019"):
        #    lst_spec =  ['Microsoft Windows 2019','Microsoft 2019','Windows Server 2019','Windows 2019','Server 2019', 'Win2019 x64', 'Win2019', 'Win2019 x32']  
            lst_spec = "2019"
        elif( os == "Windows 2016"):
            #lst_spec =  ['Microsoft Windows 2016','Microsoft 2016','Windows Server 2016','Windows 2016','Server 2016', 'Win2016 x64', 'Win2016', 'Win2016 x32'] 
            lst_spec = "2016"
        elif( os == "Windows 2012R2"):
            #lst_spec =  ['Microsoft Windows 2012R2','Microsoft 2012R2','Windows Server 2012R2','Windows 2012R2','Server 2012R2', 'Win2012R2 x64', 'Win2012R2', 'Win2012R2 x32'] 
            lst_spec = "2012R2"
        elif(os == "Windows 2012"):
            #lst_spec =  ['Microsoft Windows 2012','Microsoft 2012','Windows Server 2012','Windows 2012','Server 2012', 'Win2012 x64', 'Win2012', 'Win2012 x32'] 
            lst_spec = "2012"
        pdf_reader_to_upload.main(secure_filename(f.filename), lst_spec)
        return f.filename.split(".")[0]

@app.route("/download/<filename>")
def downloadProcessed(filename):
    download_from = os.getcwd()
    return send_from_directory(directory = download_from, path = filename)



if __name__ =='__main__':
    app.run(debug=True)