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

        col_order = ['File Name', 'Camera #', 'Resolution', 'Duration TC',
                     'Video Codec', 'Frame Rate', 'Comments']

        df = pd.read_csv(sourcefile,
                         encoding="utf-16",
                         usecols=['File Name', 'Camera #', 'Resolution', 'Duration TC', 'Video Codec', 'Frame Rate', 'Comments'],
                         dtype={"File Name": str,
                                "Camera #": str,
                                "Resolution": str,
                                "Duration TC": str,
                                "Video Codec": str,
                                "Frame Rate": float,
                                "Comments": str,
                                'Date Modified': str,
                                'Date Recorded': str
                                },
                         na_values=['.', '??', ' ']  # Take any '.' or '??' values as NA
                         )

        df = df[col_order]
        print(df.head())
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("report_template.html")

        template_vars = {"title": title,
                         "data": df.to_html(),
                         "date": self.date,
                         }

        html_output = template.render(template_vars)
        HTML(string=html_output).write_pdf(outfile)


def main():
    report = DataReport(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
