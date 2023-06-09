from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
import pandas as pd
id="15843602"
historic=HistoricController.get_last_30days_historic_rows(id)
df = pd.DataFrame(historic)

print(df.iloc[1])
