from flask import Flask, render_template, request
import json
from make_abi import read_go_file
from config import name_contract, channel_name, source_path_contract, net_json
from deploy_contr import deploy_contr

app = Flask(__name__)



@app.route("/")
def index():
    func_json = read_go_file(name_contract)
    users_orgs = read_users()
    return render_template("index.html", func_json = func_json, users_orgs = users_orgs)

@app.route("/deploy", methods =["POST"])
def deploy():
    res = deploy_contr(channel_name,name_contract,source_path_contract,net_json)
    func_json = read_go_file(name_contract)
    if not res:
        return render_template("index.html", func_json = func_json)
    else:
        return render_template("index.html", func_json = func_json, contr_name = res)

@app.route("/transact", methods =["POST"])
def transact():
    func_json = read_go_file(name_contract)
    inp_d = {}
    inp = []
    name_func = request.form.get('name_func')
    for i in range(len(func_json)):
        if name_func == func_json[i]["name"]:
            inp_d = func_json[i]["inputs"]
            break
    for i in inp_d:
        inp.append(request.form.get(i["name"]))
    
    print(name_func, inp)
    
    
    return render_template("index.html", func_json = func_json)


if __name__ == "__main__":
    app.run(debug=True)
