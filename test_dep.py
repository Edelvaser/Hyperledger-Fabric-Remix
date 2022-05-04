contr_name = "testing"

try:
    with open("deploy_history/history_" + contr_name, "r") as fp:
        num = fp.read()
except:
    with open("deploy_history/history_" + contr_name, "w") as fp:
        num = "1"
        fp.write(num)

with open("deploy_history/history_" + contr_name, "w") as fp:
    try:
        fp.write(str(int(num) + 1))
    except:
        fp.write("1")
contr_name += num
print(contr_name)