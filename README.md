TIV (Intel)
=============
* Tools required:
   - python 2.7
   - java 1.7
   - ant
   - flex
   - bison

Build Instructions
=====================

`./configure`

Run Instructions
====================
`cd src`

`./driver.py -h` (will show all the required parameters)

`./driver.py <DOMAIN_FILE_FOR_FF_PLANNER> <PROBLEM_FILE_FOR_FF_PLANNER>`

Test
====================
For testing purpose we've provided 3 sample input files in the directory `ff_planner_input_files`.

`.src/driver.py ff_planner_input_files/arm_domain.pddl ff_planner_input_files/arm_problem_1`


If everything goes correct, this will generate an `.asm` file in the `src` directory, which is the output of the tool.
