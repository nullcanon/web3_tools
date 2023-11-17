from pywebio.input import input, FLOAT, NUMBER, URL, input_group, select,actions,TEXT
from pywebio.output import put_text, put_table, use_scope, put_buttons,clear,popup,close_popup,put_row,put_column,put_code
import batch_job 
from utils import wallet, web3, config
from functools import partial
from contract import erc20, uniswapv2
import numpy as np
from decimal import Decimal

global_dict = {}
global_dict['config_flag'] = False
global_dict['wallets_flag'] = False
global_dict['main_addresses_table'] = None


def chack_input_config(btn_val):
    data = input_group("配置输入",[
        input('输入主地址：', name='address'),
        input('输入主私钥', name='privatekey'),
        input('输入网络链接', name='rpc', type= URL)
    ], cancelable = True)

    if data == None:
        return
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

def flush_address_table(addresses_table):
    global_dict['addresses_table'] = addresses_table

    with use_scope('B'):
        clear('B-2')
        with use_scope('B-2'):
            put_table(addresses_table)

def flush_main_address_table(main_addresses_table):
    global_dict['main_addresses_table'] = main_addresses_table
    with use_scope('B'):
        clear('B-1')
        with use_scope('B-1'):
            put_table(main_addresses_table)

def check_generate_address(numbers):
    address_file_name, mnemonic, wallets = batch_job.generate_wallets_batch(numbers)
    global_dict['address_file_name'] = address_file_name
    addresses_table = [[] for i in range(len(wallets) + 1)]
    addresses_table[0].append("子地址")
    for i in range(len(wallets)):
        addresses_table[i + 1].append(wallets[i][0])
    put_text('子地址私钥文件： ' + address_file_name)
    flush_address_table(addresses_table)
    
    global_dict['wallets_flag'] = True
    global_dict['addresses_table'] = addresses_table


def by_pass(btn_val):
    pass


def check_config_flag():
    if global_dict['config_flag'] == False:
        popup('提示', [
            put_text('请先输入配置'),
            put_buttons(['朕知道了'], onclick=lambda _: close_popup())
        ])
        return False
    return True

def check_wallets_flag():
    if global_dict['wallets_flag'] == False:
        popup('提示', [
            put_text('请先批量导入或者生成钱包'),
            put_buttons(['朕知道了'], onclick=lambda _: close_popup())
        ])
        return False
    return True

def select_can_canle(label, options):
    data = input_group("",[
        select(label,options, name="name")
    ],cancelable = True)
    if data == None:
        return data
    return data["name"]

def input_can_canle(label, type = None):
    data = input_group("",[
        input(label, name='name', type = type),
    ],cancelable = True)
    if data == None:
        return data
    return data["name"]

def check_send_and_recive_batch(btn_val):
    if check_config_flag() == False:
        return

    if check_wallets_flag() == False:
        return

    coin_type = select_can_canle('选择币种类型', ['主币','代币'])
    if coin_type == None:
        return
    if btn_val == '批量分发':
        address_type = select_can_canle('选择要分发的地址',['子地址','手动输入'])
        if address_type == None:
            return
        if coin_type == '主币':
            send_amount = input_can_canle('输入每个地址分发的数量：', type=FLOAT)
            if send_amount == None:
                return
            # TODO 检查余额
            if address_type == '子地址':
                batch_job.send_eth_bath('./files/' + global_dict['address_file_name'], global_dict['user_wallet'], send_amount)
            if address_type == '手动输入':
                pass

        if coin_type == '代币':
            data = input_group("输入代币合约地址和每个地址分发的数量",[
                input('代币合约地址', name='contract_address'),
                input('每个地址发送数量', name='amount', type = FLOAT),
            ], cancelable = True)
            if data == None:
                return
            # TODO check 代币合约地址
            erc20_token = erc20.ERC20(global_dict['w3'], data['contract_address'])
            amount = data['amount'] * ( 10 ** erc20_token.decimals)
            batch_job.send_erc20_batch('./files/' + global_dict['address_file_name'], erc20_token, global_dict['user_wallet'],amount)

    
    if btn_val == '一键归集':
        address_type = select_can_canle('选择要归集的地址',['主地址','手动输入'])
        if address_type == None:
            return
        recive_address = ''
        if address_type == '主地址':
            recive_address = global_dict['user_address']
        if address_type == '手动输入':
            recive_address = input_can_canle('输入归集地址：', TEXT)
            if recive_address == None:
                return

        if coin_type == '主币':
            batch_job.recive_eth_batch(global_dict['w3'], './files/' + global_dict['address_file_name'], recive_address)

        if coin_type == '代币':
            contract_address = input_can_canle('合约地址', TEXT)
            if contract_address == None:
                return
            erc20_token = erc20.ERC20(global_dict['w3'], contract_address)
            batch_job.recive_erc20_batch(global_dict['w3'],'./files/' + global_dict['address_file_name'], erc20_token, recive_address)


