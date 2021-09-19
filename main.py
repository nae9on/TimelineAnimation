from xlsparser import XlsParser
from timeline import Timeline
from performance import Performance
from animation import Animation


if __name__ == "__main__":

    paths = {'Ref': './data/Ref.xlsx',
             'Res': './data/Result.xlsx'}

    reference = Timeline(XlsParser(paths['Ref']))
    result = Timeline(XlsParser(paths['Res']))

    performance = Performance(reference, result)
    performance.print_results()

    animation = Animation(reference, result, Timeline.precision)
    animation.create_animation(save=False)