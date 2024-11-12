from datetime import date, datetime
from decimal import Decimal
import json
from marshmallow import Schema, fields
from typing import Union

class Stock:
    def __init__(self, symbol, date, open, high, low, close, volume):
        """Initialize a Stock object.

        Args:
            symbol (str): The stock symbol.
            date (str): The date of the stock data.
            open (Decimal): The opening price.
            high (Decimal): The highest price.
            low (Decimal): The lowest price.
            close (Decimal): The closing price.
            volume (int): The volume of stocks traded.
        """
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        """Initialize a Trade object.

        Args:
            symbol (str): The stock symbol.
            timestamp (str): The timestamp of the trade.
            order (str): The type of order (buy/sell).
            price (Decimal): The price at which the trade was executed.
            volume (int): The volume of stocks traded.
            commission (Decimal): The commission charged for the trade.
        """
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.volume = volume
        self.commission = commission

# Exercise 1: Custom JSON Encoder
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal to string
        elif isinstance(obj, (Stock, Trade)):
            # Add a type identifier to distinguish between Stock and Trade objects
            result = obj.__dict__.copy()
            result['__type__'] = obj.__class__.__name__
            return result
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

# Exercise 2: Custom JSON Decoder
def custom_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == 'Stock':
            # Convert date string back to date object
            obj['date'] = datetime.strptime(obj['date'], '%Y-%m-%d').date()
            # Convert decimal strings back to Decimal objects
            for key in ['open', 'high', 'low', 'close']:
                obj[key] = Decimal(obj[key])
            del obj['__type__']
            return Stock(**obj)
        elif obj['__type__'] == 'Trade':
            # Convert timestamp string back to datetime object
            obj['timestamp'] = datetime.fromisoformat(obj['timestamp'])
            # Convert decimal strings back to Decimal objects
            obj['price'] = Decimal(obj['price'])
            obj['commission'] = Decimal(obj['commission'])
            del obj['__type__']
            return Trade(**obj)
    return obj

# Exercise 3: Marshmallow Implementation
class StockSchema(Schema):
    """Schema for serializing Stock objects."""
    symbol = fields.Str()
    date = fields.Str()
    open = fields.Decimal()
    high = fields.Decimal()
    low = fields.Decimal()
    close = fields.Decimal()
    volume = fields.Int()

class TradeSchema(Schema):
    """Schema for serializing Trade objects."""
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal()
    volume = fields.Int()
    commission = fields.Decimal()

def serialize_with_marshmallow(obj):
    """Serialize an object using the appropriate Marshmallow schema.

    Args:
        obj (Union[Stock, Trade]): The object to serialize.

    Returns:
        str: The serialized JSON string of the object.

    Raises:
        TypeError: If the object type is not supported.
    """
    if isinstance(obj, Stock):
        return StockSchema().dumps(obj, cls=CustomEncoder)
    elif isinstance(obj, Trade):
        return TradeSchema().dumps(obj, cls=CustomEncoder)
    raise TypeError(f"Object of type {type(obj)} is not supported")

def deserialize_with_marshmallow(json_str, schema):
    """Deserialize JSON string using the provided schema.

    Args:
        json_str (str): The JSON string to deserialize.
        schema (Schema): The Marshmallow schema to use for deserialization.

    Returns:
        object: The deserialized object.
    """
    return schema.loads(json_str) 