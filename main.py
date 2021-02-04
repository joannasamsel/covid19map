from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
from kaggle_api import download_data_files
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas as gpd
import pandas as pd
import datasets
import sys
import menu

class ExampleApp(QtWidgets.QMainWindow, menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.button1.clicked.connect(self.clicked)

    def clicked(self):
        date = self.dateEdit.date().toPyDate()
        if self.radioButton.isChecked():
            plot_name = 'Cases per day'
            chartData = datasets.get_cases_per_day(self.geoData, date)
        elif self.radioButton_2.isChecked():
            plot_name = 'Death per day'
            chartData = datasets.get_death_per_day(self.geoData, date)
        elif self.radioButton_3.isChecked():
            plot_name = 'Cases with deaths per day'
            chartData = datasets.get_cases_per_day(self.geoData, date)
            chartData_deaths = datasets.get_death_per_day(self.geoData, date)

        if chartData.empty:
            self.label_3.setText('No data, enter another date')
        elif plot_name == 'Cases per day' or plot_name == 'Death per day':
            plot(plot_name, date, self.world, chartData)
        else:
            joined_plot(self.world, chartData, chartData_deaths)


    world = datasets.get_world()
    geoData = datasets.get_geo_data()
    clicked_int = 0


def main():
    download_data_files()
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


def plot(plot_name, date, world, geoData):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    world.plot(ax=ax, color='rosybrown', figsize=(40, 30))
    if plot_name == 'Cases per day':
        axs = geoData.plot(ax=ax, marker='o', c=geoData['size_values'], cmap='PuRd', figsize=(40, 30),
                           markersize=geoData['size_values'], column=geoData['cases'], legend=True,
                           edgecolor='black',
                           legend_kwds={'label': "Cases by Country",
                            'orientation': "horizontal"})
        axs.set
    elif plot_name == 'Death per day':
        axs = geoData.plot(ax=ax, marker='o', c=geoData['size_values'], cmap='cividis', figsize=(40, 30),
                           markersize=geoData['size_values'], column=geoData['cases'], legend=True,
                           legend_kwds={'label': "Deaths by Country",
                                        'orientation': "horizontal"})
    axs.axis('off')
    fig.canvas.set_window_title(plot_name)
    plt.tight_layout()
    plt.show()


def joined_plot(world, geoData, geoData_deths):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    world.plot(ax=ax, color='rosybrown', figsize=(40, 30))
    geoData.plot(ax=ax, marker='o', color='orchid', markersize=geoData['size_values'])
    geoData_deths.plot(ax=ax, marker='o', color='indigo', markersize=geoData_deths['size_values'])
    plt.show()


if __name__ == '__main__':
    main()
