import pygame
import sys

# Define the template check function
def check_template():
    '''
    Check the template for missing elements and syntax errors.
    '''
    missing_elements = []
    syntax_errors = []

    # TODO: Implement the elements and syntax verification logic
    # Dummy checks (to replace with real checks)
    if 'gravity_effect' not in globals():
        missing_elements.append('gravity_effect')
    if 'particle_collision' not in globals():
        missing_elements.append('particle_collision')
    if 'mouse_repulsion' not in globals():
        missing_elements.append('mouse_repulsion')

    if missing_elements:
        print('Missing elements:', missing_elements)
    else:
        print('All elements present.')

    # Return true if everything is fine, else false
    return not missing_elements and not syntax_errors

if __name__ == '__main__':
    if not check_template():
        sys.exit('Template check failed. Please add the missing components.')
    else:
        print('Template check passed. Ready to proceed.')