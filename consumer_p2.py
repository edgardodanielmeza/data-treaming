import json
from kafka import KafkaConsumer
result = {}
consumer = KafkaConsumer(
  bootstrap_servers=["localhost:9092"],
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000,
  value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

consumer.subscribe( "stock-updates")


try:
    for message in consumer:
        data = message.value
        result.setdefault(data["symbol"], {"weighted_price": 0, "total_volume": 0, "min-offset":10000000000000})
        result[data["symbol"]]["weighted_price"] += data["price"] * data["volume"]
        result[data["symbol"]]["total_volume"] += data["volume"]
        [result[data["symbol"]]["min-offset"], message.offset]
     
except Exception as e:
    print(f"Error occurred while consuming messages: {e}") 
finally:
    for key in result:
          
            print(f"weightaed aveerdage price fotr {key}:  {result[key]['weighted_price']/result[key]['total_volume']}")
    consumer.close()
 