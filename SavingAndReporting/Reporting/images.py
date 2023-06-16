from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
import pandas as pd
import matplotlib.pyplot as plt
from SavingAndReporting import imgs_path

def make_image(id: str):
    historic = HistoricController.get_all_historic_rows(id)
    df = pd.DataFrame(historic).sort_values('datetime')
    fig = plt.figure(facecolor="lightblue")
    x = df['datetime']
    y1 = df['balance_close']
    y2 = df['equity_close']
    plt.style.use('ggplot')

    plt.plot(x, y2, label="Equity",color='tab:orange')
    plt.plot(x, y1, label="Balance",color='tab:blue')
    plt.xticks(rotation=20, ha='right')
    plt.title('Account: '+id, fontname='Arial',color=(111/255,111/255,111/255),fontsize=20)
    plt.legend(loc="upper left")
    plt.savefig(imgs_path+id+".png")


