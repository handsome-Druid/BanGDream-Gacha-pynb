import sys
import time
import traceback
import tempfile
import datetime
import random
from PyQt5 import QtWidgets
from Ui_gacha_gui import Ui_MainWindow
import bangdreamgacha_numba
from font_loader import init_application, init_fonts_after_app


def _safe_text(obj):
    try:
        return str(obj)
    except Exception:
        try:
            return repr(obj)
        except Exception:
            return '<unprintable>'


def run():
    # 初始化应用（高DPI等）
    init_application()
    app = QtWidgets.QApplication(sys.argv)
    init_fonts_after_app(app)

    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # 业务逻辑（集中管理，避免重复）
    def random_seed():
        seed = random.randint(0, 2**31 - 1)
        ui.seed.setText(str(seed))

    def run_simulation():
        try:
            total5 = ui.total5.value()
            want5 = ui.want5.value()
            want4 = ui.want4.value()
            normal = 1 if ui.normal.isChecked() else 0
            sims = int(ui.sims.text())
            seed = int(ui.seed.text())

            if want5 > total5:
                raise ValueError("想要5星不能超过总数")

            ui.status.setText("模拟中...")
            ui.output.clear()
            QtWidgets.QApplication.processEvents()

            start = time.time()
            arr = bangdreamgacha_numba.simulate_batch_numba(total5, want5, want4, normal, sims, seed)
            exp, med, p90, worst = bangdreamgacha_numba.summarize(arr)
            dur = time.time() - start

            result = f"""期望抽卡次数: {exp}
中位数抽卡次数: {med}
90%玩家在以下抽数内集齐: {p90}
非酋至多抽卡次数: {worst}
总耗时： {dur:.3f}秒"""
            ui.output.setText(result)
            ui.status.setText("完成")
        except Exception as e:
            tb = traceback.format_exc()
            try:
                ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                fn = f"gacha_error_{ts}.log"
                p = tempfile.gettempdir()
                path = p + "\\" + fn
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(tb)
            except Exception:
                path = 'N/A'
            short = f"错误: {_safe_text(e)}\n（详细堆栈已写入: {path}）"
            ui.output.setText(short)
            ui.status.setText("错误")

    ui.run_btn.clicked.connect(run_simulation)
    ui.random_seed_btn.clicked.connect(random_seed)

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
