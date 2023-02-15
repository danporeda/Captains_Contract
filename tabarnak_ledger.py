import os
import json
from web3 import Web3
from pathlib import Path
import streamlit as st
import pandas as pd


w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
@st.cache(allow_output_mutation=True)

def load_contract():

    with open(Path('./contracts/compiled/tabarnak_abi.json')) as f:
        _abi = json.load(f)

    contract_address = "0x99E34Ff861309D03E1eA071B31573F72503f42A0"

    contract = w3.eth.contract(
        address = contract_address,
        abi = _abi
    )

    return contract

contract = load_contract()
owner = "0x631f6202CbCe5A9AaEa883B66D3027CCf009a200"

################################################

st.title("Tabarnak team ledger")

st.sidebar.write("# Tabarnak Roster")
ft_df = pd.DataFrame(columns=["Name","Status","Paid"])
pt_df = pd.DataFrame(columns=["Name","Status","Paid"])
sub_df = pd.DataFrame(columns=["Name","Status","Paid"])
player_list = []
sub_list = []

st.markdown("## Register Player")

name = st.text_input("Player Name")
status = st.selectbox("Status", options=("full time", "part time", "sub"))
pay_date = st.text_input("Date Registered")
if status != "sub":
    amount = st.text_input("amount paid")
else:
    amount = 0

if st.button("Register Player"):
    tx_hash = contract.functions.registerPlayer(
        name,
        status,
        int(amount),
        pay_date).transact({"from":owner, "gas":1000000})

st.markdown("---")

for i in range(contract.functions.teamLength().call()):
    player = contract.functions.team(i).call()
    if player[1] == "full time":
        ft_df = ft_df.append({"Name":player[0],"Status":player[1],"Paid":player[2]}, ignore_index=True)
        player_list.append(player[0])
    elif player[1] == "part time":
        pt_df = pt_df.append({"Name":player[0],"Status":player[1],"Paid":player[2]}, ignore_index=True)
        sub_list.append(player[0])
    elif player[1] == "sub":
        sub_df = sub_df.append({"Name":player[0],"Status":player[1],"Paid":player[2]}, ignore_index=True)
        sub_list.append(player[0])

all_players = player_list + sub_list

st.markdown("## Record Game")
date = st.text_input("Date")
opponent = st.text_input("Opponent")

p_out = st.multiselect("Rostered Players out", player_list, key="players_out")

if "subs_in" not in st.session_state:
    st.session_state.subs_in = {}

sub = st.selectbox("Sub/PT Players in", sub_list) 
sub_payment = st.number_input("Amount paid", value=35)

if st.button("add sub"):
    st.session_state.subs_in[sub] = sub_payment
    st.write(st.session_state)

if st.button("Log Game"):
    subs_list = list(st.session_state.subs_in.keys())
    game_hash = contract.functions.gameRecord(
        date,
        opponent,
        str(p_out),
        str(subs_list)).transact({"from":owner, "gas":1000000})
    
    if not st.session_state.players_out == None:
        for p in st.session_state.players_out:
            for i in range(contract.functions.teamLength().call()):
                person = contract.functions.team(i).call()
                if person[0] == p:
                    p_out_hash = contract.functions.missedGame(i).transact({"from":owner, "gas":1000000})
    if not st.session_state.subs_in == None:
        for key, value in st.session_state.subs_in.items():
            for i in range(contract.functions.teamLength().call()):
                person = contract.functions.team(i).call()
                if person[0] == key:
                    p_sub_hash = contract.functions.subGame(key, value, i, date).transact({"from":owner, "gas":1000000})

    for key in st.session_state.keys():
        del st.session_state[key]
    
    sub_list = []
    sub_df = pd.DataFrame(columns=["Name","Status","Paid"])
    for i in range(contract.functions.teamLength().call()):
        player = contract.functions.team(i).call()
        if player[1] == "sub":    
            sub_df = sub_df.append({"Name":player[0],"Status":player[1],"Paid":player[2]}, ignore_index=True)
            sub_list.append(player[0])

sidebar_df = pd.concat([ft_df,pt_df,sub_df], ignore_index=True)
sidebar_df.reset_index()
st.sidebar.dataframe(sidebar_df)
st.sidebar.markdown("---")

league_fee = contract.functions.leagueFee().call()
team_pool = contract.functions.teamPool().call()
st.sidebar.write(f"League Fee Balance: ${league_fee}")
st.sidebar.write(f"Team Pool: ${team_pool}")

st.markdown("---")
if all_players:
    player_select = st.selectbox("View player Info", options=all_players)
    for i in range(contract.functions.teamLength().call()):
        person = contract.functions.team(i).call()
        if person[0] == player_select:
            st.write(f"Name: {person[0]}")
            st.write(f"Status: {person[1]}")
            st.write(f"Paid: ${person[2]}")
            if person[1] == "full time":
                st.write(f"Games Missed: {person[4]}")
            elif person[1] == "sub" or person[1] == "part time":
                st.write(f"Games Played: {person[3]}")


payment_filter = contract.events._Payment.createFilter(fromBlock=0)
payment_events = payment_filter.get_all_entries()
payment_df = pd.DataFrame(columns=["name", "amount", "date"])

st.markdown("---")
st.write("## Payment ledger")
if payment_events:
    for p in payment_events:
        p_event = dict(p['args'])
        payment_df = payment_df.append(p_event, ignore_index=True)
payment_df.reset_index()
st.dataframe(payment_df)

st.markdown("---")
st.write("## Game Record")
game_df = pd.DataFrame(columns=["Date","Opponent","Players Out","Subs In"])
for i in range(contract.functions.game_list_length().call()):
    game = contract.functions.games(i).call()
    game_df = game_df.append({"Date":game[0],"Opponent":game[1],"Players Out":game[2],"Subs In":game[3]}, ignore_index=True)
game_df.reset_index()
st.dataframe(game_df)

if st.button("whole team"):
    for i in range(contract.functions.teamLength().call()):
        player = contract.functions.team(i).call()
        st.write(player)


