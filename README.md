# MPrint, CPrint
you can use easy like print but this print has indent and color
that create better readable for you


## Features:
+ indent data you use
+ colorize your data
+ write data with indent in file so easy


# Example:
    class AnotherData:
        pass
    string_data = "my name is matin"
    int_data = 20
    another_data = AnotherData()
    dict_data = {"auther": "matin ahmadi", "github": "https://github.com/matinprogrammer"}
    set_data = {1, 2, 3}
    list_data = [string_data, int_data, another_data, dict_data, set_data, [[["test list"]]]]

`>>> mprint(list_data)`

![Screenshot of example code of mprint](media/example_of_mprint.png)


`>>> cprint(list_data)`

![Screenshot of example code of mprint](media/example_of_cprint.png)


## how to install

## how to use

    >>> from mprint import mprint

    >>> mprint(anydata)

## customize
### custom indent length
default indent is 4(its mean 4 white space)

    >>> mprint([1], indent=8)
    [
            1
    ]

### write in file
NOTE: cprint hasn't got file parameter(cant write colorize text in file)

    >>> with open(test.txt, "w") as test_file:
            mprint(mydata, file=test_file)
### change seperator of input data
default seperator is " "(white space)

    >>> mprint(1, 2, 3, sep="-")
    1-2-3

### change end character
default seperator is "\n"(new line)

    >>> mprint(1, 2, 3, end="*")
    1 2 3*


    