UINT256_MAX = 2**256-1
def check_token_approve_batch(btn_val):
    if check_config_flag() == False:
        return

    if check_wallets_flag() == False:
        return

    data = input_group("输入被授权地址和数量",[
        input('授权代币', name='tonken_address'),
        input('被授权地址', name='spender_address'),
        input('授权数量', name='amount', type = NUMBER, value = str(UINT256_MAX)),
    ], cancelable = True)
    if data == None:
        return
    erc20_token = erc20.ERC20(global_dict['w3'], data['tonken_address'])
    approve_amount = int(Decimal(data['amount']).to_integral_value()) - 1
    batch_job.erc20_approve_batch(
        global_dict['w3'], './files/' + global_dict['address_file_name'], erc20_token, data['spender_address'], approve_amount)

def check_config_buttons(btn_val):
    chack_input_config(btn_val)
    global_dict['config_flag'] = True


def check_get_balance(btn_val):
    if check_config_flag() == False:
        return

    if check_wallets_flag() == False:
        return
    balance_type = select('选择类型',['主币','代币'])
    addresses_table = global_dict['addresses_table']

    main_addresses_table = global_dict['main_addresses_table']
    if main_addresses_table == None:
        main_addresses_table = [[] for i in range(2)]
        main_addresses_table[0].append('主地址')
        main_addresses_table[1].append(global_dict['user_wallet'].address())

    if balance_type == '主币':
        tital_index = -1
        for i in range(len(main_addresses_table[0])):
            if(main_addresses_table[0][i] == '主币余额'):
                tital_index = i

        main_balance_amount = web3.get_eth_amount( global_dict['w3'], main_addresses_table[1][0])

        if tital_index == -1:
            main_addresses_table[0].append('主币余额')
            addresses_table[0].append('主币余额')
            main_addresses_table[1].append(main_balance_amount)
        else:
            main_addresses_table[1][tital_index] = main_balance_amount

        for i in range(len(addresses_table)):
            if i == 0:
                continue
            balance_amount = web3.get_eth_amount( global_dict['w3'], addresses_table[i][0])
            if tital_index == -1:
                addresses_table[i].append(balance_amount)
            else:
                addresses_table[i][tital_index] = balance_amount

    if balance_type == '代币':
        tital_index = -1
        token_address = select_can_canle('输入代币地址')
        if token_address == None:
            return
        erc20_token = erc20.ERC20(global_dict['w3'], token_address)
        tital = erc20_token.name + '余额'
        for i in range(len(main_addresses_table[0])):
            if(main_addresses_table[0][i] == tital):
                tital_index = i

        main_balance_amount = erc20_token.balanceOfDivDecimals( main_addresses_table[1][0])

        if tital_index == -1:
            main_addresses_table[0].append(tital)
            addresses_table[0].append(tital)
            main_addresses_table[1].append(main_balance_amount)
        else:
            main_addresses_table[1][tital_index] = main_balance_amount


        for i in range(len(addresses_table)):
            if i == 0:
                continue
            balance_amount = erc20_token.balanceOfDivDecimals( addresses_table[i][0])

            if tital_index == -1:
                addresses_table[i].append(balance_amount)
            else:
                addresses_table[i][tital_index] = balance_amount


    flush_address_table(addresses_table)
    flush_main_address_table(main_addresses_table)
 

        
put_buttons(['批量导入钱包私钥', '批量生成钱包私钥'],onclick=check_wallet_event)

put_buttons(['输入配置'],onclick=check_config_buttons)



with use_scope('C'):
    put_buttons([ '批量分发', '一键归集'],onclick=check_send_and_recive_batch)

put_buttons(['批量授权代币'],onclick=check_token_approve_batch)

put_buttons(['批量获取余额'],onclick=check_get_balance)


# put_row([
#     put_column([
#         put_code('A'),
#         put_row([
#             put_code('B1'), None,  # None represents the space between the output
#             put_code('B2'), None,
#             put_code('B3'),
#         ]),
#         put_code('C'),
#     ]), None,
#     put_code('D'), None,
#     put_code('E')
# ])

# a = input("sssssss", action=('Now', by_pass))
