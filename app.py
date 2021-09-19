from src.xlsparser import XlsParser
from src.timeline import Timeline
from src.performance import Performance
from src.animation import Animation


if __name__ == "__main__":

    paths = {'Ref': './data/Ref.xlsx',
             'Res': './data/Result.xlsx'}

    reference = Timeline(XlsParser(paths['Ref']))
    result = Timeline(XlsParser(paths['Res']))

    performance = Performance(reference, result)
    performance.print_results()

    animation = Animation(reference, result, Timeline.precision)
    animation.create_animation(save=False)