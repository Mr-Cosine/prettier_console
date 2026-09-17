import prettier_console as pc

if __name__ == "__main__":
    #==============================================================================================
    def sub(*args):
        def helloworld():
            options = []
            return pc.menu(f'hello world', f"hello!", options)
        #==========================================================================================
        
        num = args
        options = [
            {
             'text': "say hello", 
             'color': 'red', 
             'id': 'hello', 
             'func': 
                {
                 'body': helloworld
                }
            },
        ]
        return pc.menu('sub panel', f"this is panel {num}", options)

    #==============================================================================================
    def file():
        # leaf runs the body itself, so pass the callable unevaluated and its positional arguments separately
        return pc.leaf(
            'file selector',
            pc.select_files,
            ["Select a file here and it will let you confirm"]  # -> select_files(prompt)
        )
    #==============================================================================================

    welcome_text = 'welcome'
    options = [
        {
         'text': "open panel 1", 
         'color': 'red', 
         'id': 'sub1', 
         'func': 
            {
             'body': sub, 
             'param': [1]   # positional argument
            }
        },
        {
         'text': "open panel 2", 
         'color': 'blue', 
         'id': 'sub2', 
         'func': 
            {
             'body': sub, 
             'param': [2]   # positional argument
            }
        },
        {
         'text': "open file selection", 
         'color': 'blue', 
         'id': 'file', 
         'func': 
            {
             'body': file, 
             'param': []
            }
        },
    ]
    pc.home_menu('HOME', welcome_text, options)