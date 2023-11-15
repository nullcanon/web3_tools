from pywebio.input import input, FLOAT, NUMBER, input_group, select
from pywebio.output import put_text, put_table, use_scope, put_buttons,clear,popup
import batch_job, generate_address 
from utils import wallet, web3, config
from functools import partial

global_dict = {}

def chack_input_config(btn_val):
    data = input_group("配置输入",[
        input('输入主地址：', name='address'),
        input('输入主私钥', name='privatekey'),
        input('输入网络链接', name='rpc')
    ])

    rpc = data['rpc']
    user_address = data['address']
    global_dict['user_address'] = user_address

    user_privite = data['privatekey']

    w3 = web3.build_web3(rpc)
    global_dict['w3'] = w3
    user_wallet = wallet.Wallet(w3, user_address, user_privite)
    global_dict['user_wallet'] = user_wallet

    clear('A')
    with use_scope('A'):
        put_table([
            ['配置选项',put_buttons(['修改配置'],onclick=chack_input_config)],
            ['主地址', user_address],
            ['网   络', rpc],
            ['链   ID', user_wallet.chainID()],
        ])


def check_wallet_event(btn_val):
    if btn_val == '批量导入钱包私钥':
        pass
    if btn_val == '批量生成钱包私钥':
        number = input('输入地址数量', type=NUMBER)
        check_generate_address(number)

def check_generate_address(numbers):
    address_file_name, mnemonic, wallets = batch_job.generate_wallets_batch(numbers)
    global_dict['address_file_name'] = address_file_name
    addresses_table = [[] for i in range(len(wallets) + 1)]
    addresses_table[0].append("子地址")
    for i in range(len(wallets)):
        addresses_table[i + 1].append(wallets[i][0])
    clear('B')
    with use_scope('B'):
        put_text('子地址私钥文件： ' + address_file_name)
        put_table(addresses_table)


def by_pass(btn_val):
    pass




def check_send_and_recive_batch(btn_val):
    coin_type = select('选择币种类型',['主币','代币'])
    if btn_val == '批量分发':
        address_type = select('选择币种类型',['子地址','手动输入'])

        if coin_type == '主币':
            send_amount = input('输入每个地址分发的数量：', type=FLOAT)
            # TODO 检查余额
            if address_type == '子地址':
                batch_job.send_eth_bath('./files/' + global_dict['address_file_name'], global_dict['user_wallet'], send_amount)
            if address_type == '手动输入':
                pass

        if coin_type == '代币':
            data = input_group("输入代币合约地址和每个地址分发的数量",[
                input('代币合约地址', name='contract_address'),
                input('每个地址发送数量', name='amount'),
            ])
    
    if btn_val == '一键归集':
        if coin_type == '主币':
            batch_job.recive_eth_batch(global_dict['w3'], './files/' + global_dict['address_file_name'], global_dict['user_address'])

        if coin_type == '代币':
            contract_address = input('合约地址')

def check_token_approve_batch(btn_val):
    pass

        

chack_input_config('输入配置')

put_buttons(['批量导入钱包私钥', '批量生成钱包私钥'],onclick=check_wallet_event)

with use_scope('C'):
    put_buttons([ '批量分发', '一键归集'],onclick=check_send_and_recive_batch)

put_buttons(['代币批量授权'],onclick=check_token_approve_batch)




# put_buttons(['分发 eth'],onclick=partial(edit_row, row=1))
# put_buttons(['分发 erc20'],onclick=partial(edit_row, row=1))
# put_buttons(['归集 eth'],onclick=partial(edit_row, row=1))
# put_buttons(['归集 erc20'],onclick=partial(edit_row, row=1))