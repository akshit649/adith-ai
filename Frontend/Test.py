from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
import sys

app = QApplication(sys.argv)
label = QLabel()
movie = QMovie("C:/Users/ASUS/Desktop/adith AI/Frontend/Graphics/Jarvis.gif")

label.setMovie(movie)
movie.start()
label.show()
sys.exit(app.exec_())
