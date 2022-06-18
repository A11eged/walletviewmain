from flask import Flask, render_template, request, url_for, redirect
import datetime
from flask_restful import Api, Resource
import json
import requests
import pandas as pd
import xlsxwriter
import openpyxl
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
from waitress import serve


application = Flask(__name__)
# api = Api(application)

#Endpoints for API
base = "http://walletview.us-east-1.elasticbeanstalk.com/"
bal = "/getBal/"
df = "/df/"
address = "0x86e7422f127dcb9b85f9426ddf3d7f22dcc4ed1a"
addresslink = "/0x86e7422f127dcb9b85f9426ddf3d7f22dcc4ed1a/"
# driver = webdriver.Chrome('C:\webdrivers\chromedriver_win32\chromedriver.exe')
addressBook = ["0x86e7422f127dcb9b85f9426ddf3d7f22dcc4ed1a", "0xFb337bfF5b37fBe227Aa965cacCBeaf7736526a2"]
address = addressBook[0]
apikey = "Y4XJDM1PCCSG3XJXMYS4HM72VKR6K6E1K1"
apilinkAcc = "http://api.etherscan.io/api?module=account&action="
apilinkTx = "http://api.etherscan.io/api?module=transaction&action=getstatus&txhash="

def getBal(address):
  balanceEndpoint = apilinkAcc + "balance&address=" + address + "&tag=latest&apikey=" + apikey
  getBalance = requests.get(balanceEndpoint)
  addrBalance = getBalance.json()
  balanceInWei = addrBalance['result']
  balanceInEth = float(balanceInWei)/1000000000000000000
  asStr = str("{0:.3f}".format(balanceInEth))
  return(asStr)

@application.route('/', methods=["POST", "GET"])
def home():
  if request.method == "POST":
    user = request.form['address']
    
    return redirect(url_for("dashboard", address=user))
  else:  
    return render_template("homepage.html", title=address)

@application.route('/dashboard/<address>')
def dashboard(address):
  balance = getBal(address)
  walletGraph = walletBalanceCSV(address)
  frequencyGraph= transactionFrequencyCSV(address)
  price = ethPrice()
  return render_template("dashpage.html", eth = price, fig1 = walletGraph, fig2 = frequencyGraph, address = address, balance = balance)


# class GetBal(Resource):
#   def get(self, address):
#     return {"balance": getBal(address)}

# api.add_resource(GetBal, "/getBal/<string:address>")

# class CSVDataframe(Resource):
#   def get(self, address):
#     return walletBalanceCSV(address)
  
# api.add_resource(CSVDataframe, "/csv/<address>")

# moved to rss
def ethPrice():
  priceEndpoint = "http://api.etherscan.io/api?module=stats&action=ethprice&apikey=" + apikey
  getPrice = requests.get(priceEndpoint)
  price = getPrice.json()['result']
  return price["ethusd"]
  
# get balance of all addresses
#takes an array/list of address and returns the balance in descending order

def getAllBal(address):
  inBal = ""
  for add in addressBook:
    inBal += add
    if add == addressBook[len(addressBook) - 1]:
      break
    inBal += ","
  balances = (apilinkAcc + "balancemulti&address=" 
    + inBal + "&tag=latest&apikey=" + apikey)
  bals = requests.get(balances).json()["result"]
  i = 1
  listballs = ""
  for each in bals:
    eachBal = int(each["balance"]) / 1000000000000000000
    listballs += ("Balance " + str(i) + ": " + str(eachBal) + "\n")
    i += 1
  return(listballs)

# moved to rss

def strtotime(str):
  t = int(str)
  ts = datetime.datetime.fromtimestamp(t)
  ts = (ts.isoformat(sep=' ', timespec='minutes'))
  return ts
#helper  
def valueWeiToEth(str):
  t = int(str)
  t = t/1000000000000000000
  return t


