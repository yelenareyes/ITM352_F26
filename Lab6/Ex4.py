year = int(input("Enter a year: "))

if(year % 4) ==0:
    if( year % 100) == 0:
        if (year% 400) == 0:
            print("{0} is a leap year", format(year)

    else:
        print("{0} is not a leap year", format(year))
    else:
        print("{0} is a leap year", format(year))
else:
    print("{0} is not a leap year", format )year))
            
                 def is_leap_year(year):
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("year must be an integer")

    if year <= 0:
        raise ValueError("year must be positive")

    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) 
