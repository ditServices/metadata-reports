import sys
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import date


class DataReport:
    date = date.today()

    def __init__(self, sourcefile, outfile, title):
        print(sourcefile, outfile)

        df = pd.read_csv(sourcefile)
        data_report = pd.pivot_table(df, index=["Name", "Camera"])

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("report_template.html")

        template_vars = {"title": title,
                         "data": data_report.to_html(),
                         "date": self.date,
                         }

        html_output = template.render(template_vars)
        HTML(string=html_output).write_pdf(outfile)


def main():
    report = DataReport(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
