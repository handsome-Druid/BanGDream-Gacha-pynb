import sys
import time
import traceback
import tempfile
import datetime
import secrets
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
    init_fonts_after_app()

    main_window = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    # 确保输出区域文字为白色（覆盖局部样式缺省）
    try:
        _style = ui.output.styleSheet() or ""
        if "color:" not in _style:
            sep = "\n" if _style and not _style.endswith("\n") else ""
            ui.output.setStyleSheet(f"{_style}{sep}color: white;")
    except Exception:
        pass

    # 业务逻辑（集中管理，避免重复）
    def random_seed():
        # 使用加密安全的随机数生成，避免 SonarLint 关于弱随机数的告警（S2245）
        seed = secrets.randbelow(2**31)
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

            # 先对抽卡次数取整（四舍五入），再计算星石消耗
            exp_i = int(round(exp))
            med_i = int(round(med))
            p90_i = int(round(p90))
            worst_i = int(round(worst))

            # 使用 HTML 表格让“花费”一列垂直对齐显示
            result_html = f"""
<div style="color: #ffffff;">
    <table style="border-collapse: collapse;">
        <tr>
            <td style="padding-right: 12px; white-space: nowrap;">期望抽卡次数: {exp}</td>
            <td style="padding: 0 8px; white-space: nowrap;">花费</td>
            <td style="white-space: nowrap;">{exp_i*250}星石</td>
        </tr>
        <tr>
            <td style="padding-right: 12px; white-space: nowrap;">中位数抽卡次数: {med}</td>
            <td style="padding: 0 8px; white-space: nowrap;">花费</td>
            <td style="white-space: nowrap;">{med_i*250}星石</td>
        </tr>
        <tr>
            <td style="padding-right: 12px; white-space: nowrap;">90%玩家在以下抽数内集齐: {p90}</td>
            <td style="padding: 0 8px; white-space: nowrap;">花费</td>
            <td style="white-space: nowrap;">{p90_i*250}星石</td>
        </tr>
        <tr>
            <td style="padding-right: 12px; white-space: nowrap;">非酋至多抽卡次数: {worst}</td>
            <td style="padding: 0 8px; white-space: nowrap;">花费</td>
            <td style="white-space: nowrap;">{worst_i*250}星石</td>
        </tr>
    </table>
    <div style="margin-top: 4px;">总耗时： {dur:.3f}秒</div>
</div>
"""
            ui.output.setHtml(result_html)
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

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
