import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import re


#reライブラリで探索
def toggle_trailing_negative(s: str) -> str:
        # 末尾が (-123) なら外す
        if re.search(r'\(-\d+\)$', s):
            return re.sub(r'\(-(\d+)\)$', r'\1', s)
        # 末尾に数字列があれば包む
        m = re.search(r'(\d+)$', s)
        if m:
            start, end = m.span(1)
            return s[:start] + f"(-{m.group(1)})"
        return s  # 末尾が数字でなければそのまま



class MainWindow(QMainWindow):#QMainWindowというのを親クラスにして継承する

    def __init__(self):

        super().__init__()          
        
        self.setWindowTitle("電卓")
        self.setGeometry(100, 100, 540, 540)
        self.createWidgets()
    
    
    

    def createWidgets(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        central.setStyleSheet("background-color:rgba(11,22,26,1); color: white; font-size: 27px;") #rgba RGBとaは透明度

        
        
        # root = [display, grid, grid2]のスタックになっている(イメージ)
        # rootのheadが一番上部に表示され、tailが下
        root = QVBoxLayout(central)
        root.setContentsMargins(50, 100, 50, 16)  # 左 上 右 下
        root.setSpacing(12)

        # ★ 上部の横長表示欄
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(48)
        self.display.setStyleSheet("color: white; font-size: 28px;")
        root.addWidget(self.display)
        
        
        
        #ボタンを配置
        grid = QGridLayout(central)
        grid.setContentsMargins(50,50,50,0) #左上右下の外余白幅
        grid.setHorizontalSpacing(17)
        grid.setVerticalSpacing(17) #要素数１８
        root.addLayout(grid)
        

        numbers = ["AC","(-)", '%', '÷','7','8','9','✕','4','5','6', '-','1','2','3', '+']
        for i, num in enumerate(numbers):
            r= i // 4
            c= i % 4
            # 行・列（0始まり）
            btn = QPushButton(num)
            btn.setMinimumSize(64, 40)   # 小さすぎ防止
            btn.clicked.connect(lambda clicked=False, ch=num: self.calculation(ch))
            grid.addWidget(btn, r, c)
        
        #0,=ボタンについてgrid2を作成
        grid2 = QGridLayout(central)
        grid2.setContentsMargins(50,0,50,16) #左上右下の外余白幅
        grid2.setHorizontalSpacing(2)
        grid2.setVerticalSpacing(2)
        root.addLayout(grid2)
        
        btn0 = QPushButton("0")
        btn0.setMinimumSize(64, 40)
        btn0.clicked.connect(lambda clicked=False, ch="0": self.calculation(ch))
        grid2.addWidget(btn0, 0, 0)
        
        btnEq = QPushButton("=")
        btnEq.setMinimumSize(64, 40)
        btnEq.clicked.connect(lambda clicked=False, ch="=": self.calculation(ch))
        grid2.addWidget(btnEq, 0, 3, 1,1)
        

        
        
        
    def calculation(self, numb: str):
        cur = self.display.text()

        if numb == "AC":
            self.display.setText("0")
            return

        
        if numb == "(-)":
            if cur[-1] == "0":
                return
            self.display.setText(toggle_trailing_negative(cur))
            return

        # 3) 数字入力（桁として連結）
        if numb.isdigit():
            if cur[-1] == ')':
                return
            if cur == "0":
                self.display.setText(numb)           # 先頭0は置き換え
            else:
                self.display.setText(cur + numb)     # 末尾に連結
            return
        if numb in {"%", "÷", "+", "-", "✕"}:
            if cur[-1] in {"%", "÷", "+", "-", "✕"}:
                pass
            else:
                self.display.setText(cur + numb)
        if numb == "=":
            if cur[-1] in {"%", "÷", "+", "-", "✕"}:
                return
            expr = cur.replace("÷", "/").replace("✕", "*")
            #ゼロ除算回避
            try:
                ans = eval(expr)
                self.display.setText(str(ans))
            except Exception as e:
                self.display.setText("Nothing")

                

    
    
    
    
        
        




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 