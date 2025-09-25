def positional_arguments_without_keys(*myargs): # single asterisk means positional argument
    print(myargs) 

def key_arguments(**kwargs): # double asterisk means key value pair arugments
    print(kwargs)

def positional_key_arguments(*args, **keyargs):
    print(args, keyargs)
    print(*args)


print(positional_arguments_without_keys(20, "string", True, None))
print(key_arguments(a=20, dd=29))
print(positional_key_arguments(20, 30, a="hello"))


# arguments with one asterisk 
