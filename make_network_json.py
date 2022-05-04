import os
import json
from config import path_templ_net, path_org, org_list, peer_list


def open_templ(path_templ_net):
    with open(path_templ_net) as fp:
        templ = json.load(fp)
    return templ

def make_network(path_org, path_templ_net):
    net_json = open_templ(path_templ_net)
    path_ord_cert = "ordererOrganizations/example.com/users/Admin@example.com/msp/signcerts/Admin@example.com-cert.pem"
    path_ord_adm = "ordererOrganizations/example.com/users/Admin@example.com/msp/keystore/"
    pr_k = os.listdir(path_org + path_ord_adm)
    print(pr_k)
    net_json["organizations"]["orderer.example.com"]["users"]["Admin"]["cert"] = path_org + path_ord_cert
    net_json["organizations"]["orderer.example.com"]["users"]["Admin"]["private_key"] = path_org + path_ord_adm + pr_k[0]

    tls_cert = path_org + "ordererOrganizations/example.com/orderers/orderer.example.com/tls/tlscacerts/"
    tls_name = os.listdir(tls_cert)
    net_json["orderers"]["orderer.example.com"]["tlsCACerts"]["path"] = tls_cert + tls_name[0]


    for org in org_list:
        path_orgs = "peerOrganizations/{0}.example.com/users/".format(org)
        list_user = os.listdir(path_org + path_orgs)
        for us in list_user:
            path_cert = path_org + "peerOrganizations/{0}.example.com/users/{1}/msp/signcerts/cert.pem".format(org, us)
            path_pr_k = "peerOrganizations/{0}.example.com/users/{1}/msp/keystore/".format(org, us)
            pr_k = os.listdir(path_org + path_pr_k)
            user_name = us.split("@")[0]
            net_json["organizations"][org + ".example.com"]["users"][user_name]["cert"] = path_cert
            net_json["organizations"][org + ".example.com"]["users"][user_name]["private_key"] = path_org + path_pr_k + pr_k[0]

        for peers in peer_list:
            tls_cert = path_org + "peerOrganizations/{0}.example.com/peers/{1}.{0}.example.com/tls/tlscacerts/".format(org, peers)
            tls_name = os.listdir(tls_cert)
            net_json["peers"][peers +"."+ org+ ".example.com"]["tlsCACerts"]["path"] = tls_cert + tls_name[0]

        ca_cert = path_org + "peerOrganizations/{0}.example.com/ca/".format(org)
        ca_name = os.listdir(ca_cert)
        net_json["certificateAuthorities"]["ca-" + org]["tlsCACerts"]["path"] = ca_cert + ca_name[0]


    with open("network_2.json", "w") as fp:
        json.dump(net_json, fp)
    print(net_json)

make_network(path_org, path_templ_net)
