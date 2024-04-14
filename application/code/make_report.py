from make_pdf import BuildPDF
from datetime import datetime

from pyecharts.render import make_snapshot
from snapshot_pyppeteer import snapshot

import os
import logging


class BuildReport(BuildPDF):
    def __init__(self, report_date, image_path, image_dict, text_dict):
        super().__init__()
        self.report_date = report_date
        self.image_path = image_path
        self.image_dict = image_dict
        self.text_dict = text_dict
        self.logger = logging.getLogger(__name__)  # Create a logger

    def financial_report(self):
        self.pdf_ = list()

        self.logger.info('Creating Financial Market Report PDF...')
        self.insert_main_title('Financial Market Report')
        self.insert_sub_title(self.report_date)

        part1 = 'Overview'
        self.logger.info(f'Inserting section: {part1}')
        self.insert_heading1('I. ' + part1)
        self.insert_text(self.text_dict[part1])

        parts = ['Stock Market', 'Bond Market']
        nums = ['II', 'III']
        for num, part in zip(nums, parts):
            self.logger.info(f'Inserting section: {part}')
            self.insert_heading1(num + '. ' + part)
            self.insert_text(self.text_dict[part])
            for image in self.image_dict[part]:
                image_path = os.path.join(self.image_path, image)
                self.insert_image(image_path, 0.35)

        part4 = 'Summary'
        self.logger.info(f'Inserting section: {part4}')
        self.insert_heading1('V. ' + part4)
        self.insert_text(self.text_dict[part4])

        self.logger.info('Exporting Financial Market Report PDF...')
        self.export_pdf('../report_pdf/Financial Market Report.pdf')
        self.logger.info('Financial Market Report PDF created successfully.')


if __name__ == '__main__':

    current_dt = str(datetime.now().date())
    print('Current date is ', current_dt)

    # Iterate over the files in the folder
    html_folder = '../output_html'
    png_folder = '../output_png'

    change_flag = False
    if change_flag:
        for file_name in os.listdir(html_folder):
            # Check if the file is an HTML file
            if file_name.endswith('.html'):
                # Extract the title from the HTML file name (assuming the title is before the '.html' extension)
                title = file_name[:-5]  # Remove the '.html' extension
                # Convert the HTML file to PNG
                make_snapshot(snapshot,
                              os.path.join(html_folder, file_name),
                              os.path.join(png_folder, '{}.png'.format(title)))

    # prepare for the image and text
    image_dict = {
        'Stock Market': ['Stock Index.png',
                         'MA5 of Stock Index.png',
                         'MA10 of Stock Index.png',
                         'MA20 of Stock Index.png',
                         'RSI of Stock Index.png',
                         'MACD of Stock Index.png',
                         'MACD Signal of Stock Index.png',
                         'Bollingar Bands of Stock Index.png',
                         'Returns of Stock Index.png',
                         'Volatilities of Stock Index.png',
                         'Chinese VIX.png'],
        'Bond Market': ['China Government Bond YTM.png',
                        'Government Bond YTM 10Y-2Y Spread in CN and US.png']
    }
    text_dict = {
        'Overview': 'These indicators cover fixed income, stock, options, and other markets. For each major category of indicators, we can automatically generate weekly results from the database. This result can effectively assist us in market analysis and forecasting. ',
        'Stock Market': "The Chinese stock indices reflect the overall performance of the Chinese stock market. They serve as barometers of the nation's economic health and investor sentiment. These indices track the performance of listed companies on the Shanghai and Shenzhen stock exchanges respectively. Investors analyze these indices to gauge market direction and sentiment, influencing investment decisions. Factors such as government policies, economic data, and global market trends impact the movement of these indices, providing insights into China's economic trajectory and market sentiment. iVX is short for SSE 50 ETF Volatility Index, which is derived based on the SSE 50 ETF option contracts, reflecting the investors' expectations for the volatility of the 50 ETF in the next 30 days. When iVX rises, the investors expect a decreasing market and the market becomes more volatile.",
        'Bond Market': 'For the study of fixed income, particularly in bonds, we utilize Chinese government bond yields to maturity (TYM), Chinese government bond futures settlement prices, and US Treasury bond yields to maturity (YTM) from our database for analysis.',
        'Summary': 'Part of the report content for the market is as shown above. Subsequent work can focus on further analysis of the preliminary reports, selecting intuitive content for in-depth analysis.'
    }

    report_ = BuildReport(current_dt, png_folder, image_dict,  text_dict)
    report_.financial_report()