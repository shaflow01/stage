from curses import flash
from types import NoneType
from flask import Flask, render_template, send_from_directory
from web3 import Web3, HTTPProvider
import json
import os
from eth_account import Account
from gevent import pywsgi

app = Flask(__name__)
w3 = Web3(HTTPProvider(ETH_PROVIDER))


contractAddress = "0x49D80B38E0BF21611AF2CF93A404A4DCF1A24FD2"
contractAddress = w3.to_checksum_address(contractAddress)


@app.route("/")
def index():
    return render_template("Demo.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/source")
def getSource():
    global content
    with open("contract.txt", "r") as f:
        content = f.read()
    return render_template("index.html", content=content)


@app.route("/<address>")
def check(address):
    abi = """[
	{
		"inputs": [],
		"name": "stage1",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_guess",
				"type": "uint256"
			}
		],
		"name": "stage2",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "check",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "isStage1Completed",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""
    contract_instance = w3.eth.contract(address=contractAddress, abi=abi)
    isComplete = True
    address = w3.to_checksum_address(address)

    if contract_instance.functions.check(address).call() == isComplete:
        flag = "SYC{Privt3_bs1_n1#_4f3}"
        return render_template("index.html", content=flag)
    else:
        message = "you have not solved the challege,try again"
        return render_template("index.html", content=message)


# app.run(host='0.0.0.0',port='8080')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
