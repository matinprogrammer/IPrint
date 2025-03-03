# IPrint (indent print)
you can use easy like print but this print has indent and color
that create better readable for you

## where use IPrint?
**Debugging** **learning** and, in general, visually inspecting values accurately and easily is very useful.

## why use IPrint?
For better display and **readability** of result of code for humans.

## how to install
    pip install indent-print

## how to use
`iprint()` for indent print

`cprint()` for indent and colorize print

`status_print()` for print all data about instance of class(variable, method, ...)

    >>> from iprint import iprint, cprint, status_print

    >>> iprint(any_data)
    >>> cprint(any_data)
    >>> status_print(any_instance)

# Example:
    class AnotherData:
        """document of test class"""
        class_variable = "class_variable_value"
    
        def __init__(self, data):
            self.instance_variable = data
    
        def instance_method(self):
            pass
    
        @classmethod
        def class_method(cls):
            pass
    
        @staticmethod
        def static_method():
            pass
    
        @property
        def property_variable(self):
            return "property_variable_value"

    string_data = "my name is matin"
    int_data = 20
    another_data = AnotherData()
    dict_data = {"auther": "matin ahmadi", "github": "https://github.com/matinprogrammer"}
    set_data = {1, 2, 3}
    list_data = [string_data, int_data, another_data, dict_data, set_data, [[["test list"]]]]

`>>> iprint(list_data)`

![Screenshot of example code of iprint](media/example_of_iprint.png)


`>>> cprint(list_data)`

![Screenshot of example code of iprint](media/example_of_cprint.png)

`>>> status_print(another_data, show_dunder_attr=True, colorize=True)`

![Screenshot of example code of iprint](media/example_of_status_print.png)

## Features:
+ indent data you use
+ colorize your data
+ write data with indent in file so easy
+ print all data about instance of class

## customize
### custom indent length
default indent is 4(its mean 4 white space)

    >>> iprint([1], indent=8)
    [
            1
    ]

### write in file
NOTE: cprint hasn't got file parameter(cant write colorize text in file)

    >>> with open(test.txt, "w") as test_file:
            iprint(mydata, file=test_file)
### change seperator of input data
default seperator is " "(white space)

    >>> iprint(1, 2, 3, sep="-")
    1-2-3

### change end character
default seperator is "\n"(new line)

    >>> iprint(1, 2, 3, end="*")
    1 2 3*


    