# get tx
#takes address to return transactions in that address
def getTx(address):
  txEndPoint = apilinkAcc + "txlist&address=" + address + "&startblock=0&endblock=99999999&page=1&offset=1000&sort=desc&apikey=" + apikey
  getTxList = requests.get(txEndPoint)
  txContent = getTxList.json()
  txResult = txContent.get("result")
  txList = []
  for tx in txResult:
    time = strtotime(tx.get('timeStamp'))
    # time = t
    blockNumber = tx.get('blockNumber')
    hash = tx.get('hash')
    fro = tx.get('from')
    to = tx.get('to')
    if fro == address:
      inOut = 1
    else:
      inOut = 0
    value = valueWeiToEth(tx.get('value'))
    contractAddress = tx.get('contractAddress')
    input = tx.get('input')
    type = tx.get('type')
    gas = tx.get('gas')
    gasUsed = tx.get('gasUsed')
    tg = int(gas) * int(gasUsed)
    #price in gwei
    #eth = tg * gwei
    # totalGas = gas * gasUsed
    traceId = tx.get('traceId')
    error = tx.get('isError')
    errCode = tx.get('errCode')    
    obj = {"blockNumber": blockNumber,"time": time, "hash": hash, "from": fro, "to": to, "inOut":inOut, "value": value, "contractAddress": contractAddress, "input": input, "gas":tg, "traceId": traceId, "error": error, "errorCode": errCode}
    txList.append(obj)
  return(txList)
  
# print(getTx(address)[0])
#takes address to return list of internal tx
def getInternalTx(address):
  internalTxEndPoint = apilinkAcc + "txlistinternal&address=" + address + "&startblock=0&endblock=99999999&page=1&offset=1000&sort=desc&apikey=" + apikey
  getInternalTxList = requests.get(internalTxEndPoint)
  internalTxContent = getInternalTxList.json()
  internalTxResult = internalTxContent.get("result")
  internalTxList = []
  interactions = []
  for tx in internalTxResult:
    t = strtotime(tx.get('timeStamp'))
    time = t
    nonce = tx.get('nonce')
    blockHash = tx.get('blockHash')
    blockNumber = tx.get('blockNumber')
    transactionIndex = tx.get('transactionIndex')
    status = tx.get('txreceipt_status')
    hash = tx.get('hash')
    fro = tx.get('from')
    to = tx.get('to')
    if to == address:
      inOut = 1
    else:
      inOut = 0
    value = valueWeiToEth(tx.get('value'))
    contractAddress = tx.get('contractAddress')
    input = tx.get('input')
    gasPrice = (tx.get('gasPrice'))
    gas = (tx.get('gas'))
    gasUsed = (tx.get('gasUsed'))
    cumulativeGasUsed = (tx.get('cumulativeGasUsed'))
    tg = int(gas) * int(gasUsed)
    # totalGas = gasPrice * gasUsed
    confirmations = tx.get('confirmations')
    traceId = tx.get('traceId')
    error = tx.get('isError')
    obj = {"blockNumber": blockNumber,"time": time, "blockHash": blockHash, "status":status, "hash": hash, "transactionIndex": transactionIndex, "confirmations": confirmations, "nonce":nonce, "from": fro, "to": to, "inOut":inOut, "value": value, "contractAddress": contractAddress, "input": input, "gasUsed": tg, "traceId": traceId, "error": error, }
    internalTxList.append(obj)
  return(internalTxList)

#takes txhash to return internal 
def tokenTransferEvents(address):

  tokenEndpoint = apilinkAcc + "tokentx&address=" + address + "&startblock=0&endblock=99999999&page=1&offset=1000&sort=desc&apikey=" + apikey
  print(tokenEndpoint)
  getfulltoken = requests.get(tokenEndpoint)
  fullTokenContent = getfulltoken.json()
  fullTokenResult = fullTokenContent.get("result")
  tokenList = []
  for tx in fullTokenResult:
    tokenList.append(tx)
  return(tokenList)


