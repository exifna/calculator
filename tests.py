import src.lexer
import src.polska
import src.calc

s = 'log(sin(1)+2^(-2)+4)-1.8'

calc_ = True

lex = src.lexer.Lexer()
pre_res, is_function = lex.parse(s)
print(f'pre_res = {pre_res}, is_function = {is_function}')

converter = src.polska.Converter()
pre_res2 = converter.convert(pre_res)
print([x[0] for x in pre_res2])



print(src.calc.Evaluator().eval(pre_res2))


