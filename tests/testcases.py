from interactive import interactive
import sys

#=================================================================================================

if __name__ == "__main__":
    #==============================================================================================
    def sub(*args):
        def helloworld():
            options = []
            return interactive.menu(f'hello world', f"hello!", options)
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
        return interactive.menu('sub panel', f"this is panel {num}", options)
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
             'param': [1]
            }
        },
        {
         'text': "open panel 2", 
         'color': 'blue', 
         'id': 'sub2', 
         'func': 
            {
             'body': sub, 
             'param': [2]
            }
        }
    ]
    interactive.home_menu('HOME', welcome_text, options)