def df(address):  
  txDf = pd.DataFrame(data = getTx(address))
  internalTxDf = pd.DataFrame(data = getInternalTx(address))
  transactionMaster = pd.concat([txDf, internalTxDf], axis=0)
  transactionMaster = transactionMaster.sort_values('time',axis=0, ascending=True)
  varsforchart = transactionMaster[['time', 'value']]
  dictformat = varsforchart.to_dict()
  jsonformat = json.dumps(dictformat)
  return jsonformat

def walletBalanceCSV(address):
  txDf = pd.DataFrame(data = getTx(address))
  internalTxDf = pd.DataFrame(data = getInternalTx(address))
  transactionMaster = pd.concat([txDf, internalTxDf], axis=0)
  transactionMaster = transactionMaster.sort_values('time',axis=0, ascending=True)
  varsforchart = transactionMaster[['time', 'value']]
  # varsforchart = varsforchart[(varsforchart["value"]>0)]
  fig = px.line(varsforchart, x='time', y='value', title='Wallet View', 
            hover_data=['value'], 
            labels={
              "time": "Time",  "value": "Eth"
            },
            color_discrete_sequence=['#2ba84a'],
            template="simple_white",
            )
  fig.update_layout(width=1000, height=500,
            title_font_color="#2ba84a",
            title_font_size=20,
            autosize=True,
            font_family="Raleway",
            hoverlabel={
              'bordercolor': '#fff',
              'bgcolor': '#fff',
              'font': {
                'family': 'PT Sans Narrow',
                'color': '#2ba84a',
                'size': 14,
              },
            },
            title={
              'y':0.9,
              'x':0.5,
              'xanchor': 'center',
              'yanchor': 'top'}
            )
  fig.update_yaxes(automargin=True)
  fig.update_xaxes(automargin=True)

  fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return fig_json

def excel(df):
  ethScan = "ethscan.xlsx"
  with pd.ExcelWriter(ethScan) as writer:  
    df.to_excel(writer, sheet_name="transactionMaster")

# walletbalanceovertime(df())


#returns df of address and freq of interactions
#trying to implement total value accross transactions
def transactionFrequencyCSV(address):
  
  tx = getInternalTx(address)
  tx += getTx(address)
  addresslist = []
  for i in tx:
    if i.get("from") != address:
      adr = i.get("from")
    if i.get("to") != address:
      adr = (i.get("to"))
    obj = {'address': adr}
    addresslist.append(obj)
  
  df = pd.DataFrame(data=addresslist).sort_values('address',axis=0, ascending=True)

  masterlist = []
  for adr in addresslist:
    obj = {'address': adr.get('address'), 'frequency': addresslist.count(adr)}
    masterlist.append(obj)
# add way to see total value transacted  
  returnDf = pd.DataFrame(data = masterlist).sort_values('frequency', axis=0, ascending=True)
  returnDf = returnDf[(returnDf["frequency"]>1)]
  returnDf = returnDf.drop_duplicates(subset="address")
  fig = px.bar(returnDf, x='frequency', y='address', title='Wallet Interactions', 
            # hover_data=['address'], 
            labels={
              "address": "Address", "frequency": "Interactions"
            },
            color_discrete_sequence=['#2ba84a'],
            template="simple_white",
            )
  fig.update_layout(width=1000, height=500,
            title_font_color="#2ba84a",
            title_font_size=20,
            autosize=True,
            font_family="Raleway",
            hoverlabel={
              'bordercolor': '#fff',
              'bgcolor': '#fff',
              'font': {
                'family': 'PT Sans Narrow',
                'color': '#2ba84a',
                'size': 14,
              },
            },
            hovermode="y unified",
            title={
              'y':0.9,
              'x':0.5,
              'xanchor': 'center',
              'yanchor': 'top'}
            )
  fig.update_yaxes(automargin=True)
  fig.update_xaxes(automargin=True)

  fig.update_yaxes(showticklabels=False)
  fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return(fig_json)

if __name__ == "__main__":
  application.run(debug = False)

#some new change
