from flask import Flask, session, request, url_for, redirect, render_template
import os
import time

initTime = time.time()

app = Flask(__name__)
app.secret_key = os.urandom(12)

bar = {"25": 2, "Bpetit": 6, "Bgrand": 10, "13": 2, "Vpetit": 12, "Vgrand": 20, "sodas": 1, "frites": 3, "cafe": 2}

userList = dict()


class User:
    def __init__(self, name, id, tel):
        self.name = name
        self.num = id
        self.sold = 0
        self.log = ""
        self.tel = tel


x = len(userList) + 1
userList[x] = User("Theo Manfredi", x, "0783694087")


def render(name):
    with open("templates/{}.html".format(name), "r") as f:
        return "".join(f)


@app.route("/")
def index():
    print(userList)
    return render_template('main.html', userList=userList)


@app.route("/login", methods=['POST'])
def login():
    pw = request.form.get("password")
    if pw == "yojeromE":
        session["username"] = "loginOK"
    return redirect(url_for("index"))


@app.route("/manage", methods=["GET"])
def manage():
    global initTime
    if time.time() - initTime > 60:
        saveUserList()
        initTime = time.time()
    num = request.args.get("num")
    user = userList[int(num)]
    return render_template('manage.html', user=user)


@app.route("/encaisser", methods=["GET"])
def encaisser():
    num = request.args.get("num")
    user = userList[int(num)]
    return render_template('encaisser.html', user=user)


@app.route("/encaisserValid", methods=["POST"])
def encaisserValid():
    num = request.form.get("num")
    value = request.form.get("montant")
    user = userList[int(num)]
    try:
        user.sold += int(value)
    except:
        pass
    return redirect(url_for('index'))


@app.route("/vente", methods=["GET"])
def vente():
    num = request.args.get("num")
    user = userList[int(num)]
    return render_template('vente.html', user=user)

@app.route("/historique", methods=["GET"])
def historique():
    num = request.args.get("num")
    user = userList[int(num)]
    logs = user.log.split("#")
    return render_template('historique.html', user=user, logs=logs)


@app.route("/venteValid", methods=["POST"])
def venteValid():
    num = request.form.get("num")
    user = userList[int(num)]
    total = 0
    for item in bar:
        amount = int("0" + request.form.get(item))
        if amount > 0:
            user.log += "# {} x {}".format(item, amount)
            total += bar[item] * amount
    user.sold -= total
    return redirect(url_for('index'))

def saveUserList():
    with open("save.txt" + str(int(time.time())), "w") as file:
        for id in userList:
            user = userList[id]
            file.write(str(user.num) + "#")
            file.write(user.name + "#")
            file.write(str(user.sold) + "#")
            file.write(user.log)

@app.route("/inscription", methods=["GET"])
def inscription():
    return render_template('inscription.html')

@app.route("/newUser", methods=["POST"])
def newUser():
    nom = request.form.get("nom")
    tel = request.form.get("tel")
    newId = len(userList) + 1
    userList[newId] = User(nom, newId, tel)
    return render_template('confirmUser.html', id=newId)