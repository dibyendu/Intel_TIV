AC_PREREQ(2.69)
AC_INIT([TIV], [1.0])
AM_INIT_AUTOMAKE

MICROTESK_ROOT=`pwd`/microtesk-2.3.0-alpha
FF_ROOT=`pwd`/FF-v2.3
AC_SUBST(MICROTESK_ROOT)
AC_SUBST(FF_ROOT)

# Checks for programs.
AC_PROG_CC

AC_CHECK_PROG(PYTHON, python, yes, no)
if test x"$PYTHON" == x"no"
then
  AC_MSG_ERROR([Please install python (version 2.7) before installing."])
fi

AC_CHECK_PROG(JAVA, javac, yes, no)
if test x"$JAVA" == x"no"
then
  AC_MSG_ERROR([Please install jdk (version 1.7) before installing ... on a debian system run "sudo apt-get install openjdk-7-jdk"])
fi

AC_CHECK_PROG(ANT, ant, yes, no)
if test x"$ANT" == x"no"
then
  AC_MSG_ERROR([Please install ant before installing ... on a debian system run "sudo apt-get install ant"])
fi

AC_PROG_YACC
if test x"$YACC" != x"bison -y"
then
  AC_MSG_ERROR([Please install bison before installing ... on a debian system run "sudo apt-get install bison"])
fi

AC_PROG_LEX
if test "x$LEX" != xflex
then
  AC_MSG_ERROR([Please install flex before installing ... on a debian system run "sudo apt-get install flex"])
fi

#extracting the src of Micro-Tesk and compiling microtesk ARM model
tar -xzf microtesk-2.3.0-alpha.tar.gz
tar -xzf arm.tar.gz
mv -f arm/etc/settings.xml microtesk-2.3.0-alpha/etc/
rm -r arm/etc
mv arm microtesk-2.3.0-alpha/arch/

export MICROTESK_HOME=`pwd`/microtesk-2.3.0-alpha
pushd $MICROTESK_HOME
AC_MSG_NOTICE([compiling ARM model for Micro-Tesk ...])
sh bin/compile.sh arch/arm/model/arm.nml
popd

#extracting the src of FF and compiling
tar -xzf FF-v2.3.tar.gz
pushd FF-v2.3
AC_MSG_NOTICE([compiling FF planner ...])
make
popd

AC_OUTPUT([src/driver.py])
chmod +x src/driver.py
rm config.*
