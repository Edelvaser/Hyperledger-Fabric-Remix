import asyncio
from hfc.fabric import Client
from hfc.fabric.lifecycle import Lifecycle
from config import channel_name, contr_name, source_path_contract, net_json
import json

def deploy_contr(channel_name, contr_name, source_path_contract, net_json, bool_init=True, args=["a"]):
    try:
        with open("deploy_history/history_" + contr_name, "r") as fp:
            num = fp.read()
    except:
        with open("deploy_history/history_" + contr_name, "w") as fp:
            num = "0"
            fp.write(num)

    with open("deploy_history/history_" + contr_name, "w") as fp:
        try:
            fp.write(str(int(num) + 1))
        except:
            fp.write("1")
    contr_name += num

    loop = asyncio.get_event_loop()
    cli = Client(net_profile=net_json)
    org1_admin = cli.get_user('org1.example.com', 'Admin')
    org2_admin = cli.get_user('org2.example.com', 'Admin')
    org3_admin = cli.get_user('org3.example.com', 'Admin')
    chaincode = Lifecycle(cli, cc_name=contr_name)
    cli.new_channel(channel_name)

    import os
    gopath_bak = os.environ.get('GOPATH', '')
    gopath = os.path.normpath(os.path.join(
                        os.path.dirname(os.path.realpath('__file__')),
                        'fabric-sdk-py/test/fixtures/chaincode'
                        ))
    os.environ['GOPATH'] = os.path.abspath(gopath)
    try:
        package = chaincode.package(
            source_path = source_path_contract,
            label = contr_name
        )
        # print(package)
        pack_id1 = loop.run_until_complete(chaincode.install(
            requestor = org1_admin, 
            peers = ['peer0.org1.example.com'], 
            packaged_cc = package
        ))
        print(pack_id1)
        pack_id2 = loop.run_until_complete(chaincode.install(
            requestor = org2_admin, 
            peers = ['peer0.org2.example.com'], 
            packaged_cc = package
        ))
        print(pack_id2)

        # pack_id3 = loop.run_until_complete(chaincode.install(
        #     requestor = org3_admin, 
        #     peers = ['peer0.org3.example.com'], 
        #     packaged_cc = package
        # ))
        # print(pack_id3)

        resp = loop.run_until_complete(chaincode.approve_for_my_org(
            requestor = org1_admin, 
            peers = ['peer0.org1.example.com'], 
            channel = channel_name, 
            cc_version = "1", 
            package_id = pack_id1[0]['packageId'], 
            init_required=False, 
            sequence=1
        ))
        print(resp)

        resp = loop.run_until_complete(chaincode.approve_for_my_org(
            requestor = org2_admin, 
            peers = ['peer0.org2.example.com'], 
            channel = channel_name, 
            cc_version = "1", 
            package_id = pack_id2[0]['packageId'],
            init_required=False, 
            sequence=1
        ))
        print(resp)

        # resp = loop.run_until_complete(chaincode.approve_for_my_org(
        #     requestor = org3_admin, 
        #     peers = ['peer0.org3.example.com'], 
        #     channel = channel_name, 
        #     cc_version = "1", 
        #     package_id = pack_id3[0]['packageId'], 
        #     init_required=False, 
        #     sequence=1
        # ))
        # print(resp)

        resp = loop.run_until_complete(chaincode.commit_definition(
            requestor = org1_admin, 
            peers = ['peer0.org1.example.com'], 
            channel = channel_name, 
            cc_version = "1",
            init_required=False, 
            sequence=1
            # ,collections_config=politic
        ))
        print(resp)
        if bool_init:
            response = loop.run_until_complete(cli.chaincode_invoke(
                        requestor=org1_admin,
                        channel_name=channel_name,
                        peers=['peer0.org1.example.com'],
                        args=args,
                        cc_name=contr_name,
                        fcn='Init'))
            print(response)
        return (contr_name)
    except Exception as e:
        print(e)
        return False
    
