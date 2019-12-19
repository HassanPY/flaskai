from wtforms import Form, FloatField, DateField, IntegerField, validators

class StockPriceForm(Form):

    stockdate = DateField('Stockdate')
    openprice = FloatField('Openprice')
    lowprice = FloatField('Lowprice')
    highprice = FloatField('Highprice')
    volume = IntegerField('Volume')
