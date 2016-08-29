# Intel_TIV

`sudo apt-get install openjdk-7-jdk`

`sudo apt-get install ant`

`sudo apt-get install flex`

`sudo apt-get install bison`

`export MICROTESK_HOME=/home/dibyendu/Desktop/microtesk-2.3.0-alpha`

`cd $MICROTESK_HOME`

`sh bin/compile.sh arch/arm/model/arm.nml`

`sh bin/generate.sh arm arch/arm/templates/euclid.rb`

`./ff -o arm_domain.pddl -f arm_problem_case_2`
