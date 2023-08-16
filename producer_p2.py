import websocket
import json
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError 

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

topic = "stock-updates"

#redpanda handlrs
def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

#WS handlers
def on_ws_message(ws, message):
   # print(message)
    data=json.loads(message)['data']
    records = [
    {
        "symbol": d["s"],
        "price": d["p"],
        "volume": d["v"],
        "timestamp": datetime.utcfromtimestamp(d["t"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
     }
           for d in data
     ]

    #for r in records:
        #meter esto en redpanda
        #print(r)
    for record in records:
        future = producer.send( topic, value=record )
        future.add_callback(on_success)
        future.add_errback(on_error)

def on_ws_error(ws, error):
    print(error)

def on_ws_close(ws,close_status_code, close_msg ):
    producer.flush()
    producer.close()
    print("### closed ###")

def on_ws_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cj8gvvpr01qjjsj7cmi0cj8gvvpr01qjjsj7cmig",
                              on_message = on_ws_message,
                              on_error = on_ws_error,
                              on_close = on_ws_close)
    ws.on_open = on_ws_open
    ws.run_forever()

   