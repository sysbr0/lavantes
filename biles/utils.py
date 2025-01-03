import pandas as pd
from .models import TrBills

# Fetch data from TrBills model
def get_data():
    queryset = TrBills.objects.all().values('price', 'net', 'top', 'is_paid', 'done')
    df = pd.DataFrame(queryset)
    return df
