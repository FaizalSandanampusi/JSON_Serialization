import pytest
from datetime import date, datetime
from decimal import Decimal
import json
from assignment18 import (
    Stock, Trade, CustomEncoder, custom_decoder,
    StockSchema, TradeSchema, serialize_with_marshmallow, deserialize_with_marshmallow
)

# Sample data for testing
@pytest.fixture
def activity():
    return {
        "quotes": [
            Stock('TSLA', date(2018, 11, 22), 
                  Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
            Stock('AAPL', date(2018, 11, 22), 
                  Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
            Stock('MSFT', date(2018, 11, 22), 
                  Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
        ],
        "trades": [
            Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
            Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
        ]
    }

def test_custom_encoder_stock_serialization(activity):
    """Test that Stock objects are serialized correctly with CustomEncoder."""
    stock_json = json.dumps(activity["quotes"][0], cls=CustomEncoder)
    assert '"symbol": "TSLA"' in stock_json
    assert '"date": "2018-11-22"' in stock_json

def test_custom_encoder_trade_serialization(activity):
    """Test that Trade objects are serialized correctly with CustomEncoder."""
    trade_json = json.dumps(activity["trades"][0], cls=CustomEncoder)
    assert '"symbol": "TSLA"' in trade_json
    assert '"timestamp": "2018-11-22T10:05:12"' in trade_json

def test_custom_encoder_nested_serialization(activity):
    """Test that a nested dictionary with Stock and Trade objects is serialized correctly."""
    nested_json = json.dumps(activity, cls=CustomEncoder)
    assert '"quotes"' in nested_json
    assert '"trades"' in nested_json

def test_custom_decoder_stock_deserialization(activity):
    """Test that Stock objects are deserialized correctly with CustomDecoder."""
    stock_json = json.dumps(activity["quotes"], cls=CustomEncoder)
    stocks = json.loads(stock_json, object_hook=custom_decoder)
    assert isinstance(stocks[0], Stock)
    assert stocks[0].symbol == 'TSLA'

def test_custom_decoder_trade_deserialization(activity):
    """Test that Trade objects are deserialized correctly with CustomDecoder."""
    trade_json = json.dumps(activity["trades"], cls=CustomEncoder)
    trades = json.loads(trade_json, object_hook=custom_decoder)
    assert isinstance(trades[0], Trade)
    assert trades[0].symbol == 'TSLA'

def test_marshmallow_stock_serialization(activity):
    """Test that Stock objects are serialized correctly with Marshmallow."""
    stock_json = serialize_with_marshmallow(activity["quotes"][0])
    assert "TSLA" in stock_json
    assert "2018-11-22" in stock_json

def test_marshmallow_trade_serialization(activity):
    """Test that Trade objects are serialized correctly with Marshmallow."""
    trade_json = serialize_with_marshmallow(activity["trades"][0])
    assert "TSLA" in trade_json
    assert "2018-11-22T10:05:12" in trade_json

def test_marshmallow_stock_deserialization(activity):
    """Test that Stock objects are deserialized correctly with Marshmallow."""
    stock_json = serialize_with_marshmallow(activity["quotes"][0])
    stock = deserialize_with_marshmallow(stock_json, StockSchema())
    assert stock['symbol'] == 'TSLA'

def test_marshmallow_trade_deserialization(activity):
    """Test that Trade objects are deserialized correctly with Marshmallow."""
    trade_json = serialize_with_marshmallow(activity["trades"][0])
    trade = deserialize_with_marshmallow(trade_json, TradeSchema())
    assert trade['symbol'] == 'TSLA' 