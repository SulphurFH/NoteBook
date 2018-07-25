# -*- coding: utf-8 -*-


def args_decorator(permission):

    def wrapper(func):
        print 'you permission is ' + permission

        def second_wrapper(*args, **kwargs):
            print 'permission is ' + permission
            print 'second world'
            func(*args, **kwargs)
        return second_wrapper
    return wrapper


@args_decorator('check_view')
def print_full_name(first_name, last_name):
    print "My name is", first_name, last_name


print_full_name("Peter", "Venkman")
