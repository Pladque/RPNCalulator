from django.shortcuts import render
import requests
from Scripts import functions as f


def home_calculator(request):
    equation = request.POST.get('equation')
    if equation:
        if list(equation)[0] == '-' or list(equation)[0] == '+':
            equation = '0' + equation
        equation_in_RPN = f.trim_change_to_list_and_convert_to_RPN(equation)
        if len(equation_in_RPN)!= 0:
            equation_in_RPN_as_string = f.list_equation_to_str(equation_in_RPN)
            equation_result = f.calc_equation_in_RPN(equation_in_RPN)
            equation_result = f.delete_unnecessary_float_tail(equation_result)
            color_css = "green"
        else:
            equation_in_RPN_as_string = "INPUT ERROR"
            equation_result = "INPUT ERROR"
            color_css = "red"
        return render(request, "base.html",
                        {
                            'input_equation': equation,
                            'equation_in_RPN': equation_in_RPN_as_string,
                            'equation_result': equation_result,
                            'color_css': color_css,
                        }
                      )
    else:
        return render(request, "base.html", {})
