docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

CREATE STREAM tp2 (symbol VARCHAR,price DOUBLE, volume DOUBLE)
  WITH (kafka_topic='stock-updates', value_format='json', partitions=1);

CREATE TABLE promedio AS
 SELECT  symbol, ( sum(price * volume) /  SUM(volume)  )  AS aveerdage , count(symbol) as transacciones FROM tp2 
	GROUP BY symbol  
	EMIT CHANGES;

CREATE TABLE mima AS
 SELECT  symbol, max(price) AS maximo,  min(volume)   AS minimo  FROM tp2 
	GROUP BY symbol  
	EMIT CHANGES;


 SELECT  symbol,aveerdage  from promedio;
 SELECT  symbol,transacciones  from promedio;
 SELECT  symbol,  maximo from mima;
 SELECT  symbol,  minimo from mima;


