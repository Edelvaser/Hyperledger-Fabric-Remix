from copy import copy
import json
from pickletools import read_uint1
from unicodedata import name
from config import ex_inp_out, example_func

def make_dict(name_f, inputs, outputs):
    temp_func = dict.copy(example_func)
    temp_func["name"] = name_f
    temp_func["inputs"] = inputs
    temp_func["outputs"] = outputs
    temp_func["type"] = "functions"
    return temp_func

def read_go_file2(name_f):
    func = []
    with open (name_f) as fp:
        while True:
            kod = fp.readline()
            if not kod:
                break
            if kod.find("func ") > -1 and kod.find("main") < 0:
                func.append(kod)
    # print(func)
    for f in func:
        ff = f.replace("("," ")
        ff = ff.replace(")"," ")
        ff = ff.replace(",","")
        ff = ff.split()
        ff.remove("func")
        ff.remove("ctx")
        ff.pop(0)
        ff.pop(0)
        for k in range(len(ff)):
            ind = ff[k].find("contractapi.TransactionContextInterface")
            if ind > -1:
                ff.pop(k)
                break
        try:
            ff.remove("{")
        except:
            pass
        print(ff)


def read_name_func(stroka):
    start = stroka.find(")") + 1
    end = stroka.find("(", start)
    name_func = stroka[start:end]
    name_func = name_func.replace(" ", "")
    return name_func, end+1

def read_input(stroka, start):
    end = stroka.find(")", start)
    inp = stroka[start:end]
    inp = inp.replace("ctx contractapi.TransactionContextInterface", "")
    inp = inp.replace(",", "")
    inp = inp.split()
    if inp == []:
        return [], end + 1
    i = 0
    inputs = []
    while i < len(inp):
        if inp[i] not in ("string", "int", "boolean") and "[]" not in inp[i]:
            param = dict.copy(ex_inp_out)
            j = i + 1
            param["name"] = inp[i]
            while True:
                if j > len(inp) - 1:
                    break
                if inp[j] in ("string", "int", "boolean") or "[]" in inp[j]:
                    param["type"] = inp[j]
                    break
                else:
                    j += 1
            inputs.append(param)
        i += 1
    return inputs, end

def read_output(stroka, start):
    out = stroka[start:]
    out = out.replace("(", "")
    out = out.replace(")", "")
    out = out.replace(",", "")
    out = out.replace("{", "")
    out = out.split()
    outputs = []
    for o in out:
        temp_out = dict.copy(ex_inp_out)
        temp_out["name"] = ""
        temp_out["type"] = o
        outputs.append(temp_out)
    return outputs

def read_go_file(name_file):
    func = []
    abi = []
    with open (name_file) as fp:
        while True:
            kod = fp.readline()
            if not kod:
                break
            if kod.find("func ") > -1 and kod.find("main") < 0:
                func.append(kod)
    for f in func:
        name_f, end = read_name_func(f)
        inputs, end = read_input(f, end)
        outputs = read_output(f, end)
        dict_func = make_dict(name_f, inputs, outputs)
        abi.append(dict_func)
    with open(name_file + "_abi.json", "w") as fp:
        json.dump(abi, fp)
    return abi


if __name__ == "__main__":
    abi = read_go_file("abstore.go")
    print(abi)