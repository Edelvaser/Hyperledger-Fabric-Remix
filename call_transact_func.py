import asyncio
from hfc.fabric import Client
import os

from deploy_contr import deploy_contr
from config import channel_name, contr_name, net_json, s_p_contr_UserId

loop = asyncio.get_event_loop()
cli = Client(net_profile = net_json)
org1_admin = cli.get_user('org1.example.com', 'Admin')
org2_admin = cli.get_user('org2.example.com', 'Admin')
org3_admin = cli.get_user('org3.example.com', 'Admin')
cli.new_channel(channel_name)

def transact(user, peers, fcn, args):
    global contr_name, channel_name
    try:
        with open("deploy_history/history_" + contr_name, "r") as fp:
            num = fp.read()
    except:
        print("Please, deploy contract")
        return False
    c_name = contr_name + num
    try:
        response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=user,
                channel_name=channel_name,
                peers=[peers],
                args=args,
                fcn = fcn,
                cc_name= c_name,
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
        print(response)
        return response
    except Exception as e: 
        print(e)
        return False


def read_users(path_org):
    global contr_name, channel_name, s_p_contr_UserId
    try:
        with open("deploy_history/history_" + contr_name, "r") as fp:
            num = fp.read()
    except:
        print("Please, deploy contract")
        return False
    c_name = contr_name + num
    deploy_contr(channel_name, c_name, s_p_contr_UserId, net_json)
    
    try:
        response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=user,
                channel_name=channel_name,
                peers=[peers],
                args=args,
                fcn = "invoke",
                cc_name= c_name,
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
        print(response)
        return response
    except Exception as e: 
        print(e)
        return False

